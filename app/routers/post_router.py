# third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.post_schema import PostResponseSchema
from app.schemas.post_schema import PostRequestSchema
from app.services import post_service
from app.services.jwt_service import UserIdProvider

router = APIRouter(
    prefix="/api/posts",
    tags=["게시글 API"],
)


@router.post("", response_model=PostResponseSchema, summary="게시글 Create")
def create_post(post: PostRequestSchema, db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider())):
    return post_service.create_post(db=db, post=post, user_id=user_id)


@router.put("", response_model=PostResponseSchema, summary="게시글 Create")
def create_post(post: PostRequestSchema, db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider())):
    return post_service.create_post(db=db, post=post, user_id=user_id)
