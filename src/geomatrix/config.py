import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    db_url: str = "sqlite:///geomatrix_db.db" #default database set to sqlite
    pool_size: int = 10

    # load envs from .env
    model_config = SettingsConfigDict(env_file=".env")


class JWTSettings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# get db settings from cache if available else load
@lru_cache
def get_db_settings():
    return DatabaseSettings()


def get_jwt_settings():
    return JWTSettings()