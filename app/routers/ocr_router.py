from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel

from app.services.ocr_service import OcrService


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
async def upload_ocr_photo(image: UploadFile = File(...), ocr_service: OcrService = Depends(OcrService)):
    image_content = await image.read()
    ocr_result = ocr_service.info_extractor(image_content)
    return ocr_result
