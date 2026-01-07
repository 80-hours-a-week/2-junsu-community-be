from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class UserData(BaseModel):
    name: str
    age: int
    email: str

@app.post("/submit")
def create_user(user: UserData):
    return {
        "status": "success",
        "message": f"{user.name}님의 데이터를 성공적으로 받았습니다.",
        "received_data": user
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)