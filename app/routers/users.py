# third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-api
from app.config.database import get_db
from app.models import users as user_model
from app.schemas.users import UserResponseSchema
from app.schemas.users import UserRequestSchema
from app.services import users as user_service

router = APIRouter(
    prefix="/api/users",
)


@router.post("", response_model=UserResponseSchema)
def create_user(user: UserRequestSchema, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

