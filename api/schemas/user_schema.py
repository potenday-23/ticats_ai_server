# built-in
from typing import List
# third-party
from pydantic import BaseModel, EmailStr
# Fast-api
from api.schemas.board_schema import BoardResponseSchema
from api.schemas.post_schema import PostResponseSchema


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
