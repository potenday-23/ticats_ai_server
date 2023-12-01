# Fast-API
from app.config.database import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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

    # FK
    user = relationship("User", back_populates="posts")
    board = relationship("Board", back_populates="posts")
