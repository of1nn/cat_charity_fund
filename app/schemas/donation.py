from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ..., description='Полная сумма пожертвования'
    )
    comment: Optional[str] = Field(
        None, description='Комментарий к пожертвованию'
    )


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime = Field(
        ..., description='Дата создания пожертвования'
    )

    class Config:
        orm_mode = True


class DonationDBAll(DonationDB):
    close_date: Optional[datetime] = Field(
        ..., description='Дата закрытия пожертвования'
    )
    user_id: int = Field(..., description='Идентификатор пользователя')
    invested_amount: int = Field(
        ..., description='Сумма пожертвования, которая уже была вложена'
    )
    fully_invested: bool = Field(
        ...,
        description='Флаг, указывающий, что пожертвование полностью вложено',
    )
