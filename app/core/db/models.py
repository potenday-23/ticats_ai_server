# Fast-API
from app.core.db.base import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    # Table Name
    __tablename__ = "users"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)

    # FK
    boards = relationship("Board", back_populates="user")


class Board(Base):
    # Table Name
    __tablename__ = "boards"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    public = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # FK
    user = relationship("User", back_populates="boards")
