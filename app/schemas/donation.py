from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    create_date: datetime = Field(default_factory=datetime.now)


class DonationDB(DonationCreate):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True
