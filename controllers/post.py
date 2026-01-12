# controllers/post.py

# 냉장고에서 데이터를 가져옵니다.
from database import fake_posts

# 함수 이름은 보통 '동사_명사' 형태로 짓습니다.
async def get_posts_list(offset: int, limit: int):
    
    # 1. 데이터 슬라이싱 (페이징 처리)
    # 리스트[시작 : 끝]
    paginated_posts = fake_posts[offset : offset + limit]
    
    # 2. 결과 반환 (단순한 딕셔너리 구조)
    return {
        "code": "GET_POSTS_SUCCESS",
        "message": "게시글 목록을 성공적으로 불러왔습니다.",
        "data": {
            "posts": paginated_posts,
            "totalCount": len(fake_posts)
        }
    }