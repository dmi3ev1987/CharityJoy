from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charityproject_crud
from app.models import CharityProject, User
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_name(project_name: str, session: AsyncSession):
    if await charityproject_crud.get_project_by_name(project_name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_fully_invested(
    project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def check_project_before_edit(
    project_id: int,
    session: AsyncSession,
    user: User,
) -> CharityProject:
    project = await charityproject_crud.get(
        obj_id=project_id,
        session=session,
    )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать полностью инвестированный проект!',
        )
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    if not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Недостаточно прав для редактирования проекта!',
        )

    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession,
    user: User,
) -> CharityProject:
    project = await check_project_before_edit(project_id, session, user)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект в процессе инвестирования!',
        )

    return project


async def check_project_before_update(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession,
    user: User,
) -> CharityProject:
    project_db = await check_project_before_edit(project_id, session, user)
    if project_in.full_amount is not None:
        if project_in.full_amount < project_db.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Сумма инвестиции не может быть меньше уже вложенной!',
            )
    if project_in.name is not None:
        await check_project_name(project_in.name, session)

    return project_db
