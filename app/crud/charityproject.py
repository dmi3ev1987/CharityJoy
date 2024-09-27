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


charityproject_crud = CRUDCharityProject(CharityProject)
