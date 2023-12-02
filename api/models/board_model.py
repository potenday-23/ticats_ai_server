# Fast-API
from api.config.database_config import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


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
    posts = relationship("Post", back_populates="board")
