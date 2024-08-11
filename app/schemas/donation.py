from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    """A scheme for creating a new donation."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    """A scheme for viewing donations."""
    id: int
    create_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationDBAll(DonationDB):
    """A scheme for the full viewing of donations."""
    invested_amount: Optional[int]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]
