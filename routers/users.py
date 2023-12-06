from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from operations.users import UsersOperation
from schemas._input import UpdateUserProfileInput, UserInput

router = APIRouter()


@router.post("/")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body(),
):
    user = await UsersOperation(db_session).create(
        username=data.username,
        password=data.password,
    )
    return user


@router.get("/")
async def profile(db_session: Annotated[AsyncSession, Depends(get_db)], username: str):
    user_profile = await UsersOperation(db_session).get_user_by_username(username)

    return user_profile


@router.put("/")
async def update(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UpdateUserProfileInput = Body(),
):
    user_profile = await UsersOperation(db_session).update_username(
        old_username=data.old_username, new_username=data.new_username
    )

    return user_profile


@router.delete("/")
async def delete(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body(),
):
    delete_user = await UsersOperation(db_session).user_delete_account(
        data.username, data.password
    )
    return delete_user


@router.post("/login")
async def login(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body(),
):
    token = await UsersOperation(db_session).login(
        username=data.username, password=data.password
    )
    return token


@router.post("/logout")
async def logout():
    pass
