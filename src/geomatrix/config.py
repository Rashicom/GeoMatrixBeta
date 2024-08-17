import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    db_url: str = "sqlite:///geomatrix_db.db" #default database set to sqlite
    pool_size: int = 10

    # load envs from .env
    model_config = SettingsConfigDict(env_file=".env")



# get db settings from cache if available else load
@lru_cache
def get_db_settings():
    return DatabaseSettings()