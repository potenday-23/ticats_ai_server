# built-in
from datetime import datetime
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
# fast-app
from app.config.database import Base


class Board(Base):
    # Table Name
    __tablename__ = "boards"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    public = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # created_at & updated_at
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())  # todo : Patch또는 Put사에 변경되는 로직 추가

    # FK
    user = relationship("User", back_populates="boards")
    posts = relationship("Post", back_populates="board")
