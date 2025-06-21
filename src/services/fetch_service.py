import logging
from typing import List, Dict
from httpx import HTTPError
from src.exceptions import FetchError

logger = logging.getLogger(__name__)


class FetchService:
    def __init__(self, client):
        self.client = client

    async def _fetch(self, endpoint: str, entity_name: str) -> List[Dict]:
        try:
            logger.info(f"Fetching {entity_name} from {endpoint}...")
            data = await self.client.get(endpoint)
            logger.info(f"Fetched {len(data)} {entity_name}")
            return data
        except HTTPError as e:
            logger.error(f"Failed to fetch {entity_name}: {e}")
            raise FetchError(f"Unable to fetch {entity_name}") from e

    async def fetch_users(self) -> List[Dict]:
        return await self._fetch("/users", "users")

    async def fetch_posts(self) -> List[Dict]:
        return await self._fetch("/posts", "posts")
