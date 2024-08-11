from datetime import datetime
from app.models.charity_base import CharityBase


async def process_donation(
        charity_obj: CharityBase,
        charity_db_list: list) -> CharityBase:
    for db in charity_db_list:
        charity_obj, db = distribute_money(charity_obj, db)
    return charity_obj


def close_charity(charity_db: CharityBase) -> CharityBase:
    charity_db.invested_amount = charity_db.full_amount
    charity_db.fully_invested = True
    charity_db.close_date = datetime.now()
    return charity_db


def distribute_money(
        obj: CharityBase,
        db: CharityBase) -> CharityBase:
    remaining_obj = obj.full_amount - obj.invested_amount
    remaining_db = db.full_amount - db.invested_amount
    if remaining_obj > remaining_db:
        obj.invested_amount += remaining_db
        db = close_charity(db)
    elif remaining_obj == remaining_db:
        obj = close_charity(obj)
        db = close_charity(db)
    else:
        db.invested_amount += remaining_obj
        obj = close_charity(obj)
    return obj, db
