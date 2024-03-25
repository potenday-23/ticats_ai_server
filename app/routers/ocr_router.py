# Fast Api
from fastapi import APIRouter

# Schemas
from app.schemas.ocr_schema import OcrRequestSchema, OcrResponseSchema

# Services
from app.services import ocr_service

# Router
router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR API"],
)


# Main Section
@router.post("", response_model=OcrResponseSchema, summary="OCR 분석", description="")
async def upload_ocr_photo(ocr_photo: OcrRequestSchema):
    return ocr_service.get_ocr_values(ocr_photo=ocr_photo)
