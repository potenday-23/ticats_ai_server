# Fast-API
from app.config.database import Base
# third-party
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.posts import Post
from app.models.users import User
from app.models.boards import Board