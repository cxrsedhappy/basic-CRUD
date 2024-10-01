from fastapi import APIRouter, Depends, status

from core.database import create_session

from .schemas import PostM, PostCreateM
from . import crud
from ..user.auth import get_current_user

router = APIRouter(prefix='/post', tags=['Posts'])


@router.post('', status_code=status.HTTP_201_CREATED, response_model=PostM)
async def create_post(post: PostCreateM, user=Depends(get_current_user), session=Depends(create_session)) -> PostM:
    return await crud.create_post(session, user['id'], post)


@router.get('/{user_id}', response_model=list[PostM])
async def get_user_posts(user_id: int, session=Depends(create_session)) -> list[PostM]:
    return await crud.get_users_post(session, user_id)


@router.put('/{post_id}', response_model=PostM)
async def update_post(post_id: int, post: PostCreateM, user=Depends(get_current_user), session=Depends(create_session)) -> PostM:
    return await crud.update_post(session, post_id, post.text)


@router.delete('/{post_id}')
async def delete_post(post_id: int, user=Depends(get_current_user), session=Depends(create_session)) -> dict[str, str]:
    await crud.delete_post(session, post_id)
    return {'message': 'Post deleted'}
