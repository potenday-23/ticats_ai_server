# Config
from app.config.exceptions import validation_exception_handler

# Fast API
from fastapi import FastAPI

# Exception
from fastapi.exceptions import RequestValidationError

# Main Section
app = FastAPI(
    title="AI 서버",
    summary=" - 키워드 추출 및 감성 추출\n"
            " - 문화생활 추천\n",
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


# Router inclusion moved inside the function to avoid circular imports
def include_routers(app):
    from app.routers import keyword_router, ocr_router, recommend_router
    app.include_router(keyword_router.router)
    app.include_router(ocr_router.router)
    app.include_router(recommend_router.router)


include_routers(app)

# exception Handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
