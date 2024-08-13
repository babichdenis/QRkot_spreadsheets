from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBAll
from app.services.investment import investment_process


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создать пожертвование. Доступ: авторизованный пользователь."""
    donation_db = await donation_crud.create(
        obj_in=donation_in, session=session, user=user)
    charity_projects_db = await charity_project_crud.get_open_objects(session)
    if charity_projects_db:
        investment_process(
            target=donation_db,
            sources=charity_projects_db
        )
    await session.commit()
    await session.refresh(donation_db)
    return donation_db


@router.get(
    '/',
    response_model=list[DonationDBAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
):
    """Returns a list of all donations."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Returns a list of the user's donations."""
    return await donation_crud.get_by_user(session=session, user=user)
