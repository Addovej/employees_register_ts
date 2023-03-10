from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from utils import stringify


class EmployeeSchema(BaseModel):
    id: Optional[int]
    chief_id: Optional[int]
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    position: str
    hire_date: date
    salary: float

    _normalize_hire_date = validator('hire_date', allow_reuse=True)(stringify)

    class Config:
        orm_mode = True


class EmployeeUpdateSchema(BaseModel):
    chief_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]

    position: Optional[str]
    hire_date: Optional[date]
    salary: Optional[float]


class EmployeeListSchema(BaseModel):
    __root__: list[EmployeeSchema]
