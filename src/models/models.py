from pydantic import BaseModel, Field
from typing import Optional


class PostRequest(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    username: Optional[str] = None
    limit: Optional[int] = Field(default=100, le=100)
    skip: Optional[int] = 0
