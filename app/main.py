# tird-party
from fastapi import FastAPI
# fast-api
from app.config.config import engine, SessionLocal, Base
from app.config.exceptions import validation_exception_handler
from app.routers import user_router, post_router, board_router
from fastapi.exceptions import RequestValidationError

# Root
app = FastAPI(
    title="김가영 미니 프로젝트",
    summary="엘리스 신입(python) 채용 과제로 수행한, 게시판, 게시글을 작성할 수 있는 FastAPI 기반 프로젝트",
    description="✔ 수행 기간 : 2023.12.01(9:00) ~ 2023.12.05(9:00)<br>"
                "✔ Tech : FastAPI, SQLAlchemy, pydantic, postgresql, JWT, Alembic, Docker, AWS",
    version="0.0.1",
    contact={
        "name": "김가영",
        "url": "https://github.com/gabang2",
        "email": "offbeat1020@naver.com"
    },
    openapi_tags=[
        {
            "name": "계정 API",
            "description": "사용자의 회원가입(SignUp), 로그인(Login), 로그아웃(Logout)",
        },
        {
            "name": "게시판 API",
            "description": "사용자의 권한에 따라 게시판 생성, 수정, 삭제, 단건 조회, 목록 조회",
        },
        {
            "name": "게시글 API",
            "description": "사용자의 권한에 따라 게시글 생성, 수정, 삭제, 단건 조회, 게시판 목록 조회",
        }
    ]
)

# DB 생성
# Base.metadata.create_all(bind=engine)

# Router
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(board_router.router)

# exception Handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
