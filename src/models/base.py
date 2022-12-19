from sqlalchemy import Column, DateTime, Integer

from connections.postgresql import Base, DeclarativeBase


class BaseModel(Base, DeclarativeBase):  # type: ignore
    __abstract__ = True

    id: Column = Column(Integer, primary_key=True)
    created_dt: Column = Column(DateTime, nullable=False)
