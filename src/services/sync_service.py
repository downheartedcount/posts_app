import logging
from abc import abstractmethod, ABC
from httpx import HTTPError
from sqlalchemy.exc import SQLAlchemyError
from src.client.posts_client import PostsClient

logger = logging.getLogger(__name__)


class BaseSyncService(ABC):

    @abstractmethod
    async def sync_all(self):
        raise NotImplementedError


class SyncService(BaseSyncService):
    def __init__(self):
        self.posts_client = PostsClient()

    async def sync_all(self):
        logger.info("Starting sync process...")

        try:
            users = await self.posts_client.fetch_users()
            logger.info(f"Fetched {len(users)} users.")
            await self.posts_client.repo.save_users(users)
            logger.info("Users saved successfully.")
        except HTTPError as e:
            logger.error(f"HTTP error during users fetch: {e}", exc_info=True)
        except SQLAlchemyError as e:
            logger.error(f"Database error saving users: {e}", exc_info=True)
            await self.posts_client.repo.session.rollback()

        try:
            posts = await self.posts_client.fetch_posts()
            logger.info(f"Fetched {len(posts)} posts.")
            await self.posts_client.repo.save_posts(posts)
            logger.info("Posts saved successfully.")
        except HTTPError as e:
            logger.error(f"HTTP error during posts fetch: {e}", exc_info=True)
        except SQLAlchemyError as e:
            logger.error(f"Database error saving posts: {e}", exc_info=True)
            await self.posts_client.repo.session.rollback()

        logger.info("Sync process finished.")
