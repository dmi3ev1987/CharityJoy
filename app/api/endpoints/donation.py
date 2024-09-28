from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import charityproject_crud, donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.invest import invest_donations

router = APIRouter()

FIELDS_TO_EXCLUDE = {
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date',
}


@router.get('/', response_model=list[DonationDB])
async def get_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude=FIELDS_TO_EXCLUDE,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    projects = await charityproject_crud.get_not_invested_projects(session)

    return await invest_donations(new_donation, projects, session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude=FIELDS_TO_EXCLUDE,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(session=session, user=user)
