from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    user: UserOut
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
