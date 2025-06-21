from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.utils.dependencies import get_sync_service
from src.api.routes import router
from src.utils.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with get_sync_service() as sync_service:
            await sync_service.sync_all()
            start_scheduler(sync_service)
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Application startup failed", e)
        raise
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
