# built-in
from typing import Optional
from datetime import datetime, timedelta
# third-party
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Request
# fast-api
from app.config.exceptions import ApiException, ExceptionCode
from app.services.redis_service import get_session_from_redis_key

SECRET_KEY = "e068f0399d3729db42eafdc56ca258ff3954c38a24ac423a6d5b15005378785c"  # todo : 새로 생성하고, 환경변수로 분리할 것
ALGORITHM = "HS256"


class AuthProvider:
    async def __call__(self, req: Request):
        authorization: str = req.headers.get('authorization')
        # authorization 토큰 없을 때
        if not authorization:
            raise ApiException(exception_code=ExceptionCode.AUTHORIZATION_EMPTY)
        # "Baerer"형식이 아닐 때
        if authorization[:8] is not "Baerer ":
            raise ApiException(exception_code=ExceptionCode.TOKEN_NOT_VALID)
        return authorization


def create_access_token(session_id: str, expires_delta: Optional[timedelta] = None) -> str:
    encode = {"sub": session_id}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return "Baerer " + jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_sub_from_access_token(access_token: str) -> str:
    try:
        # redis_key 추출
        payload = jwt.decode(access_token.replace("Baerer ", ""), SECRET_KEY, algorithms=[ALGORITHM])
        redis_key = payload.get("sub")
        if redis_key is None:
            raise JWTError()
        return redis_key
    # 유효기한 만료
    except ExpiredSignatureError:
        raise ApiException(exception_code=ExceptionCode.TOKEN_EXPIRED)
    # 그 외
    except JWTError:
        raise ApiException(exception_code=ExceptionCode.TOKEN_NOT_VALID)


def get_user_id(access_token: str) -> int:
    # redis_key 추출
    redis_key = get_sub_from_access_token(access_token)

    # session 추출
    session = get_session_from_redis_key(redis_key)

    return int(session["userId"])
