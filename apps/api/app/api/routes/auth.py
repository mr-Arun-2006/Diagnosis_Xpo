from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.db import connection
from app.dependencies import get_current_user
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def _tokens_for_user(conn, user: dict) -> TokenResponse:
    refresh_token, expires_at = create_refresh_token()
    token_hash = hash_refresh_token(refresh_token)
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO refresh_sessions (user_id, token_hash, expires_at)
               VALUES (%s, %s, %s)""",
            (user["id"], token_hash, expires_at),
        )
    conn.commit()
    return TokenResponse(
        access_token=create_access_token(str(user["id"]), user["role"]),
        refresh_token=refresh_token,
        expires_in=settings.access_token_minutes * 60,
        user=UserResponse.model_validate(user),
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, conn=Depends(connection)):
    email = payload.email.lower().strip()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists")
        cur.execute(
            """INSERT INTO users (email, password_hash, role, language, default_exchange)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING id, email, role, language, default_exchange, notifications_enabled""",
            (email, hash_password(payload.password), payload.role, payload.language, payload.default_exchange),
        )
        user = cur.fetchone()
    return _tokens_for_user(conn, user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, conn=Depends(connection)):
    email = payload.email.lower().strip()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    with conn.cursor() as cur:
        cur.execute("UPDATE users SET last_login_at = %s WHERE id = %s", (datetime.now(timezone.utc), user["id"]))
    conn.commit()
    return _tokens_for_user(conn, user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, conn=Depends(connection)):
    token_hash = hash_refresh_token(payload.refresh_token)
    now = datetime.now(timezone.utc)
    with conn.cursor() as cur:
        cur.execute(
            """SELECT s.id AS session_id, u.id, u.email, u.role, u.language,
                      u.default_exchange, u.notifications_enabled
               FROM refresh_sessions s
               JOIN users u ON u.id = s.user_id
               WHERE s.token_hash = %s AND s.revoked_at IS NULL AND s.expires_at > %s""",
            (token_hash, now),
        )
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        cur.execute("UPDATE refresh_sessions SET revoked_at = %s WHERE id = %s", (now, user["session_id"]))
    conn.commit()
    return _tokens_for_user(conn, user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, conn=Depends(connection)):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE refresh_sessions SET revoked_at = %s WHERE token_hash = %s AND revoked_at IS NULL",
            (datetime.now(timezone.utc), hash_refresh_token(payload.refresh_token)),
        )
    conn.commit()


@router.get("/me", response_model=UserResponse)
def me(user=Depends(get_current_user)):
    return UserResponse.model_validate(user)
