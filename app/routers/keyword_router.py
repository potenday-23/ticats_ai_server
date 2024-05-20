# Fast Api
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.keyword_schema import KeywordRequestSchema, KeywordResponseSchema

# Services
from app.services.utils import get_cultural_event_evaluation_list

# Router
router = APIRouter(
    prefix="/api/keyword",
    tags=["Keyword API"],
)


# Main Section
@router.post("", summary="키워드 추출", description="", response_model=KeywordResponseSchema)
async def extract_keywords(schema: KeywordRequestSchema):
    # 기대평 & 관람평 데이터프레임 가져오기
    df = get_cultural_event_evaluation_list()

    # 예시: 기대평 & 관람평 텍스트 필드가 "text" 컬럼에 있다고 가정
    text_data = df["text"].tolist()

    # 키워드 추출 및 감정 분석 수행
    all_keywords = []
    all_sentiments = []

    for text in text_data:
        # keywords = extract_keywords(text)
        # sentiment = analyze_sentiment(text)
        keywords = list()
        sentiments = list()
        all_keywords.extend(keywords)
        all_sentiments.append(sentiments)

    # KeywordResponseSchema 객체 생성 및 반환
    response = KeywordResponseSchema(keywords=all_keywords, sentiments=all_sentiments)
    return response