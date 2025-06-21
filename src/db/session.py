from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.SQLALCHEMY_ECHO
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session
