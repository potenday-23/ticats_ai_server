# third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Fast-app
from app.config.config import get_db
from app.schemas.board_schema import BoardResponseSchema
from app.schemas.board_schema import BoardRequestSchema
from app.services import board_service
from app.services.jwt_service import UserIdProvider

router = APIRouter(
    prefix="/api/boards",
    tags=["게시판 API"],
)


@router.post("", response_model=BoardResponseSchema, summary="게시판 Create")
def create_board(board: BoardRequestSchema, db: Session = Depends(get_db), user_id: int = Depends(UserIdProvider())):
    return board_service.create_board(db=db, board=board, user_id=user_id)
