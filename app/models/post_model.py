# built-in
from datetime import datetime
# fast-api
from app.config.database import Base
# third-party
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Post(Base):
    # Table Name
    __tablename__ = "posts"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    board_id = Column(Integer, ForeignKey("boards.id"))

    # created_at & updated_at
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())  # todo : Patch또는 Put사에 변경되는 로직 추가

    # FK
    user = relationship("User", back_populates="posts")
    board = relationship("Board", back_populates="posts")
