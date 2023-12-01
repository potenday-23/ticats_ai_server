# Fast-API
from app.core.db.base import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    # Table Name
    __tablename__ = "user"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)

    # FK
    boards = relationship("Board", back_populates="user")
    posts = relationship("Post", back_populates="user")


class Board(Base):
    # Table Name
    __tablename__ = "board"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    public = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # FK
    user = relationship("User", back_populates="boards")
    posts = relationship("Post", back_populates="board")


class Post(Base):
    # Table Name
    __tablename__ = "post"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    board_id = Column(Integer, ForeignKey("board.id"))

    # FK
    user = relationship("User", back_populates="posts")
    board = relationship("Board", back_populates="posts")
