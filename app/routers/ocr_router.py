from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.ocr_service import OcrService


# Dependency injection function
def get_ocr_service():
    return OcrService()


# Response schema definition
class OcrResponseSchema(BaseModel):
    result: str
    title: str


# Router
router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR API"],
)


@router.post("", response_model=OcrResponseSchema, summary="OCR 분석", description="")
async def upload_ocr_photo(ocr_service: OcrService = Depends(get_ocr_service)):
    ocr_result = ocr_service.run_ocr()
    return {"result": "hello", "title": "OCR Analysis Result"}
