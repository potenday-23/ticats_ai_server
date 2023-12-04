from app.schemas.common_schema import PageInfo


def get_page_info(total_elements: int, page: int, size: int):
    total_pages = int(total_elements / size + (0 if total_elements % size == 0 else 1))

    # page_info 설정
    data = {
        "page": page,
        "size": size,
        "total_elements": total_elements,
        "total_pages": total_pages
    }
    return PageInfo(**data)
