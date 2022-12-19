import logging
import uuid
from typing import Any, Optional, TypeVar, Union

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.base import ColumnCollection
from sqlalchemy.sql.schema import Column, MetaData

from conf import settings

logger = logging.getLogger(__name__)

DeclarativeBaseType = TypeVar('DeclarativeBaseType', bound='DeclarativeBase')


class DeclarativeBase:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.metadata: MetaData = MetaData()
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'

    @classmethod
    @property
    def _columns(cls) -> ColumnCollection:
        return inspect(cls).columns

    @classmethod
    @property
    def _columns_keys(cls) -> list[Column]:
        return [c.key for c in cls._columns]  # type: ignore

    @classmethod
    @property
    def _pk_name(cls) -> str:
        return inspect(cls).primary_key[0].name

    @classmethod
    @property
    def _pk_column(cls) -> Column:
        return getattr(cls, cls._pk_name)  # type: ignore

    @property
    def _pk_value(self) -> Union[int, uuid.UUID]:
        return getattr(self, self._pk_name)

    @classmethod
    def _get_db(cls) -> AsyncSession:
        return make_db()

    @classmethod
    async def create(
            cls,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
            _refresh: bool = True,
            **kwargs: Any
    ) -> DeclarativeBaseType:
        """Create a new model instance and saves to DB."""

        db: AsyncSession = _db or cls._get_db()
        try:
            obj = cls.__call__(**kwargs)
            db.add(obj)

            if _commit:
                await db.commit()
                if _refresh:
                    await db.refresh(obj)
        finally:
            if not _db:
                await db.close()

        return obj

    @classmethod
    async def get(cls, pk: Any, _db: Optional[AsyncSession] = None) -> DeclarativeBaseType:
        """Return a model instance by PK."""

        db: AsyncSession = _db or cls._get_db()
        try:
            obj = await db.get(cls, ident=pk)
        finally:
            if not _db:
                await db.close()

        return obj

    @classmethod
    async def get_list(
            cls, *args: Any, _db: Optional[AsyncSession] = None, **kwargs: Any
    ) -> list[DeclarativeBaseType]:
        """Return a list of model instances."""

        db: AsyncSession = _db or cls._get_db()
        order_by = kwargs.pop('order_by', None)
        try:
            result = await db.execute(select(cls).filter(*args, **kwargs).order_by(
                order_by if order_by else cls._pk_column
            ))
        finally:
            if not _db:
                await db.close()

        return result.all()

    async def save(
            self,
            update_fields: Optional[Union[tuple[str, ...], list[str], set[str]]] = None,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
    ) -> None:
        """Save changed model's fields to DB."""

        if not self._pk_value:
            raise Exception(f'Unable to get primary key value for {self} column {self._pk_column}')

        if update_fields:
            data = {k: getattr(self, str(k)) for k in self._columns_keys if k in update_fields}
        else:
            data = {k: getattr(self, str(k)) for k in self._columns_keys}

        db: AsyncSession = _db or self._get_db()
        try:
            query = update(self.__class__).values(**data).where(self._pk_column == self._pk_value)

            query.execution_options(synchronize_session='fetch')
            await db.execute(query)

            if _commit:
                await db.commit()
        finally:
            if not _db:
                await db.close()

    async def delete(self, _db: Optional[AsyncSession] = None, _commit: bool = True) -> None:
        """Delete a model instance from DB."""

        db: AsyncSession = _db or self._get_db()
        try:
            await db.delete(self)

            if _commit:
                await db.commit()
        finally:
            if not _db:
                await db.close()


Base: DeclarativeBase = declarative_base(cls=DeclarativeBase)

# Make DB
engine = create_async_engine(settings.POSTGRES_DSN)
make_db = sessionmaker(bind=engine, class_=AsyncSession, future=True, expire_on_commit=False)
