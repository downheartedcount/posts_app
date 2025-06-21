from contextlib import asynccontextmanager

from src.config import settings
from src.client.http_client import HTTPClient
from src.services.fetch_service import FetchService
from src.services.db_service import DBService
from src.services.sync_service import SyncService
from src.db.session import get_session


@asynccontextmanager
async def get_sync_service():
    client = HTTPClient(str(settings.BASE_URL))
    await client.startup()

    try:
        fetch = FetchService(client)

        session_gen = get_session()
        session = await anext(session_gen)

        db = DBService(session)
        sync_service = SyncService(fetch, db)
        yield sync_service
    finally:
        await client.shutdown()
