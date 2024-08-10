from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.config import Constant


class CharityProject(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=Constant.NAME_FLD_MIN_LEN,
        max_length=Constant.NAME_FLD_MAX_LEN
    )
    description: Optional[str] = Field(
        None,
        min_length=Constant.NAME_FLD_MIN_LEN
    )
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=Constant.NAME_FLD_MIN_LEN,
        max_length=Constant.NAME_FLD_MAX_LEN
    )
    description: str = Field(
        ...,
        min_length=Constant.NAME_FLD_MIN_LEN
    )
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description', 'full_amount')
    def field_not_empty(cls, value: Union[str, int]):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
