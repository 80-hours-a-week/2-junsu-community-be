from fastapi import APIRouter
from routers.post import router as post_router
from routers.auth import router as auth_router
# 나중에 user_router, comment_router 등등 생기면 여기서 불러옵니다.

# [통합 라우터 생성]
# 이 router 변수 하나에 모든 기능이 담깁니다.
router = APIRouter()

# [하위 라우터 연결]
router.include_router(post_router)
router.include_router(auth_router)