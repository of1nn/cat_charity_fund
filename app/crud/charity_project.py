from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


class CRUDCharityProject(CRUDBase):
    async def get_id_by_name(
        self, name: str, session: AsyncSession
    ) -> Optional[int]:
        charity_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return charity_id.scalars().first()


charity_project_crud = CRUDCharityProject(
    model=CharityProject, outer_model=Donation
)
