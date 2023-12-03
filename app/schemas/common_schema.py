from pydantic import BaseModel


class PageInfo(BaseModel):
    page: int
    size: int
    total_elements: int
    total_pages: int
