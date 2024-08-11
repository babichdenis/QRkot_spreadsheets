from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_base import CharityBase


async def process_donation(
        charity_obj: CharityBase,
        charity_db: CharityBase,
        session: AsyncSession
) -> CharityBase:
    all_db = await session.execute(select(charity_db).where(
        charity_db.fully_invested == 0
    ).order_by(charity_db.create_date))
    all_db = all_db.scalars().all()
    for db in all_db:
        charity_obj, db = distribute_money(charity_obj, db)
        session.add_all([charity_obj, db])
    await session.commit()
    await session.refresh(charity_obj)
    return charity_obj


def close_charity(charity_db: CharityBase) -> CharityBase:
    charity_db.invested_amount = charity_db.full_amount
    charity_db.fully_invested = True
    charity_db.close_date = datetime.now()
    return charity_db


def distribute_money(
        charity_obj: CharityBase,
        charity_db: CharityBase
) -> CharityBase:
    remaining_charity_obj = charity_obj.full_amount - charity_obj.invested_amount
    remaining_charity_db = charity_db.full_amount - charity_db.invested_amount
    if remaining_charity_obj > remaining_charity_db:
        charity_obj.invested_amount += remaining_charity_db
        charity_db = close_charity(charity_db)
    elif remaining_charity_obj == remaining_charity_db:
        charity_obj = close_charity(charity_obj)
        charity_db = close_charity(charity_db)
    else:
        charity_db.invested_amount += remaining_charity_obj
        charity_obj = close_charity(charity_obj)
    return charity_obj, charity_db
