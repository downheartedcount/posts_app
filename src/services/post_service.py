from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.models.db_models import Post

class PostService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_posts(
        self,
        user_id: Optional[int] = None,
        title: Optional[str] = None,
        username: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = select(Post).options(joinedload(Post.user))

        if user_id is not None:
            query = query.where(Post.user_id == user_id)

        if title is not None:
            query = query.where(Post.title.ilike(f"%{title}%"))

        if username is not None:
            query = query.where(Post.user.has(username=username))

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()
