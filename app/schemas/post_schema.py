# third-party
from datetime import datetime

from pydantic import BaseModel


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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
