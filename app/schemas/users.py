# built-in
from typing import List
# third-party
from pydantic import BaseModel, EmailStr
# Fast-api
from app.schemas.boards import BoardResponseSchema
from app.schemas.posts import PostResponseSchema


class UserRequestSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserResponseSchema(UserRequestSchema):
    id: int
    email: str
    password: str
    full_name: str
    boards: List[BoardResponseSchema] = []
    posts: List[PostResponseSchema] = []

    class Config:
        orm_mode = True
