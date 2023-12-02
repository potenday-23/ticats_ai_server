# third-party
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

# Fast-app
from app.models.board_model import Board
from app.schemas.board_schema import BoardRequestSchema


# 데이터 읽기 - ID로 게시판 불러오기
def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


# 데이터 읽기 - 여러 게시판 불러오기
def get_boards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Board).offset(skip).limit(limit).all()


# 데이터 생성하기
def create_board(db: Session, board: BoardRequestSchema):
    # Board 저장
    db_board = Board(name=board.name, public=board.public, user_id=board.user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


# 데이터 삭제 - id로 게시판 삭제하기
def delete_board_by_id(db: Session, board_id: int):
    db.query(Board).filter(Board.id == board_id).delete()
    db.commit()
