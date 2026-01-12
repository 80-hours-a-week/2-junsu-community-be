# controllers/post.py

from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime
from database import fake_posts
from models.post import CreatePostRequest

# ==========================================
# 1. 게시글 목록 조회 (원래 있던 친구)
# ==========================================
async def get_posts_list(offset: int, limit: int):
    
    # 데이터 슬라이싱
    paginated_posts = fake_posts[offset : offset + limit]
    
    return {
        "code": "GET_POSTS_SUCCESS",
        "message": "게시글 목록을 성공적으로 불러왔습니다.",
        "data": {
            "posts": paginated_posts,
            "totalCount": len(fake_posts)
        }
    }

# ==========================================
# 2. 게시글 작성 (새로 온 친구 - fileUrl 포함)
# ==========================================
async def create_post(post_data: CreatePostRequest):
    
    # 1. ID 생성
    new_id = 1
    if len(fake_posts) > 0:
        new_id = fake_posts[-1]["postId"] + 1
        
    # 2. 시간 생성
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    # 3. 데이터 조립 (설계도 fileUrl 반영)
    new_post = {
        "postId": new_id,
        "title": post_data.title,
        "content": post_data.content,
        "fileUrl": post_data.fileUrl, # 파일 URL 추가됨
        "writer": post_data.writer,
        "viewCount": 0,
        "createdAt": current_time
    }
    
    # 4. 저장
    fake_posts.append(new_post)
    
    return {
        "code": "post_created",
        "data": {
            "post_id": new_id
        }
    }