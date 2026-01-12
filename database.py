# database.py

# 원래 main.py에 있던 리스트들입니다.
# 서버가 켜져 있는 동안 데이터가 유지되는 메모리 공간입니다.

fake_users = []

fake_posts = [
    {"postId": 1, "title": "안녕하세요, 첫 글입니다!", "writer": "준수", "viewCount": 10, "createdAt": "2026-01-12T10:00:00Z"},
    {"postId": 2, "title": "영상 디자인에서 AI로 전향 중이에요", "writer": "준수", "viewCount": 25, "createdAt": "2026-01-12T10:05:00Z"},
    {"postId": 3, "title": "FastAPI 생각보다 재밌네요", "writer": "테스터", "viewCount": 5, "createdAt": "2026-01-12T11:00:00Z"},
    {"postId": 4, "title": "AWS AI School 2기 파이팅", "writer": "동기", "viewCount": 100, "createdAt": "2026-01-12T12:00:00Z"},
]