from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_not_invested_projects(self, session: AsyncSession):
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(False)
            )
        )
        return projects.scalars().all()

    async def get_project_by_name(self, name: str, session: AsyncSession):
        project = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return project.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
