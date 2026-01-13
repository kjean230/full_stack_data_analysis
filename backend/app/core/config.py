from __future__ import annotations

from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    App settings loaded from environment variables.

    We keep field names UPPERCASE to match your current backend/.env keys
    (DB_HOST, DB_NAME, JWT_SECRET, etc.) to avoid renaming env vars.
    """

    # App
    APP_ENV: str = "dev"

    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(
        env_file=".env",                # inside container: /app/.env (because ./backend is mounted to /app)
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """
        SQLAlchemy URL for PyMySQL.

        quote_plus is important if your password has special characters like @ : / ? # etc.
        """
        user = quote_plus(self.DB_USER)
        pwd = quote_plus(self.DB_PASSWORD)
        return (
            f"mysql+pymysql://{user}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?charset=utf8mb4"
        )


settings = Settings()