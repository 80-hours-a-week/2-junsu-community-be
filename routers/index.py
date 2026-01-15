from fastapi import APIRouter
from routers.session import router as session_router
from routers.post import router as post_router
from routers.comment import router as comment_router
from routers.user import router as user_router

router = APIRouter()
router.include_router(session_router)
router.include_router(user_router)
router.include_router(post_router)
router.include_router(comment_router)