from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import charityproject_crud, donation_crud
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB
from app.services.invest import invest_donations

router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB])
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charityproject_crud.get_multi(session)


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    project_new = await charityproject_crud.create(project_in, session)
    donations = await donation_crud.get_not_invested_donations(session)

    return await invest_donations(project_new, donations, session)
