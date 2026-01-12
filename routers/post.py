# routers/post.py

from fastapi import APIRouter, status
# 방금 만든 요리사(컨트롤러)를 데려옵니다.
from controllers.post import get_posts_list

# 주소 앞에 자동으로 "/v1/posts"가 붙습니다.
router = APIRouter(prefix="/v1/posts")

@router.get("", status_code=status.HTTP_200_OK)
async def get_posts(offset: int = 0, limit: int = 10):
    """
    게시글 목록 조회 라우터
    - 사용자가 /v1/posts?offset=0&limit=10 으로 요청하면 실행됩니다.
    """
    # 컨트롤러에게 일을 시키고 결과를 바로 손님에게 줍니다.
    return await get_posts_list(offset, limit)