from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from src.db.session import get_session
from src.models.db_models import Post, User
from src.models.schemas import PostOut

router = APIRouter()


@router.get("/posts", response_model=list[PostOut])
async def get_posts(
    session: AsyncSession = Depends(get_session),
    user_id: Optional[int] = Query(None),
    username: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    min_id: Optional[int] = Query(None),
    max_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    query = select(Post).options(joinedload(Post.user))

    if username:
        query = query.join(Post.user)

    filter_conditions = {
        "user_id": Post.user_id == user_id if user_id else None,
        "username": User.username == username if username else None,
        "title": Post.title.ilike(f"%{title}%") if title else None,
        "min_id": Post.id >= min_id if min_id is not None else None,
        "max_id": Post.id <= max_id if max_id is not None else None,
    }

    filters = [condition
               for condition in filter_conditions.values()
               if condition is not None
               ]

    if filters:
        query = query.where(and_(*filters))

    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    return result.scalars().all()
