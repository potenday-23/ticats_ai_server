# third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-api
from app.config.database_config import get_db
from app.schemas.user_schema import UserResponseSchema
from app.schemas.user_schema import UserRequestSchema
from app.services import user_service

router = APIRouter(
    prefix="/api/users",
)


@router.post("", response_model=UserResponseSchema)
def create_user(user: UserRequestSchema, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

