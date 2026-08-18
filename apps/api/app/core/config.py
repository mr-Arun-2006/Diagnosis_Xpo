import os


class Settings:
    app_name: str = os.getenv("APP_NAME", "Diagnosis_Xpo API")
    database_url: str = os.getenv("DATABASE_URL", "postgresql://diagnosis:change-me@localhost:5432/diagnosis")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "development-only-change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
    refresh_token_days: int = int(os.getenv("REFRESH_TOKEN_DAYS", "30"))
    cors_origins: list[str] = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if x.strip()]
    ai_base_url: str = os.getenv("AI_BASE_URL", "")
    ai_model: str = os.getenv("AI_MODEL", "")
    ai_api_key: str = os.getenv("AI_API_KEY", "")


settings = Settings()

if settings.jwt_secret == "development-only-change-me" and os.getenv("ENVIRONMENT", "development") == "production":
    raise RuntimeError("JWT_SECRET must be set in production")
