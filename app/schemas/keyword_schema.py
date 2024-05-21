from pydantic import BaseModel


class KeywordResponse(BaseModel):
    topic: str
    sentiment: str
