from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.models import User
from app.crud import donation_crud
from app.schemas import DonationDBAll, DonationDB, DonationCreate


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBAll],
    dependencies=[
        Depends(current_superuser),
    ],
)
async def get_donation(session: AsyncSession = Depends(get_async_session)):
    all_dontations = await donation_crud.get_multi(session=session)
    return all_dontations


@router.get(
    '/my/',
    response_model=list[DonationDB],
)
async def get_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    my_donation = await donation_crud.get_by_user(
        session=session, user_id=user.id
    )
    return my_donation


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donation_crud.create(
        session=session, obj_in=donation, user=user
    )
    return donation
