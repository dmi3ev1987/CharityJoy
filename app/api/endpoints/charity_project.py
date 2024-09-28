from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_before_delete,
    check_project_before_update,
    check_project_fully_invested,
    check_project_name,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charityproject_crud, donation_crud
from app.models import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
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
    user: User = Depends(current_superuser),
):
    await check_project_name(project_in.name, session)
    project_new = await charityproject_crud.create(project_in, session)
    donations = await donation_crud.get_not_invested_donations(session)

    return await invest_donations(project_new, donations, session)


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    project = await check_project_before_delete(project_id, session, user)
    return await charityproject_crud.remove(project, session)


@router.patch('/{project_id}', response_model=CharityProjectDB)
async def edit_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    db_project = await check_project_before_update(
        project_id, project_in, session, user
    )
    project = await charityproject_crud.update(
        db_obj=db_project,
        obj_in=project_in,
        session=session,
    )
    return await check_project_fully_invested(project, session)
