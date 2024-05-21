# Fast Api
from fastapi import APIRouter

# App
from app.schemas.keyword_schema import KeywordResponse
from app.services.keyword_service import get_evaluations

# Schema

# Router
router = APIRouter(
    prefix="/api/keyword",
    tags=["Keyword API"],
)


# Main Section
@router.get("", response_model=KeywordResponse)
async def get_keyword(goods_code: str = None):
    # 1. 기대평 & 관람평 추출
    evaluation_text = get_evaluations(goods_code)

    # 2. 토픽 추출
    topic = "topic example"

    # 3. 감정 추출
    sentiment = "sentiment example"

    return KeywordResponse(topic=topic, sentiment=sentiment)
