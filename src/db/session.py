from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.configs.db_config import get_db_config

db_config = get_db_config()

engine = create_async_engine(
    str(db_config.DATABASE_URL),
    echo=db_config.SQLALCHEMY_ECHO
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session

Base = declarative_base()
