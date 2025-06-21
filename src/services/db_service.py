import logging
from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from src.models.db_models import User, Post

logger = logging.getLogger(__name__)


class DBService:
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
                    email=u["email"]
                )
                for u in users if u["id"] not in existing_ids
            ]

            self.session.add_all(new_users)
            await self.session.commit()

            logger.info(f"Added {len(new_users)} new users.")

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error saving users: {e}")
            raise

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
                    body=p["body"]
                )
                for p in posts if p["id"] not in existing_ids
            ]

            self.session.add_all(new_posts)
            await self.session.commit()

            logger.info(f"Added {len(new_posts)} new posts.")

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error saving posts: {e}")
            raise
