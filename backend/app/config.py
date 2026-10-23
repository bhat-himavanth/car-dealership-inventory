"""App settings, read from environment variables with sensible local defaults."""
import os


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dealership.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-only-secret-change-me-in-production-please")
    jwt_algorithm: str = "HS256"
    token_expiry_minutes: int = int(os.getenv("TOKEN_EXPIRY_MINUTES", "60"))
    # Comma-separated list, e.g. "http://localhost:5173,https://my-app.vercel.app"
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


settings = Settings()