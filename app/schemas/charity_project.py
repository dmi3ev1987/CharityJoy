from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    @validator('name', 'description')
    def check_not_empty(cls, value):
        if not value:
            raise ValueError(f'{value.capitalize()} is empty')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt
    create_date: datetime = Field(default_factory=datetime.now)


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True
