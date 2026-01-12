from fastapi import FastAPI
from typing import List, Dict, Any

app = FastAPI(title="Community API - Task 2-1")

# --- 설계도 기반 가짜 데이터 (Model 역할을 대신함) ---
fake_posts = [
    {"postId": 1, "title": "안녕하세요, 첫 글입니다!", "writer": "준수", "viewCount": 10, "createdAt": "2026-01-12T10:00:00Z"},
    {"postId": 2, "title": "영상 디자인에서 AI로 전향 중이에요", "writer": "준수", "viewCount": 25, "createdAt": "2026-01-12T10:05:00Z"},
    {"postId": 3, "title": "FastAPI 생각보다 재밌네요", "writer": "테스터", "viewCount": 5, "createdAt": "2026-01-12T11:00:00Z"},
    {"postId": 4, "title": "AWS AI School 2기 파이팅", "writer": "동기", "viewCount": 100, "createdAt": "2026-01-12T12:00:00Z"},
]

# ==========================================
# 1. 게시글 목록 조회 (GET /v1/posts)
# ==========================================
@app.get("/v1/posts")
async def get_posts(offset: int = 0, limit: int = 10):
    """
    설계도 반영: 게시글 목록을 페이징하여 조회합니다.
    """
    # 1. 페이징 로직 (리스트 슬라이싱)
    paginated_posts = fake_posts[offset : offset + limit]
    
    # 2. 설계도 규격에 맞춘 응답 반환 (status 필드 제외)
    return {
        "code": "GET_POSTS_SUCCESS",
        "message": "게시글 목록을 성공적으로 불러왔습니다.",
        "data": {
            "posts": paginated_posts,
            "totalCount": len(fake_posts)
        }
    }