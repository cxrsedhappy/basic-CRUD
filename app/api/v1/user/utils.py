from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from core.database import User
from core.config import setting

from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(
            password={
                "tokenUrl": tokenUrl,
                "scopes": scopes}
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


async def authenticate_user(session: AsyncSession, username: str, password: str):
    statement = select(User).where(User.username == username)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.password):
        return False

    return user


async def create_access_token(user_id: int, username: str, expired_in: timedelta | None = None):
    encode = {'id': user_id, 'username': username}

    if not expired_in:
        expired_in = timedelta(minutes=30)

    encode.update({'exp': datetime.now() + expired_in})
    return jwt.encode(encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
