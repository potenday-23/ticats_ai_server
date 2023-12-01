# third-party
from sqlalchemy.orm import Session

# Fast-api
from app.models.post_model import Post
from app.schemas.post_schema import PostRequestSchema


# 데이터 읽기 - ID로 사용자 불러오기
def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


# 데이터 읽기 - 여러 사용자 불러오기
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


# 데이터 생성하기
def create_post(db: Session, post: PostRequestSchema):
    # Post 저장
    db_post = Post(title=post.title, content=post.content, user_id=post.user_id, board_id=post.board_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# # 데이터 읽기 - 여러 항목 읽어오기
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_post_item(db: Session, item: schemas.ItemCreate, post_id: int):
#     db_item = models.Item(**item.dict(), owner_id=post_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
