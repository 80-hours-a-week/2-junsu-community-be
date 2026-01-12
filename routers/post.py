# routers/post.py

from fastapi import APIRouter, status
from controllers.post import get_posts_list

router = APIRouter(prefix="/v1/posts")

@router.get("", status_code=status.HTTP_200_OK)
async def get_posts(offset: int = 0, limit: int = 10):
    return await get_posts_list(offset, limit)