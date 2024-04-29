# Config
from app.config.exceptions import validation_exception_handler

# Fast API
from fastapi import FastAPI

# Routers
from app.routers import ocr_router, recommend_router

# Exception
from fastapi.exceptions import RequestValidationError


# Main Section
app = FastAPI(
    title="티켓 사진 OCR 서버",
    summary="티켓 사진의 텍스트로 추출하는 FastAPI 기반 프로젝트",
    description="✔ Tech : FastAPI, SQLAlchemy, pydantic, postgresql, JWT, Alembic, Docker, AWS",
    version="0.0.1",
    contact={
        "name": "김가영",
        "url": "https://github.com/gabang2",
        "email": "offbeat1020@naver.com"
    },
    openapi_tags=[
        {
            "name": "OCR API",
            "description": "사진을 넣으면 value 추출",
        }
    ]
)

# Router
app.include_router(ocr_router.router)
app.include_router(recommend_router.router)

# exception Handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
