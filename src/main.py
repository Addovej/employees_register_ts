from logging.config import dictConfig

from aiohttp.web import Application, run_app

from api import employees_v1_router
from conf import settings
from conf.logging import get_logging
from middlewares import exception_middleware

app = Application(middlewares=[exception_middleware])
dictConfig(get_logging(log_level=settings.LOG_LEVEL))

app.add_routes(employees_v1_router)

if __name__ == '__main__':
    run_app(app, port=settings.PORT)
