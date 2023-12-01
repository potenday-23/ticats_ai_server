# built-in
from typing import List, Union
# third-party
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    board_id: int


class Post(PostBase):
    id: int
    title: str
    content: str
    user_id: int
    board_id: int

    class Config:
        orm_mode = True


class BoardBase(BaseModel):
    name: str
    public: bool
    user_id: int


class Board(BoardBase):
    id: int
    name: str
    public: bool
    user_id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class User(UserBase):
    id: int
    email: str
    password: str
    full_name: str
    boards: List[Board] = []
    posts: List[Post] = []

    class Config:
        orm_mode = True
