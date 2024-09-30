from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import User
from .schemas import UserCreateM, UserPublicM, UserPrivateM
from .utils import bcrypt_context


async def create_user(session: AsyncSession, _user: UserCreateM):
    """
    Creates a new User with hashed password.

    :param session: AsyncSession
    :param _user: UserCreateM
    :return: User object
    """
    dump = _user.model_dump()
    dump['password'] = bcrypt_context.hash(dump['password'])
    user = User(**dump)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession) -> Sequence[User]:
    """
    Returns all Users in database

    :param session: AsyncSession
    :return: User object
    """
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return users


# async def get_my_user(session: AsyncSession, user_id) -> UserPrivateM | None:
#     """
#     Finds User by passed user_id
#
#     :param session: AsyncSession
#     :param user_id: int
#     :return: User object
#     """
#     me = await session.get(User, user_id)
#     return UserPrivateM.from_orm(me)


async def get_user_by_id(session: AsyncSession, user_id) -> UserPublicM | None:
    """
    Finds User by passed user_id

    :param session: AsyncSession
    :param user_id: int
    :return: User object
    """
    user = await session.get(User, user_id)
    if user is not None:
        return UserPublicM.from_orm(user)
    return None


async def delete_user(session: AsyncSession, user_id):
    """
    Deletes a User by passed user_id

    :param session: AsyncSession
    :param user_id: int
    :return: None
    """
    user = await session.get(User, user_id)
    await session.delete(user)
    await session.commit()


async def update_user_password(session: AsyncSession, user_id, password):
    """
    Updates the password of a user.

    :param session: the database session.
    :param user_id: the id of the user to update.
    :param password: the new password.
    """
    user = await session.get(User, user_id)
    user.password = bcrypt_context.hash(password)
    await session.commit()
    return user
