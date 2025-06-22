from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.utils.dependencies import get_sync_service
from src.api.routes import router
from src.utils.scheduler import start_scheduler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


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


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app

app = create_app()


def main():
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()