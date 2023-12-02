from typing import Optional

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "e068f0399d3729db42eafdc56ca258ff3954c38a24ac423a6d5b15005378785c"  # todo : 새로 생성하고, 환경변수로 분리할 것
ALGORITHM = "HS256"


def create_access_token(session_id: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": session_id}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return "Baerer " + jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
