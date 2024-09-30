from typing import Sequence, Dict, Any

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import User
from .schemas import UserCreateM, UserPublicM, UserPrivateM
from .utils import bcrypt_context


async def create_user(session: AsyncSession, _user: UserCreateM) -> UserPrivateM:
    """
    Creates a new User with hashed password.
    Raise HTTPException if User already exists

    :param session: AsyncSession
    :param _user: UserCreateM
    :return: User object
    """
    _ = await session.execute(select(User).where(User.username == _user.username))
    _ = _.scalar_one_or_none()

    if _:
        raise HTTPException(status_code=400, detail='User already exists')

    _user.password = bcrypt_context.hash(_user.password)
    user = User(**_user.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserPrivateM.from_orm(user)


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


async def delete_user(session: AsyncSession, user_id) -> None:
    """
    Deletes a User by passed user_id

    :param session: AsyncSession
    :param user_id: int
    :return: None
    """
    user = await session.get(User, user_id)
    await session.delete(user)
    await session.commit()


async def update_user_password(session: AsyncSession, user_id, password) -> UserPrivateM:
    """
    Updates the password of a user.

    :param session: the database session.
    :param user_id: the id of the user to update.
    :param password: the new password.
    """
    user = await session.get(User, user_id)
    user.password = bcrypt_context.hash(password)
    await session.commit()
    return UserPrivateM.from_orm(user)
