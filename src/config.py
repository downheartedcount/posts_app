import os
from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings

secret_path = "/run/secrets/database_url"
if os.path.exists(secret_path):
    with open(secret_path) as f:
        os.environ["DATABASE_URL"] = f.read().strip()

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SQLALCHEMY_ECHO: bool = False
    BASE_URL: AnyHttpUrl = "https://jsonplaceholder.typicode.com"
    SYNC_INTERVAL_HOURS: int = 24

    class Config:
        env_file = "../.env"

settings = Settings()
