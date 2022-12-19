from logging import getLogger
from typing import Callable

from aiohttp.web import Application, Request

from exceptions import HTTPException
from utils import JsonResponse

logger = getLogger(__name__)


async def exception_middleware(app: Application, handler: Callable) -> Callable:
    async def middleware_handler(request: Request) -> JsonResponse:
        try:
            return await handler(request)
        except HTTPException as e:
            return e
        except Exception as e:
            logger.warning(f'Request {request} has failed with exception: {repr(e)}')
            return JsonResponse(text={'detail': f'Error: {e}'}, status=500)

    return middleware_handler
