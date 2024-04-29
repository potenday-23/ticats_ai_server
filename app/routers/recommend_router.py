# Fast Api
from fastapi import APIRouter

# Services
from app.services.recommend_service import get_cultural_event_list

# Router
router = APIRouter(
    prefix="/api/recommend",
    tags=["Recommend API"],
)


# Main Section
@router.post("", summary="OCR 분석", description="")
async def upload_ocr_photo():
    df = get_cultural_event_list()
    print(df)

    return None
