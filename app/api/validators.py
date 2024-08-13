from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_obj_exists_by_id(
        obj_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверить наличие объекта-БД по id."""
    charity_project_db = await charity_project_crud.get(
        obj_id=obj_id,
        session=session)
    if charity_project_db is None:
        raise HTTPException(
            status_code=404,
            detail='Проекта с указанным id не существует!')
    return charity_project_db


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    if await charity_project_crud.get_id_by_name(project_name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_project_by_id(
        charity_project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_active(
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_charity_project_invested(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_invested_amount(
    invested_amount: int,
    new_full_amount: int,
    session: AsyncSession
) -> None:
    if invested_amount < new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )


async def check_charity_project_before_edit(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Проверить проект перед редактированием."""
    project_db = await check_obj_exists_by_id(
        obj_id=project_id,
        session=session)
    if project_db.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!')
    if (project_in.full_amount and
            project_db.invested_amount > project_in.full_amount):
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить требуемую сумму меньше уже вложенной')
    await check_name_duplicate(
        obj_name=project_in.name,
        session=session)
    return project_db


async def check_charity_project_before_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверить проект: перед удалением."""
    charity_project_db = await check_obj_exists_by_id(
        obj_id=project_id,
        session=session)
    if charity_project_db.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!')
    if charity_project_db.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!')
    return charity_project_db
