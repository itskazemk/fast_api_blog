from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from fastapi import APIRouter, Body, Depends
from operations.users import UsersOperation
from schemas._input import RegisterInput, UpdateUserProfileInput

router = APIRouter()


@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: RegisterInput = Body(),
):
    user = await UsersOperation(db_session).create(
        username=data.username,
        password=data.password,
    )
    return user


@router.post("/login")
async def login():
    pass


@router.get("/{username}/")
async def profile(db_session: Annotated[AsyncSession, Depends(get_db)], username: str):
    user_profile = await UsersOperation(db_session).get_user_by_username(username)

    return user_profile


@router.put("/update")
async def update(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UpdateUserProfileInput = Body(),
):
    user_profile = await UsersOperation(db_session).update_username(
        old_username=data.old_username, new_username=data.new_username
    )

    return user_profile


@router.post("/logout")
async def logout():
    pass
