# third-party
from fastapi import UploadFile
from pydantic import BaseModel


# Main Section
class OcrRequestSchema(BaseModel):
    file: UploadFile


class OcrResponseSchema(BaseModel):
    title: str

    class Config:
        from_attributes = True
