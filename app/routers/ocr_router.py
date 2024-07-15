import json
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel

from app.services.ocr_service import OcrService


# Response schema definition
class OcrResponseSchema(BaseModel):
    title: Optional[str]
    place: Optional[str]
    date: Optional[str]
    seat: Optional[str]


# Router
router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR API"],
)


@router.post("", response_model=OcrResponseSchema, summary="OCR 분석", description="")
async def upload_ocr_photo(image: UploadFile = File(...), ocr_service: OcrService = Depends(OcrService)):
    image_content = await image.read()
    ocr_result = ocr_service.info_extractor(image_content)

    # OCR 결과가 None일 경우 기본값을 설정
    if ocr_result is None:
        ocr_result = {}

    # OCR 결과에서 필요한 필드를 추출하여 응답 형식에 맞게 변환
    response_data = {
        "title": ocr_result.get("공연제목") or None,
        "place": ocr_result.get("공연장소") or None,
        "date": ocr_result.get("공연날짜") or None,
        "seat": ocr_result.get("좌석정보") or None
    }

    return response_data
