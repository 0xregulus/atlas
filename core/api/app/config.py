from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Atlas Core API"
    environment: str = "local"
    default_tenant: str = "demo"
    allow_origins: list[str] = ["*"]
    database_url: str = "sqlite:///./atlas.db"
    auth_secret: str = "atlas-secret"
    auth_access_token_minutes: int = 60
    auth_algorithm: str = "HS256"
    auth_username: str = "admin@atlas"
    auth_password: str = "atlas"
    stripe_webhook_secret: str = "whsec_demo"
    otlp_endpoint: str | None = None

    class Config:
        env_prefix = "ATLAS_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
