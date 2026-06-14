from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int] = [277236314]
    DATABASE_URL: str
    REDIS_URL: str
    ADMIN_API_KEY: str
    ADMIN_HOST: str = "0.0.0.0"
    ADMIN_PORT: int = 8000
    ELO_INITIAL: int = 1500
    CONFIDENCE_THRESHOLD: float = 0.6
    MIN_MATCH_DATA: int = 10
    CACHE_TTL: int = 3600
    LIVE_CACHE_TTL: int = 60
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/foti.log"
    RATE_LIMIT: int = 60
    RATE_LIMIT_WINDOW: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
