# third-party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import redis

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin1234@postgres:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

redis_client = redis.Redis(host="localhost", port=6379)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
