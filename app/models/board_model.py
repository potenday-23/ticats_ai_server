# built-in
from datetime import datetime
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, and_, or_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
# fast-api
from app.config.config import Base


class Board(Base):
    # Table Name
    __tablename__ = "boards"

    # Column
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    public = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # created_at & updated_at
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    # FK
    user = relationship("User", back_populates="boards")
    posts = relationship("Post", back_populates="board")

    @hybrid_property
    def post_count(self) -> int:
        return int(self.posts.count)
