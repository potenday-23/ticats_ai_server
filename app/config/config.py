# built-in
import os
# third-party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import redis
from starlette.config import Config
from dotenv import load_dotenv

load_dotenv()

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')
SECRET_KEY = config('SECRET_KEY')

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
