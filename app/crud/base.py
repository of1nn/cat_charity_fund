from typing import Optional
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model, outer_model):
        self.model = model
        self.outer_model = outer_model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()

        if user is not None:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)
        outer_obj = await session.execute(
            select(self.outer_model).where(
                self.outer_model.fully_invested == 0
            )
        )

        outer_obj = outer_obj.scalars().all()
        remaining_amount = db_obj.full_amount

        for obj in outer_obj:
            if remaining_amount <= 0:
                break

            # Вычислить сколько можно инвестировать в текущий проект
            available_amount = obj.full_amount - obj.invested_amount
            invest_amount = min(available_amount, remaining_amount)

            obj.invested_amount += invest_amount
            remaining_amount -= invest_amount

            # Если пожертвование полностью инвестировано
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

            session.add(obj)

        db_obj.invested_amount = db_obj.full_amount - remaining_amount
        if db_obj.invested_amount >= db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
