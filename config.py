import os

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    MONGO_URI: str = Field(..., env='MONGO_URL')

    class Config:
        env_file = os.getenv('ENV_FILE')
        env_file_encoding = "utf-8"


@lru_cache()
def cached_settings():
    return Settings()


settings = cached_settings()
