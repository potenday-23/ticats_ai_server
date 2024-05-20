# Fast Api
from fastapi import APIRouter

# Services
from app.services.utils import get_cultural_event_evaluation_list

# Router
router = APIRouter(
    prefix="/api/recommend",
    tags=["Recommend API"],
)


# Main Section
@router.post("", summary="OCR 분석", description="")
async def upload_ocr_photo():
    df = get_cultural_event_evaluation_list()
    print(df)

    return None
