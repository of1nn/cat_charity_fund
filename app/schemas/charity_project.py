from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, validator, Extra


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description='Имя проекта'
    )
    description: Optional[str] = Field(
        None, min_length=1, description='Описание проекта'
    )
    full_amount: Optional[PositiveInt] = Field(
        None, description='Полная сумма сбора'
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=1, max_length=100, description='Имя проекта'
    )
    description: str = Field(..., min_length=1, description='Описание проекта')
    full_amount: PositiveInt = Field(..., description='Полная сумма сбора')


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
