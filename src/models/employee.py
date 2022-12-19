from datetime import date
from datetime import datetime as dt
from typing import Any, Optional

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from schemas import EmployeeUpdateSchema

from .base import BaseModel


class Employee(BaseModel):
    __tablename__ = 'employees'

    first_name: Column = Column(String(50))
    last_name: Column = Column(String(50))
    middle_name: Column = Column(String(50), nullable=True)

    position: Column = Column(String(25))
    hire_date: Column = Column(Date)
    salary: Column = Column(Float)

    chief_id: Column = Column(Integer, ForeignKey('employees.id'), nullable=True)
    chief = relationship('Employee')

    @classmethod
    async def create(
            cls,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
            _refresh: bool = True,
            **kwargs: Any
    ) -> 'Employee':
        """Overridden create method created_at default values"""

        if 'created_dt' not in kwargs:
            kwargs['created_dt'] = dt.utcnow()
        if not isinstance(kwargs['hire_date'], date):
            kwargs['hire_date'] = date.fromisoformat(kwargs['hire_date'])

        return await super().create(_db, _commit, _refresh, **kwargs)

    async def update(self, data: EmployeeUpdateSchema) -> 'Employee':

        for field in data.__fields_set__:
            setattr(self, field, getattr(data, field))
        await self.save(data.__fields_set__)

        return self
