from typing import Any

from utils import JsonResponse


class HTTPException(JsonResponse, Exception):
    status_code = -1
    empty_body = False

    __http_exception__ = True

    def __init__(self, *, text: str | dict | list, **kwargs: Any) -> None:
        JsonResponse.__init__(self, text=text, status=self.status_code, **kwargs)
        Exception.__init__(self, self.reason)


class ValidationException(HTTPException):
    status_code = 400


class NotFoundException(HTTPException):
    status_code = 404
