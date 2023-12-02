# third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Fast-api
from api.config.database_config import get_db
from api.schemas.board_schema import BoardResponseSchema
from api.schemas.board_schema import BoardRequestSchema
from api.services import board_service

router = APIRouter(
    prefix="/api/boards",
    tags=["게시판 API"],
)


@router.post("", response_model=BoardResponseSchema, summary="게시판 Create")
def create_board(board: BoardRequestSchema, db: Session = Depends(get_db)):
    return board_service.create_board(db=db, board=board)

