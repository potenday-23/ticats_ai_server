# built-in
from datetime import datetime
from typing import List
# third-party
from pydantic import BaseModel, EmailStr
# Fast-app
from app.schemas.board_schema import BoardResponseSchema
from app.schemas.post_schema import PostResponseSchema


class UserSignupRequestSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: str
    password: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    boards: List[BoardResponseSchema] = []
    posts: List[PostResponseSchema] = []

    class Config:
        orm_mode = True
