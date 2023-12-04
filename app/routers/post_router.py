# third-party
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.post_schema import PostResponseSchema, PostUpdateRequestSchema, PostResponseListSchema
from app.schemas.post_schema import PostRequestSchema
from app.services import post_service
from app.services.jwt_service import UserIdProvider

router = APIRouter(
    prefix="/api/posts",
    tags=["게시글 API"],
)


@router.post("", response_model=PostResponseSchema, summary="게시글 Create",
             description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판 또는 전체공개 게시판(public=true)에만 게시글을 작성할 수 있습니다.\n- title, content, board_id는 필수로 입력해야하는 값입니다.")
def create_post(post: PostRequestSchema, db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider())):
    return post_service.create_post(db=db, post=post, user_id=user_id)


@router.put("/{post_id}", response_model=PostResponseSchema, summary="게시글 Update",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시글만 수정할 수 있습니다.\n- title, content, board_id는 필수로 입력해야하는 값입니다.")
def update_post(post: PostUpdateRequestSchema, db: Session = Depends(get_db), post_id: int = None,
                user_id: int = Depends(UserIdProvider())):
    return post_service.update_post(db=db, post=post, post_id=post_id, user_id=user_id)


@router.delete("/{post_id}", status_code=204, summary="게시글 Delete",
               description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시글만 삭제할 수 있습니다.")
def delete_post(db: Session = Depends(get_db), post_id: int = None, user_id: int = Depends(UserIdProvider())):
    post_service.delete_post(db=db, post_id=post_id, user_id=user_id)


@router.get("/{post_id}", response_model=PostResponseSchema, summary="게시글 Get(1건)",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판 또는 전체공개 게시판(public=true)의 글만 조회할 수 있습니다.")
def get_post(db: Session = Depends(get_db), post_id: int = None, user_id: int = Depends(UserIdProvider())):
    return post_service.get_post(db=db, post_id=post_id, user_id=user_id)


# todo : 이 주소는 RESTful한가?
@router.get("/boards/{board_id}", response_model=PostResponseListSchema, summary="게시글 Get(해당 게시판의 게시글 List)",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판 또는 전체공개 게시판(public=true)의 글만 조회할 수 있습니다.")
def get_post_list(db: Session = Depends(get_db), board_id: int = None, user_id: int = Depends(UserIdProvider()),
                  page: int = 1, size: int = 10):
    return post_service.get_post_by_board_id(db=db, board_id=board_id, user_id=user_id, page=page, size=size)
