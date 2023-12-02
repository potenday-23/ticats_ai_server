# tird-party
from fastapi import FastAPI
# fast-api
from api.config.database_config import engine, SessionLocal, Base
from api.routers import user_router, post_router, board_router

# Root
app = FastAPI()

# DB 생성
Base.metadata.create_all(bind=engine)

# Router
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(board_router.router)


def create_app() -> FastAPI:
    """ app 변수 생성 및 초기값 설정 """

    _app = FastAPI(
        title="fastapi-pytest",
        description="fastapi 테스트 코드 연습장",
        version="1.0.0",
    )

    # DB 생성
    Base.metadata.create_all(bind=engine)

    _app.include_router(user_router.router)
    _app.include_router(post_router.router)
    _app.include_router(board_router.router)
    return _app

#
# @api.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @api.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @api.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @api.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
