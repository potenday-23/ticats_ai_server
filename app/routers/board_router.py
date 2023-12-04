# third-party
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.board_schema import BoardResponseSchema, BoardResponseListSchema
from app.schemas.board_schema import BoardRequestSchema
from app.services import board_service
from app.services.jwt_service import UserIdProvider

router = APIRouter(
    prefix="/api/boards",
    tags=["게시판 API"],
)


@router.post("", response_model=BoardResponseSchema, summary="게시판 Create",
             description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- name, public는 필수로 입력해야하는 값입니다.")
def create_board(board: BoardRequestSchema, db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider())):
    return board_service.create_board(db=db, board=board, user_id=user_id)


@router.put("/{board_id}", response_model=BoardResponseSchema, summary="게시판 Update",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- name, public는 필수로 입력해야하는 값입니다.")
def update_board(board: BoardRequestSchema, db: Session = Depends(get_db), board_id: int = None,
                 user_id: int = Depends(UserIdProvider())):
    return board_service.update_board(db=db, board=board, board_id=board_id, user_id=user_id)


@router.delete("/{board_id}", status_code=204, summary="게시판 Delete",
               description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판만 삭제할 수 있습니다.")
def update_board(db: Session = Depends(get_db), board_id: int = None, user_id: int = Depends(UserIdProvider())):
    board_service.delete_board(db=db, board_id=board_id, user_id=user_id)


@router.get("/{board_id}", response_model=BoardResponseSchema, summary="게시판 Get(1개)",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판 또는 전체공개 게시판(public=true)만 조회할 수 있습니다.")
def get_board(db: Session = Depends(get_db), board_id: int = None, user_id: int = Depends(UserIdProvider())):
    return board_service.get_board(db=db, board_id=board_id, user_id=user_id)


@router.get("", response_model=BoardResponseListSchema, summary="게시판 Get(리스트)",
            description="- API문서의 상단 초록색 버튼 Authorization버튼을 클릭하여 JWT 토큰을 입력해야합니다.\n- 내가 작성한 게시판 또는 전체공개 게시판(public=true)만 조회할 수 있습니다.\n- 해당 게시판에 포함된 게시글 갯수의 내림차순으로 정렬됩니다.")
def get_board_list(db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider()), page: int = 1,
                   size: int = 10):
    return board_service.get_board_list(db=db, user_id=user_id, page=page, size=size)
