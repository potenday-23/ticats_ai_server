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

config = Config(".env")
SECRET_KEY = config("SECRET_KEY")

Base = declarative_base()
