import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_url: str = "sqlite:///geomatrix_db.db" #default database set to sqlite
    pool_size: int = 10

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    BASE_URL: str = "http://127.0.0.1:8000/api/v1"

    # load envs from .env
    model_config = SettingsConfigDict(env_file=".env")


    


# get db settings from cache if available else load
@lru_cache
def get_settings():
    return Settings()
