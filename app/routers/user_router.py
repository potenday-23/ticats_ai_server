# third-party
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.user_schema import UserResponseSchema, UserSignupRequestSchema, UserLoginRequestSchema
from app.services import user_service

router = APIRouter(
    prefix="/app/users",
    tags=["계정 API"],
)


@router.post("/signup", response_model=UserResponseSchema, summary="계정 Signup")
def create_user(user: UserSignupRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)


@router.post("/login", summary="계정 Login")
def login_user(user: UserLoginRequestSchema, db: Session = Depends(get_db), response: Response = Response()):
    access_token = user_service.login_user(db=db, user=user)
    response.set_cookie(key="AccessToken", value=access_token)
    response.headers["AccessToken"] = access_token
    return None
