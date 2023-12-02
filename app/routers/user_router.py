# third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-app
from app.config.database_config import get_db
from app.schemas.user_schema import UserResponseSchema
from app.schemas.user_schema import UserRequestSchema
from app.services import user_service

router = APIRouter(
    prefix="/app/users",
    tags=["계정 API"],
)


@router.post("/sign-up", response_model=UserResponseSchema, summary="계정 Sign Up")
def create_user(user: UserRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)

