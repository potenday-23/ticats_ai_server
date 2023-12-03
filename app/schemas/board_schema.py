# built-in
from datetime import datetime
from typing import List
# third-party
from pydantic import BaseModel
# Fast-app
from app.schemas.post_schema import PostResponseSchema


class BoardRequestSchema(BaseModel):
    name: str
    public: bool


class BoardResponseSchema(BoardRequestSchema):
    id: int
    name: str
    public: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    posts: List[PostResponseSchema] = []

    class Config:
        orm_mode = True
