from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Donation, CharityProject


class CRUDDonation(CRUDBase):
    async def get_by_user(
        self, session: AsyncSession, user_id: int
    ) -> Donation:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(model=Donation, outer_model=CharityProject)
