# built-in
from datetime import datetime
from typing import List
# third-party
from pydantic import BaseModel, field_validator
# Fast-app
from app.config.exceptions import ApiException, ExceptionCode
from app.schemas.post_schema import PostResponseSchema


class BoardRequestSchema(BaseModel):
    name: str
    public: bool

    @field_validator('name')
    @classmethod
    def name_must_not_contain_space(cls, v: str) -> str:
        if v.replace(" ", "") == "":
            raise ApiException(exception_code=ExceptionCode.VALIDATION_NOT_BLANK)
        return v.title()


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
