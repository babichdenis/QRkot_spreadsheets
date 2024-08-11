from sqlalchemy import Column, String, Text

from app.models.charity_base import CharityBase


class CharityProject(CharityBase):
    """The project model."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
