# built-in
from datetime import datetime
# third-party
from sqlalchemy.orm import Session
import bcrypt
# Fast-app
from app.config.exceptions import ApiException, ExceptionCode
from app.models.user_model import User
from app.schemas.user_schema import UserRequestSchema


# password 암호화
def get_password_hash(password) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# password 검증
def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode('utf-8'))


# 데이터 읽기 - ID로 사용자 불러오기
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# 데이터 읽기 - Email로 사용자 불러오기
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# 데이터 읽기 - 여러 사용자 불러오기
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# 데이터 생성하기
def create_user(db: Session, user: UserRequestSchema):
    # email 중복 검사
    if get_user_by_email(db, email=user.email):
        raise ApiException(exception_code=ExceptionCode.USER_EMAIL_DUPLICATE)

    # password 암호화
    hash_password = get_password_hash(user.password)

    # User 저장
    db_user = User(email=user.email, password=hash_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 데이터 삭제 - id로 사용자 삭제하기
def delete_user_by_id(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()


# 데이터 삭제 - email로 사용자 삭제하기
def delete_user_by_email(db: Session, email: str):
    db.query(User).filter(User.email == email).delete()
    db.commit()

# # 데이터 읽기 - 여러 항목 읽어오기
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
