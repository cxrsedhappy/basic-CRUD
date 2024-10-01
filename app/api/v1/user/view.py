from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from core.database import create_session

from .auth import get_current_user
from .schemas import UserCreateM, UserPublicM, UserPrivateM, UserPasswordChangeM
from . import crud

router = APIRouter(prefix='/user', tags=['Users'])


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserPrivateM)
async def create_users(user: UserCreateM, session=Depends(create_session)):
    return await crud.create_user(session, user)

#  Wanted to add some more features but technical task says it's not needed. Ask me more about it in telegram.
#  @router.get('/me', response_model=UserPrivateM)
#  async def get_me(user=Depends(get_current_user), session=Depends(create_session)):
#      return await crud.get_my_user(session, user['id'])


@router.get('/{user_id}', response_model=UserPublicM)
async def get_user(user_id: int, session=Depends(create_session)):
    user = await crud.get_user_by_id(session, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id <{user_id}> not found')

    return user


@router.put('/{user_id}', response_model=UserPrivateM)
async def get_user(pwd_model: UserPasswordChangeM, user=Depends(get_current_user), session=Depends(create_session)):
    user = await crud.update_user_password(session, user['id'], pwd_model.password)
    return user


@router.delete('/{user_id}')
async def get_user(response: Response, user=Depends(get_current_user), session=Depends(create_session)):
    await crud.delete_user(session, user['id'])
    response.delete_cookie(key="access_token", httponly=True)
    return {'msg': f'User with id<{user["id"]}> deleted'}