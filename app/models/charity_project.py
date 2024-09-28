from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from app.core.db import Base


class CharityDonationBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)


class CharityProject(CharityDonationBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
