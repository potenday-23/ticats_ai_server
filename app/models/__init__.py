# Fast-API
from app.config.database_config import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.post_model import Post
from app.models.user_model import User
from app.models.board_model import Board