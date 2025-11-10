"""Settings for Atlas AI services."""

from functools import lru_cache
from typing import Literal

from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    core_api_url: HttpUrl | str = "http://localhost:8000"
    core_api_token: str | None = None
    default_tenant: str = "demo"
    vector_collection: str = "knowledge_base"
    enable_semantic_cache: bool = True
    evaluation_mode: Literal["fast", "strict"] = "fast"
    otlp_endpoint: str | None = None

    class Config:
        env_prefix = "ATLAS_AI_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
