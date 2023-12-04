# third-party
from datetime import datetime

from sqlalchemy.orm import Session

# Fast-app
from app.config.exceptions import ApiException, ExceptionCode
from app.models import Board
from app.models.post_model import Post
from app.schemas.common_schema import PageInfo
from app.schemas.post_schema import PostRequestSchema, PostUpdateRequestSchema

from app.services.board_service import get_board_by_id
from app.services.common_service import get_page_info


def get_post_by_id(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise ApiException(exception_code=ExceptionCode.POST_NOT_FOUND)
    return post


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


# 데이터 수정하기
def update_post(db: Session, post: PostUpdateRequestSchema, post_id: int, user_id: int):
    db_post = get_post_by_id(db, post_id)
    # 내 Post인지 검증
    if db_post.user_id != user_id:
        raise ApiException(exception_code=ExceptionCode.POST_CANT_UPDATE)

    # Post 수정
    db_post.title = post.title
    db_post.content = post.content
    db_post.updated_at = datetime.now()
    db.add(db_post)
    db.commit()
    return db_post


# 데이터 삭제
def delete_post(db: Session, post_id: int, user_id: int):
    db_post = get_post_by_id(db, post_id)

    # 내 Post인지 검증
    if db_post.user_id != user_id:
        raise ApiException(exception_code=ExceptionCode.POST_CANT_UPDATE)

    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()


# 데이터 조회
def get_post(db: Session, post_id: int, user_id: int):
    # 내 게시판, 전체공개 게시판 검증
    post = get_post_by_id(db, post_id)
    if post.board.user_id != user_id and post.board.public == False:
        raise ApiException(exception_code=ExceptionCode.POST_BOARD_UNAUTHORIZATION)

    return post


# 데이터 삭제 - id로 게시글 삭제하기
def delete_post_by_id(db: Session, post_id: int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()


# 게시판 데이터 조회
def get_post_by_board_id(db: Session, board_id: int, user_id: int, page: int, size: int):
    # 내 게시판, 전체공개 게시판 검증
    db_board = get_board_by_id(db, board_id)
    if db_board.user_id != user_id and db_board.public == False:
        raise ApiException(exception_code=ExceptionCode.BOARD_CANT_GET)
    posts = db.query(Post).filter(Post.board_id == board_id)  # todo : 쿼리가 두 번 돌아가는데 이를 줄일 수 있는 방법은 없을까?

    # page_info 계산
    page_info = get_page_info(posts.count(), page, size)
    post_list = posts.offset((page - 1) * size).limit(page * size).all()

    return {
        "post_list": post_list,
        "page_info": page_info
    }
