from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from core.database import User
from core.config import setting


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def authenticate_user(session: AsyncSession, username: str, password: str):
    statement = select(User).where(User.username == username)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.password):
        return False

    return user


async def create_access_token(user_id: int, username: str, expired_in: timedelta):
    encode = {'id': user_id, 'username': username}
    encode.update({'exp': datetime.now() + expired_in})
    return jwt.encode(encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)