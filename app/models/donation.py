from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)

from app.models.charity_project import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
