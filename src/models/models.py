from pydantic import BaseModel
from typing import Optional


class PostRequest(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    username: Optional[str] = None
    limit: Optional[int] = 100
    skip: Optional[int] = 0
