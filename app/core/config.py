# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator

class Settings(BaseSettings):
    # from env file 
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_pass: str
    batch_size: int = 1000
    csv_path: str = "./data"

    # use a db uri string
    database_uri: PostgresDsn | None = None

    # model config
    model_config = SettingsConfigDict(
        env_file=".env",          # .env file read
        env_prefix="",
        extra="ignore",
    )

    # ensamblar la URI si no la pasaron completa
    @field_validator("database_uri", mode="before")
    def assemble_db_uri(cls, v, info):
        if v:
            return v
        data = info.data
        return (
            f"postgresql+psycopg2://{data['db_user']}:{data['db_pass']}"
            f"@{data['db_host']}:{data['db_port']}/{data['db_name']}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()
