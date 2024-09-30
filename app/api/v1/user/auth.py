from typing import Annotated

from jose import jwt, JWTError
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import setting
from core.database import create_session, User

from .schemas import TokenM
from .utils import create_access_token, authenticate_user

router = APIRouter(prefix='/auth', tags=['Auth'])
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id = payload.get('id')
        username = payload.get('username')
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')
        return {'id': user_id, 'username': username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')


@router.post('/token', response_model=TokenM)
async def login_for_token(
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[create_session, Depends()]
):
    user: User = await authenticate_user(session, form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    token = await create_access_token(user.id, user.username, expired_in=timedelta(minutes=60))
    return TokenM(access_token=token, token_type='bearer')
