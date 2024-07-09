from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import URLType

Base = declarative_base()

class CulturalEvent(Base):
    __tablename__ = "cultural_event"
    __table_args__ = (Index('idx_title', 'title'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    thumbnail_image_url = Column(URLType)
    start_date = Column(Date)
    end_date = Column(Date)
    ticket_open_date = Column(DateTime)
    running_time = Column(String)
    summary = Column(Text)
    genre = Column(String)
    view_rate_name = Column(String)
    like_count = Column(Integer, default=0)
    visit_count = Column(Integer, default=0)
    point = Column(Integer, default=0)
    information = Column(Text)
    topic = Column(Text)
    sentiment = Column(Text)