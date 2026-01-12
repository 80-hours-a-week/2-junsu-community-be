# models/post.py

from pydantic import BaseModel
from typing import Optional

class CreatePostRequest(BaseModel):
    title: str       # 필수
    content: str     # 필수
    writer: str      # (세션 대용으로 필수)
    fileUrl: Optional[str] = None  # [설계도 반영] 이미지 주소 추가