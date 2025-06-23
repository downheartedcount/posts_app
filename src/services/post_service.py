from abc import abstractmethod, ABC
from typing import List, Dict
from httpx import HTTPError
from src.exceptions import FetchError
from src.utils.http_client import HTTPClient, logger


class BasePostServive(ABC):

    @abstractmethod
    async def _fetch_users(self) -> List[Dict]:
        raise NotImplementedError

    @abstractmethod
    async def _fetch_posts(self) -> List[Dict]:
        raise NotImplementedError


class PostService(BasePostServive):
    def __init__(self):
        self.http = HTTPClient()

    async def _fetch_users(self) -> List[Dict]:
        logger.info("Fetching users from /users...")
        await self.http.startup()
        try:
            data = await self.http.get("/users")
            logger.info(f"Fetched {len(data)} users")
            return data
        except HTTPError as e:
            logger.error(f"Failed to fetch users: {e}")
            raise FetchError("Unable to fetch users") from e

    async def _fetch_posts(self) -> List[Dict]:
        logger.info("Fetching posts from /posts...")
        await self.http.startup()
        try:
            data = await self.http.get("/posts")
            logger.info(f"Fetched {len(data)} posts")
            return data
        except HTTPError as e:
            logger.error(f"Failed to fetch posts: {e}")
            raise FetchError("Unable to fetch posts") from e
