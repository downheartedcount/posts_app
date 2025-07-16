from typing import List, Dict
from src.client.base import BaseClient
from src.exceptions import FetchError, DatabaseError
from src.models.models import PostRequest
from src.services.post_service import PostService
from src.db.session import SessionLocal
from src.db.repo import PostRepo
from src.utils.http_client import HTTPClient
import logging

logger = logging.getLogger(__name__)


class PostsClient(BaseClient):

    def __init__(self):
        self.db = SessionLocal()
        self.repo = PostRepo(self.db)
        self.http = HTTPClient(timeout=10)
        self.post = PostService()

    async def fetch_users(self) -> List[Dict]:
        try:
            return await self.post.fetch_users()
        except Exception as e:
            logger.exception("Failed to fetch users")
            raise FetchError("Fetching users failed") from e

    async def fetch_posts(self) -> List[Dict]:
        try:
            return await self.post.fetch_posts()
        except Exception as e:
            logger.exception("Failed to fetch posts")
            raise FetchError("Fetching posts failed") from e

    async def get_posts(self, post_request: PostRequest):
        try:
            posts = await self.repo.get_posts(post_request)
        except Exception as e:
            logger.exception("Failed to fetch posts")
            raise DatabaseError('Failed to fetch posts from database') from e
        return posts
