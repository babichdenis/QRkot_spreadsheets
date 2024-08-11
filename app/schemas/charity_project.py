from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.variables import MAX_LENGTH, MIN_LENGTH


class CharityProjectBase(BaseModel):
    """The basic scheme of the project."""
    name: Optional[str] = Field(None, min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    """Schema for creating a new project."""
    name: str = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(..., min_length=MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Schema for updating the project."""

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Schema for displaying projects."""
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
