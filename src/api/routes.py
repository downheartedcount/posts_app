from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.models.schemas import PostOut
from src.services.post_service import PostService

router = APIRouter()

@router.get("/posts", response_model=list[PostOut])
async def get_posts(
    user_id: Optional[int] = None,
    title: Optional[str] = None,
    username: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    service = PostService(session)
    return await service.get_posts(
        user_id=user_id,
        title=title,
        username=username,
        skip=skip,
        limit=limit,
    )
