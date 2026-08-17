from fastapi import APIRouter, HTTPException
import redis

from app.core.config import settings
from app.db import get_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    checks = {"database": "down", "redis": "down"}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        checks["database"] = "up"
    except Exception:
        pass

    try:
        client = redis.from_url(settings.redis_url, socket_connect_timeout=2, socket_timeout=2)
        client.ping()
        checks["redis"] = "up"
        client.close()
    except Exception:
        pass

    status = "healthy" if all(value == "up" for value in checks.values()) else "degraded"
    if status != "healthy":
        raise HTTPException(status_code=503, detail={"status": status, "service": "api", "checks": checks})
    return {"status": status, "service": "api", "checks": checks}
