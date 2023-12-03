# third-party
from sqlalchemy.orm import Session

# Fast-app
from app.config.exceptions import ApiException, ExceptionCode
from app.models.post_model import Post
from app.schemas.post_schema import PostRequestSchema


# 데이터 읽기 - ID로 사용자 불러오기
from app.services.board_service import get_board_by_id


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


# 데이터 읽기 - 여러 사용자 불러오기
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


# 데이터 생성하기
def create_post(db: Session, post: PostRequestSchema, user_id: int):
    # 내 게시판인지, 전체공개 게시판인지 검증
    board = get_board_by_id(db, post.board_id)
    if board.user_id != user_id and board.public == False:
        raise ApiException(exception_code=ExceptionCode.POST_BOARD_UNAUTHORIZATION)

    # Post 저장
    db_post = Post(title=post.title, content=post.content, user_id=user_id, board_id=post.board_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# 데이터 삭제 - id로 게시글 삭제하기
def delete_post_by_id(db: Session, post_id: int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
