# third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-api
from app.config.database_config import get_db
from app.schemas.post_schema import PostResponseSchema
from app.schemas.post_schema import PostRequestSchema
from app.services import post_service

router = APIRouter(
    prefix="/api/posts",
    tags=["게시글 API"],
)


@router.post("", response_model=PostResponseSchema, summary="게시글 Create")
def create_post(post: PostRequestSchema, db: Session = Depends(get_db)):
    return post_service.create_post(db=db, post=post)

