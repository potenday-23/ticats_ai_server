# Fast Api
import json

import numpy as np
from fastapi import APIRouter
from fastapi.params import Query
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.recommend_service import RecommendService

# Router
router = APIRouter(
    prefix="/api/recommend",
    tags=["Recommend API"],
)


def get_recommend_service(db: Session = Depends(get_db)):
    return RecommendService(db)


# Main Section
@router.get("", summary="문화생활 추천", description="")
async def get_recommendations(
        cultural_ids: List[int] = Query(None, description="Comma-separated list of cultural event IDs"),
        recommend_service: RecommendService = Depends(get_recommend_service)):
    recommend_cultural_event_ids = recommend_service.content_recommender(cultural_ids)
    # numpy 데이터를 일반 Python 데이터 타입으로 변환
    recommend_cultural_event_ids = [int(id_) if isinstance(id_, np.integer) else id_ for id_ in
                                    recommend_cultural_event_ids]

    return recommend_cultural_event_ids
