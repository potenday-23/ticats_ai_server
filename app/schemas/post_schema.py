# third-party
from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator

from app.config.exceptions import ApiException, ExceptionCode
from app.schemas.common_schema import PageInfo


class PostUpdateRequestSchema(BaseModel):
    title: str
    content: str

    @field_validator('title', 'content')
    @classmethod
    def name_must_not_contain_space(cls, v: str) -> str:
        if v.replace(" ", "") == "":
            raise ApiException(exception_code=ExceptionCode.VALIDATION_NOT_BLANK)
        return v.title()


class PostRequestSchema(PostUpdateRequestSchema):
    title: str
    content: str
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


class PostResponseListSchema(BaseModel):
    post_list: List[PostResponseSchema] = []
    page_info: PageInfo
