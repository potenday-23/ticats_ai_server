# built-in
from datetime import datetime
from typing import List
# third-party
from pydantic import BaseModel, EmailStr, field_validator
# Fast-app
from app.config.exceptions import ApiException, ExceptionCode
from app.schemas.board_schema import BoardResponseSchema
from app.schemas.post_schema import PostResponseSchema


class UserSignupRequestSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator('password', 'full_name')
    @classmethod
    def name_must_not_contain_space(cls, v: str) -> str:
        if v.replace(" ", "") == "":
            raise ApiException(exception_code=ExceptionCode.VALIDATION_NOT_BLANK)
        return v.title()

    @field_validator('email')
    @classmethod
    def email_to_lower_case(cls, v: str) -> str:
        return v.lower()


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def name_must_not_contain_space(cls, v: str) -> str:
        if v.replace(" ", "") == "":
            raise ApiException(exception_code=ExceptionCode.VALIDATION_NOT_BLANK)
        return v.title()

    @field_validator('email')
    @classmethod
    def email_to_lower_case(cls, v: str) -> str:
        return v.lower()


class UserResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    boards: List[BoardResponseSchema] = []
    posts: List[PostResponseSchema] = []

    class Config:
        orm_mode = True
