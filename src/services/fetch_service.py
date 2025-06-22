import logging
from typing import List, Dict
from httpx import HTTPError
from src.exceptions import FetchError

logger = logging.getLogger(__name__)


class FetchService:
    def __init__(self, client):
        self.client = client

    async def _fetch_users(self) -> List[Dict]:
        logger.info("Fetching users from /users...")
        try:
            data = await self.client.get("/users")
            logger.info(f"Fetched {len(data)} users")
            return data
        except HTTPError as e:
            logger.error(f"Failed to fetch users: {e}")
            raise FetchError("Unable to fetch users") from e

    async def _fetch_posts(self) -> List[Dict]:
        logger.info("Fetching posts from /posts...")
        try:
            data = await self.client.get("/posts")
            logger.info(f"Fetched {len(data)} posts")
            return data
        except HTTPError as e:
            logger.error(f"Failed to fetch posts: {e}")
            raise FetchError("Unable to fetch posts") from e

    async def fetch_users(self) -> List[Dict]:
        return await self._fetch_users()

    async def fetch_posts(self) -> List[Dict]:
        return await self._fetch_posts()