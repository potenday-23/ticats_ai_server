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


@router.post("/signup", response_model=UserResponseSchema, summary="계정 Signup",
             description="- 서비스 내 email은 중복될 수 없습니다.\n - email, password, full_name은 공백으로 설정할 수 없습니다.")
def create_user(user: UserSignupRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)


@router.post("/login", status_code=204, summary="계정 Login",
             description="- email, password, full_name은 공백으로 설정할 수 없습니다.")
def login_user(user: UserLoginRequestSchema, db: Session = Depends(get_db), response: Response = Response):
    access_token = user_service.login_user(db=db, user=user)
    response.set_cookie(key="AccessToken", value=access_token, expires=14)
    response.headers["AccessToken"] = access_token


@router.post("/logout", status_code=204, summary="AccessToken으로 로그아웃하기",
             description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.")
def logout_user(db: Session = Depends(get_db), authorization: str = Depends(AuthProvider())):
    logout_by_access_token(db=db, access_token=authorization)
