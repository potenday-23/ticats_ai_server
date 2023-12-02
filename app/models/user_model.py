# built-in
from datetime import datetime
# fast-api
from app.config.database import Base
# third-party
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    # Table Name
    __tablename__ = "users"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)

    # created_at & updated_at
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())  # todo : Patch또는 Put사에 변경되는 로직 추가

    # FK
    boards = relationship("Board", back_populates="user")
    posts = relationship("Post", back_populates="user")
