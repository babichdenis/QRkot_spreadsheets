from datetime import datetime
from app.models.charity_base import CharityBase


def process_donation(
    charity_obj: CharityBase,
    charity_db_list: list
) -> CharityBase:
    for charity_db in charity_db_list:
        charity_obj, charity_db = distribute_money(
            charity_obj,
            charity_db
        )
    return charity_obj


def close_charity(charity_db: CharityBase) -> CharityBase:
    charity_db.invested_amount = charity_db.full_amount
    charity_db.fully_invested = True
    charity_db.close_date = datetime.now()
    return charity_db


def distribute_money(charity_obj: CharityBase,
                     charity_db: CharityBase) -> CharityBase:
    remaining_obj = charity_obj.full_amount - charity_obj.invested_amount
    remaining_db = charity_db.full_amount - charity_db.invested_amount

    if remaining_obj > remaining_db:
        charity_obj.invested_amount += remaining_db
        charity_db = close_charity(charity_db)
    elif remaining_obj == remaining_db:
        charity_obj = close_charity(charity_obj)
        charity_db = close_charity(charity_db)
    else:
        charity_db.invested_amount += remaining_obj
        charity_obj = close_charity(charity_obj)

    return charity_obj, charity_db
