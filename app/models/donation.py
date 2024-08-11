from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.charity_base import CharityBase


class Donation(CharityBase):
    """The donation model."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
