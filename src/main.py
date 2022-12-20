from logging.config import dictConfig

from aiohttp.web import Application, Request, Response, run_app, static

from api import employees_v1_router
from conf import settings
from conf.logging import get_logging
from middlewares import exception_middleware


async def index(request: Request) -> Response:
    with open(f'{settings.STATIC_PATH}/index.html') as f:
        return Response(text=f.read(), content_type='text/html')


app = Application(middlewares=[exception_middleware])
dictConfig(get_logging(log_level=settings.LOG_LEVEL))

app.router.add_get('/', index)
app.add_routes(employees_v1_router)
app.add_routes([static('/', settings.STATIC_PATH)])

if __name__ == '__main__':
    run_app(app, port=settings.PORT)
