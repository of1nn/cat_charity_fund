from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.crud import charity_project_crud
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_project_update,
    check_project_delete,
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[
        Depends(current_superuser),
    ],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    old_project = await check_project_exists(charity_project_id, session)
    await check_name_duplicate(charity_project.name, session)
    await check_project_update(old_project, charity_project)
    project = await charity_project_crud.update(
        old_project, charity_project, session
    )
    return project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[
        Depends(current_superuser),
    ],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(charity_project_id, session)
    await check_project_delete(project)
    project = await charity_project_crud.remove(project, session)
    return project
