import asyncio
from typing import Any, AsyncGenerator, TypeVar

import pytest
from aiohttp.test_utils import TestClient, TestServer

from conf import settings
from main import app

from ._db_utils import create_database
from .factories import Employee

T = TypeVar('T')
YieldAsyncFixture = AsyncGenerator[T, None]


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if 'There is no current event loop in thread' in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
async def setup(event_loop: asyncio.AbstractEventLoop) -> YieldAsyncFixture:
    # Create test database if not exists
    await create_database(str(settings.POSTGRES_DSN))

    yield


@pytest.fixture
async def server(aiohttp_server: Any) -> TestServer:
    return await aiohttp_server(app)


@pytest.fixture
async def client(server: TestServer) -> YieldAsyncFixture[TestClient]:
    async with TestClient(server) as client:
        yield client


# Data fixtures

@pytest.fixture
def employee() -> dict:
    return Employee.build()
