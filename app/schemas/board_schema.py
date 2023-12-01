# built-in
from typing import List
# third-party
from pydantic import BaseModel
# Fast-api
from app.schemas.post_schema import PostResponseSchema


class BoardRequestSchema(BaseModel):
    name: str
    public: bool
    user_id: int


class BoardResponseSchema(BoardRequestSchema):
    id: int
    name: str
    public: bool
    user_id: int
    posts: List[PostResponseSchema] = []

    class Config:
        orm_mode = True
