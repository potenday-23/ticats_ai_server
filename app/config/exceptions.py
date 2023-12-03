# third-party
from enum import Enum

from fastapi import HTTPException


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_422 = 422


class ExceptionCode:
    # Server Error
    SERVER_ERROR = (StatusCode.HTTP_500, "S001", "백엔드 서버 에러입니다. 해당 에러는 추후 개선 예정입니다.")

    # Authorization
    TOKEN_NOT_VALID = (StatusCode.HTTP_401, "A001", "유효하지 않은 토큰입니다.")
    TOKEN_EXPIRED = (StatusCode.HTTP_401, "A002", "유효기한이 만료된 토큰입니다.")
    AUTHORIZATION_EMPTY = (StatusCode.HTTP_401, "A003", "인증 정보(Authorization)이 누락되었습니다.")

    # USER
    USER_NOT_FOUND = (StatusCode.HTTP_400, "U001", "해당 id의 사용자가 없습니다.")
    USER_EMAIL_DUPLICATE = (StatusCode.HTTP_400, "U002", "해당 이메일은 이미 사용중입니다.")
    USER_NOT_VALID = (StatusCode.HTTP_400, "U003", "이메일이 존재하지 않거나, 비밀번호를 틀렸습니다.")

    # BOARD
    BOARD_NOT_FOUND = (StatusCode.HTTP_400, "B001", "해당 id의 게시판이 없습니다.")

    # POST
    POST_NOT_FOUND = (StatusCode.HTTP_400, "P001", "해당 id의 게시글이 없습니다.")


class ApiException(HTTPException):
    """
    사용 예시
    raise ApiException(exception_code=ExceptionCode.USER_NOT_FOUND)
    """

    def __init__(self,
                 exception_code: tuple = ExceptionCode.SERVER_ERROR):
        super().__init__(
            status_code=exception_code[0],
            detail={
                "status_code": exception_code[0],
                "code": exception_code[1],
                "message": exception_code[2]
            }
        )


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(exc: RequestValidationError):
#     details = exc.errors()
#     return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                         content={"status_code": StatusCode.HTTP_422,
#                                  "code": "C422",
#                                  "message": details[0]["msg"]
#                                  }
#                         )
