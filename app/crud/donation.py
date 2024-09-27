from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    async def get_not_invested_donations(
        self, session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.fully_invested.is_(False))
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
