from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAdminDB, DonationCreate, DonationDB
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/', response_model=DonationDB,
    response_model_exclude_none=True)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    '''Сделать пожертвование.'''
    donation = await donation_crud.create(donation, session, user)
    await investing(session)
    await session.refresh(donation)
    return donation


@router.get(
    '/', response_model=list[DonationAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров.\n
    Возвращает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationDB])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_user(session=session, user=user)
