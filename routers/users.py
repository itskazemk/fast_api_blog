from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from fastapi import APIRouter, Body, Depends
from operations.users import UsersOperation
from schemas._input import RegisterInput

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


@router.get("/")
async def profile():
    pass


@router.put("/update")
async def update():
    pass


@router.post("/logout")
async def logout():
    pass
