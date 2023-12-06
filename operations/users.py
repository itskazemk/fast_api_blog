import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from schemas._output import Register_DeleteOutput
from utils.secrets import password_manager

SECRET_KEY = "329d31dc41075cd99289628312e25fd80768999075125b6f1f74b1c82ed6390c"
ALGORITHM = "HS526"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UsersOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str) -> Register_DeleteOutput:
        user_pwd = password_manager.hash(password)
        user = User(username=username, password=user_pwd)
        # check_user_exist_query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            # user_check = await session.scalar(check_user_exist_query)

            # if user_check:
            # raise HTTPException(status_code=409, detail="user exist")
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise HTTPException(status_code=409, detail="user exist")

        return Register_DeleteOutput(id=user.id, username=user.username)

    async def get_user_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise HTTPException(status_code=404, detail="user doesn't exist")

            return user_data

    async def update_username(self, old_username: str, new_username: str) -> User:
        query = sa.select(User).where(User.username == old_username)

        update_query = (
            sa.update(User)
            .where(User.username == old_username)
            .values(username=new_username)
        )

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise HTTPException(status_code=404, detail="user doesn't exist")

            await session.execute(update_query)
            await session.commit()

            user_data.username = new_username
            return user_data

    async def user_delete_account(self, username, password) -> str:
        delete_query = sa.delete(User).where(
            User.username == username, User.password == password
        )
        user_query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise HTTPException(status_code=404, detail="user doesn't exist")

            await session.execute(delete_query)
            await session.commit()

            return f"User '{username}' Deleted!"
