from json import dumps
from typing import Any, Optional

from aiohttp.typedefs import LooseHeaders
from aiohttp.web import Response
from pydantic import BaseModel


def stringify(val: Any) -> str:
    return str(val)


class JsonResponse(Response):

    def __init__(
            self,
            *,
            text: Optional[str | dict | list | BaseModel] = None,
            status: int = 200,
            content_type: Optional[str] = 'application/json',
            headers: Optional[LooseHeaders] = None,
            **kwargs: Any
    ) -> None:
        if isinstance(text, BaseModel):
            text = text.json()
        if isinstance(text, (dict, list)):
            text = dumps(text)

        super().__init__(
            text=text, status=status, content_type=content_type, headers=headers, **kwargs
        )
