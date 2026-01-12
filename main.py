# main.py

from fastapi import FastAPI
# routers 폴더의 post 파일 안에 있는 router 변수를 가져와서 post_router라고 부르겠다.
from routers.post import router as post_router 

app = FastAPI(title="Community API - Task 2-1")

# [라우터 연결]
app.include_router(post_router)

@app.get("/")
async def root():
    return {"message": "Community Server is Running!"}