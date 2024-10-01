__all__ = {
    'router'
}


from fastapi import APIRouter

from .user.view import router as user_router
from .post.view import router as post_router

router = APIRouter(prefix='/v1')
router.include_router(router=user_router)
router.include_router(router=post_router)
