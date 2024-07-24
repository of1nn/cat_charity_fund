from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект не найден!',
        )
    return project


async def check_project_update(
    project: CharityProject,
    new_project: CharityProjectUpdate,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if (
        new_project.full_amount and
        project.invested_amount > new_project.full_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нелья установить значение '
                'full_amount меньше уже вложенной суммы.'
            ),
        )
    elif (
        new_project.full_amount and
        project.invested_amount == new_project.full_amount
    ):
        project.fully_invested = True
        project.close_date = datetime.now()


async def check_project_delete(
    project: CharityProject,
) -> None:
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'В проект были внесены средства, ' 'не подлежит удалению!'
            ),
        )
