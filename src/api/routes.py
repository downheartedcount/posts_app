import logging
from fastapi import HTTPException
from typing import Optional
from fastapi import APIRouter
from src.client.posts_client import PostsClient
from src.exceptions import AppException
from src.models.models import PostRequest
from src.models.schemas import PostOut

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/posts", response_model=list[PostOut])
async def get_posts(
    user_id: Optional[int] = None,
    title: Optional[str] = None,
    username: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    post_request = PostRequest(
        user_id=user_id,
        title=title,
        username=username,
        skip=skip,
        limit=limit
    )

    try:
        service = PostsClient()
        posts = await service.get_posts(post_request)
        if not posts:
            raise HTTPException(status_code=404, detail="Posts Not Found")
        return posts

    except AppException:
        logger.exception("Data fetch failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")