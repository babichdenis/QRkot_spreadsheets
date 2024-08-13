from datetime import datetime
from typing import List, Union
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, CharityBase, Donation


def close_obj(obj: Union[CharityBase, Donation]) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


def investment_process(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> None:
    free_target_amount = target.full_amount
    for source in sources:
        free_amount = min(
            free_target_amount, source.full_amount - source.invested_amount)
        source.invested_amount += free_amount
        target.invested_amount += free_amount
        free_target_amount -= free_amount
        if source.full_amount == source.invested_amount:
            close_obj(source)
        if not free_target_amount:
            close_obj(target)
            break

# async def process_donation(
#         charity_obj: CharityBase,
#         charity_db: CharityBase,
#         session: AsyncSession
# ) -> CharityBase:
#     all_db = await session.execute(select(charity_db).where(
#         charity_db.fully_invested == 0
#     ).order_by(charity_db.create_date))
#     all_db = all_db.scalars().all()
#     for db in all_db:
#         charity_obj, db = distribute_money(charity_obj, db)
#         session.add_all([charity_obj, db])
#     await session.commit()
#     await session.refresh(charity_obj)
#     return charity_obj


def close_charity(charity_db: CharityBase) -> CharityBase:
    charity_db.invested_amount = charity_db.full_amount
    charity_db.fully_invested = True
    charity_db.close_date = datetime.now()
    return charity_db


def distribute_money(obj: CharityBase, db: CharityBase) -> CharityBase:
    remaining_obj = obj.full_amount - obj.invested_amount
    remaining_db = db.full_amount - db.invested_amount

    if remaining_obj > remaining_db:
        obj.invested_amount += remaining_db
        db = close_charity(db)
    elif remaining_obj == remaining_db:
        obj, db = close_charity(obj), close_charity(db)
    else:
        db.invested_amount += remaining_obj
        obj = close_charity(obj)

    return obj, db
