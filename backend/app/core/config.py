from __future__ import annotations
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # Database settings
    # app
    app_env: str = "dev"

    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    # jwt settings
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440  # 24 hours

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def database_url(self) -> str:
        user = quote_plus(self.db_user)
        pwd = quote_plus(self.db_password)
        name = quote_plus(self.db_name)
        return f"mysql+pymysql://{user}:{pwd}@{self.db_host}:{self.db_port}/{name}?charset=utf8mb4"

settings = Settings()