from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.configs.app_config import get_app_config
from src.scheduler.schedule import start_scheduler
from src.services.sync_service import SyncService
from src.api.routes import router
import logging
from src.utils.http_client import HTTPClient

app_config = get_app_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with get_sync_service() as sync_service:
            await sync_service.sync_all()
            start_scheduler(sync_service)
    except Exception as e:
        logging.exception("Application startup failed", e)
        raise
    yield


@asynccontextmanager
async def get_sync_service():
    client = HTTPClient(str(app_config.BASE_URL))
    await client.startup()

    try:
        sync_service = SyncService()
        yield sync_service
    finally:
        await client.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()


def main():
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=app_config.APP_HOST,
        port=app_config.APP_PORT,
        reload=True
    )


if __name__ == "__main__":
    main()
