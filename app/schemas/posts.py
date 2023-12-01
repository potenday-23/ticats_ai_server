# built-in
from typing import List, Union
# third-party
from pydantic import BaseModel, EmailStr


class PostRequestSchema(BaseModel):
    title: str
    content: str
    user_id: int
    board_id: int


class PostResponseSchema(PostRequestSchema):
    id: int
    title: str
    content: str
    user_id: int
    board_id: int

    class Config:
        orm_mode = True
