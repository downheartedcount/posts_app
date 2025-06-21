from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = \
        "postgresql+asyncpg://postgres:1234@localhost:5432/json_app"
    SQLALCHEMY_ECHO: bool = False
    BASE_URL: AnyHttpUrl = "https://jsonplaceholder.typicode.com"
    SYNC_INTERVAL_HOURS: int = 24

    class Config:
        env_file = "../.env"


settings = Settings()

try:
    with open("/run/secrets/database_url") as f:
        settings.DATABASE_URL = f.read().strip()
except FileNotFoundError:
    raise Exception("Database URL not found")