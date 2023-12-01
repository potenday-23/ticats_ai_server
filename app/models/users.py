# Fast-API
from app.config.database import Base
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
    posts = relationship("Post", back_populates="user")
