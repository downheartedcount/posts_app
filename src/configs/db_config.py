import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    DB_HOST: str = os.environ['DB_HOST']
    DB_PORT: int = os.environ['DB_PORT']
    DB_NAME: str = os.environ['DB_NAME']
    DB_USER: str = os.environ['DB_USER']
    DB_PASSWORD: str = os.environ['DB_PASSWORD']
    SQLALCHEMY_ECHO: bool = os.environ['SQLALCHEMY_ECHO']

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_db_config():
    return DBConfig()
