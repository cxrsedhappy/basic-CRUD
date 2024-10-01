from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import User, Post
from .schemas import PostM, PostCreateM


async def create_post(session: AsyncSession, _user_id: int, _post: PostCreateM) -> PostM:
    """
    Creates a new Post with passed user_id and _post

    :param session: AsyncSession
    :param _user_id: int
    :param _post: PostCreateM
    :return: PostM
    """
    new_post = Post(user_id=_user_id, text=_post.text)

    user = await session.get(User, _user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user.posts.append(new_post)
    await session.commit()

    return PostM.from_orm(new_post)


async def get_users_post(session: AsyncSession, user_id) -> list[PostM]:
    """
    Finds all posts of a user by passed user_id

    :param session: AsyncSession
    :param user_id: int
    :return: list of PostM objects
    """
    user = await session.get(User, user_id)
    return [PostM.from_orm(post) for post in user.posts]


async def update_post(session: AsyncSession, post_id: int, text: str) -> PostM:
    """
    Updates the post with the given post_id

    :param session: AsyncSession
    :param post_id: int
    :param text: str
    :return: PostM
    """
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    post.text = text
    await session.commit()
    return PostM.from_orm(post)


async def delete_post(session: AsyncSession, post_id) -> None:
    """
    Deletes a Post by passed post_id

    :param session: AsyncSession
    :param post_id: int
    :return: None
    """
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    await session.delete(post)
    await session.commit()
