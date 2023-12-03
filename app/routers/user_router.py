# third-party
from fastapi import APIRouter, Depends, HTTPException, Response, Request, Header
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.user_schema import UserResponseSchema, UserSignupRequestSchema, UserLoginRequestSchema
from app.services import user_service
from app.services.jwt_service import AuthProvider
from app.services.user_service import get_user_by_access_token, logout_by_access_token

router = APIRouter(
    prefix="/api/users",
    tags=["계정 API"],
)


@router.post("/signup", response_model=UserResponseSchema, summary="계정 Signup")
def create_user(user: UserSignupRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)


@router.post("/login", summary="계정 Login", status_code=204)
def login_user(user: UserLoginRequestSchema, db: Session = Depends(get_db), response: Response = Response):
    access_token = user_service.login_user(db=db, user=user)
    response.set_cookie(key="AccessToken", value=access_token, expires=14)
    response.headers["AccessToken"] = access_token


@router.get("", response_model=UserResponseSchema, summary="AccessToken으로 사용자 찾기")
def get_user(db: Session = Depends(get_db), authorization: str = Depends(AuthProvider())):
    return get_user_by_access_token(db=db, access_token=authorization)


@router.post("/logout", summary="AccessToken으로 로그아웃하기", status_code=204)
def logout_user(db: Session = Depends(get_db), authorization: str = Depends(AuthProvider())):
    logout_by_access_token(db=db, access_token=authorization)
