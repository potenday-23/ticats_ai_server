# Fast-app
from app.schemas.ocr_schema import OcrRequestSchema


# Main Section
def get_ocr_values(ocr_photo: OcrRequestSchema):
    file = ocr_photo.file


    values = {"title": "title example"}
    return values
