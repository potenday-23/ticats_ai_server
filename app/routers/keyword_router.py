# Fast Api
import time

from fastapi import APIRouter, Depends

# App
from app.schemas.keyword_schema import KeywordResponse
from app.services.keyword_service import KeywordService

# Router
router = APIRouter(
    prefix="/api/keyword",
    tags=["Keyword API"],
)

# Create a single instance of KeywordService
keyword_service = KeywordService()


# Dependency injection function
def get_keyword_service():
    return keyword_service


# Main Section
@router.get("", response_model=KeywordResponse)
async def get_keyword(goods_code: str = None, keyword_service: KeywordService = Depends(get_keyword_service)):


    evaluation_text = keyword_service.get_evaluations(goods_code)
    topic, sentiment = keyword_service.united_Processor(evaluation_text)

    return KeywordResponse(topic=topic, sentiment=sentiment)
