# app/core/config.py
from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    database_uri: PostgresDsn

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
