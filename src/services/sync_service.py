import logging

logger = logging.getLogger(__name__)


class SyncService:
    def __init__(self, fetch_service, db_service):
        self.fetch_service = fetch_service
        self.db_service = db_service

    async def sync_all(self):
        logger.info("Starting sync process...")

        try:
            users = await self.fetch_service.fetch_users()
            logger.info(f"Fetched {len(users)} users.")
            await self.db_service.save_users(users)
            logger.info("Users saved successfully.")
        except Exception as e:
            logger.error(f"Failed to sync users: {e}")
        try:
            posts = await self.fetch_service.fetch_posts()
            logger.info(f"Fetched {len(posts)} posts.")
            await self.db_service.save_posts(posts)
            logger.info("Posts saved successfully.")
        except Exception as e:
            logger.error(f"Failed to sync posts: {e}")

        logger.info("Sync process finished.")
