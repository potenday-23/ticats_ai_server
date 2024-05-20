from typing import List
from pydantic import BaseModel


# Main Section
class KeywordRequestSchema(BaseModel):
    content: str


class KeywordResponseSchema(BaseModel):
    keywords: List[str] = []
    sentiments: List[str] = []

    class Config:
        orm_mode = True
