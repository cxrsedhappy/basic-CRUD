from typing import Annotated

from jose import jwt, JWTError
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response

from core.config import setting
from core.database import create_session, User

from .schemas import TokenM, UserCreateM
from .utils import OAuth2PasswordBearerWithCookie, create_access_token, authenticate_user
from .crud import create_user

router = APIRouter(prefix='/auth', tags=['Auth'])
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id = payload.get('id')
        username = payload.get('username')

        if user_id is None or username is None:
            raise credentials_exception

        return {'id': user_id, 'username': username}
    except JWTError:
        raise credentials_exception


@router.post('/token')
async def login_for_token(
        response: Response,
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[create_session, Depends()]
):
    user: User = await authenticate_user(session, form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    access_token = await create_access_token(
        user.id,
        user.username,
        expired_in=timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return TokenM(access_token=access_token, token_type='bearer')


@router.post('/register')
async def register_user(
        user: UserCreateM,
        session: Annotated[create_session, Depends()],
):
    new_user = await create_user(session, user)

    token = await create_access_token(new_user.id, new_user.username, expired_in=timedelta(minutes=60))
    return {'message': 'User created successfully', 'auth_token': token}
