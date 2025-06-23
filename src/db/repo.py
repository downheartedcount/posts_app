import logging
from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from src.db.base import BaseRepo
from src.models.models import PostRequest
from src.models.db_models import User, Post
from src.exceptions import DatabaseError
from datetime import datetime


logger = logging.getLogger(__name__)


class PostRepo(BaseRepo):
    def __init__(self, session):
        self.session = session

    async def save_users(self, users: List[Dict]):
        try:
            user_ids = [u["id"] for u in users]
            existing = await self.session.execute(
                select(User.id).where(User.id.in_(user_ids))
            )
            existing_ids = {u[0] for u in existing.all()}

            new_users = [
                User(
                    id=u["id"],
                    name=u["name"],
                    username=u["username"],
                    email=u["email"],
                    created_at=datetime.now()
                )
                for u in users if u["id"] not in existing_ids
            ]

            self.session.add_all(new_users)
            await self.session.commit()

            logger.info(f"Added {len(new_users)} new users.")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error saving users: {e}")
            raise DatabaseError("Failed to save users") from e

    async def save_posts(self, posts: List[Dict]):
        try:
            post_ids = [p["id"] for p in posts]
            existing = await self.session.execute(
                select(Post.id).where(Post.id.in_(post_ids))
            )
            existing_ids = {p[0] for p in existing.all()}

            new_posts = [
                Post(
                    id=p["id"],
                    user_id=p["userId"],
                    title=p["title"],
                    body=p["body"],
                    created_at=datetime.now()
                )
                for p in posts if p["id"] not in existing_ids
            ]

            self.session.add_all(new_posts)
            await self.session.commit()

            logger.info(f"Added {len(new_posts)} new posts.")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error saving posts: {e}")
            raise DatabaseError("Failed to save posts") from e

    async def get_posts(self, post_request: PostRequest):
        try:
            query = select(Post).options(joinedload(Post.user))

            if post_request.user_id is not None:
                query = query.where(Post.user_id == post_request.user_id)

            if post_request.title is not None:
                query = query.where(
                    Post.title.ilike(f"%{post_request.title}%")
                )

            if post_request.username is not None:
                query = query.where(
                    Post.user.has(username=post_request.username)
                )

            query = query.offset(post_request.skip).limit(post_request.limit)

            result = await self.session.execute(query)
            posts = result.scalars().all()
            logger.info(f"Fetched {len(posts)} posts with filters: "
                        f"{post_request.dict()}"
                        )
            return posts

        except SQLAlchemyError as e:
            logger.error(f"Error fetching posts: {e}")
            raise DatabaseError("Failed to fetch posts") from e
