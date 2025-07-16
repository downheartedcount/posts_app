import os
from typing import List

from pydantic import AnyHttpUrl, Field
from functools import lru_cache
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_NAME: str = os.environ['APP_NAME']
    APP_HOST: str = os.environ['APP_HOST']
    APP_PORT: int = os.environ['APP_PORT']

    BASE_URL: AnyHttpUrl = os.environ['BASE_URL']
    HTTP_TIMEOUT: int = 10
    CORS_ORIGINS: List[str] = os.environ['CORS_ORIGINS'].split(',')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = 'ignore'


@lru_cache
def get_app_config():
    return AppConfig()
