from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
