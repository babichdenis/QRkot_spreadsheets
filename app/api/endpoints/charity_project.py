from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_active,
                                check_charity_project_exists,
                                check_charity_project_invested,
                                check_charity_project_invested_amount,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud import charity_project_crud, donation_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создать проект. Доступ: суперпользователь."""
    await check_name_duplicate(
        obj_name=charity_project_in.name,
        session=session)
    charity_project_db = await charity_project_crud.create(
        obj_in=charity_project_in,
        session=session)
    donations_db = await donation_crud.get_open_objects(session)
    if donations_db:
        investment_process(
            target=charity_project_db,
            sources=donations_db)
    await session.commit()
    await session.refresh(charity_project_db)
    return charity_project_db


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a list of all projects."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        charity_project_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Редактировать проект. Доступ: суперпользователь."""
    charity_project_db = await check_charity_project_before_edit(
        project_id=project_id,
        charity_project_in=charity_project_in,
        session=session)
    charity_project_db = await charity_project_crud.update(
        db_obj=charity_project_db,
        obj_in=charity_project_in,
        session=session)
    return charity_project_db
# @router.patch(
#     '/{project_id}',
#     response_model=CharityProjectDB,
#     dependencies=[Depends(current_superuser)],
# )
# async def partially_update_charity_project(
#     project_id: int,
#     obj_in: CharityProjectUpdate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Only to superuser. Updates the object of the charity project."""
#     charity_project = await check_charity_project_exists(
#         project_id,
#         session
#     )
#     charity_project = await check_charity_project_active(
#         charity_project,
#         session
#     )
#     if obj_in.name:
#         await check_name_duplicate(obj_in.name, session)
#     if not obj_in.full_amount:
#         return await charity_project_crud.update(
#             charity_project,
#             obj_in,
#             session
#         )
#     await check_charity_project_invested_amount(
#         obj_in.full_amount,
#         charity_project.invested_amount,
#         session
#     )
#     return await process_donation(await charity_project_crud.update(
#         charity_project, obj_in, session), [Donation])


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Only to superuser. Deletes the project."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_invested(charity_project, session)
    return await charity_project_crud.remove(charity_project, session)
