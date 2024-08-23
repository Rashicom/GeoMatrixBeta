import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_url: str = "sqlite:///geomatrix_db.db" #default database set to sqlite
    pool_size: int = 10

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAIL_USERNAME: str ="rashid.kp484@gmail.com"
    MAIL_PASSWORD: str = "wpvm boxm bnud zthk"
    MAIL_FROM: str = "rashid.kp484@gmail.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.gmail.com"

    # load envs from .env
    model_config = SettingsConfigDict(env_file=".env")



# get db settings from cache if available else load
@lru_cache
def get_settings():
    return Settings()
