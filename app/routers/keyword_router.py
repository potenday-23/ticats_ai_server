# Fast Api
from fastapi import APIRouter

# App
from app.schemas.keyword_schema import KeywordResponse
from app.services.keyword_service import KeywordService

# Router
router = APIRouter(
    prefix="/api/keyword",
    tags=["Keyword API"],
)


# Main Section
@router.get("", response_model=KeywordResponse)
async def get_keyword(goods_code: str = None):
    keyword_service = KeywordService()
    evaluation_text = keyword_service.get_evaluations(goods_code)
    topic, sentiment = keyword_service.united_Processor(evaluation_text)

    return KeywordResponse(topic=topic, sentiment=sentiment)
