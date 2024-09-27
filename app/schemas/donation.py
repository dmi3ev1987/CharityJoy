from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    create_date: datetime = Field(default_factory=datetime.now)


class DonationSortDB(DonationCreate):
    id: int

    class Config:
        orm_mode = True


class DonationFullDB(DonationSortDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)
