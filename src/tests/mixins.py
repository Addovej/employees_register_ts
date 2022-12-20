import pytest

from connections.postgresql import Base, engine

from .conftest import YieldAsyncFixture


class PostgresMixin:
    """Class for PostgreSQL fixtures"""

    @pytest.fixture(autouse=True)
    async def setup_postgres(self) -> YieldAsyncFixture:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


class BaseTestCase(PostgresMixin):
    """Base test class"""

    _api_pref: str
