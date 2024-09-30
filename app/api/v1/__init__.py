__all__ = {
    'router'
}


from fastapi import APIRouter

from .user.view import router as user_router

router = APIRouter(prefix='/v1')
router.include_router(router=user_router)