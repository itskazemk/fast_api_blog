import sqlalchemy as sa
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UsersOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str) -> User:
        user = User(username=username, password=password)

        async with self.db_session as session:
            session.add(user)
            await session.commit()

        return user

    async def get_user_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise ValidationError("user is none")

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
                raise ValidationError("user is none")

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
                raise ValidationError("user is none")

            await session.execute(delete_query)
            await session.commit()

            return f"User '{username}' Deleted!"
