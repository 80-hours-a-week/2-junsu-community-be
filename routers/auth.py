# routers/auth.py
from fastapi import APIRouter, status
from controllers.auth import auth_signup
from models.auth import SignupRequest

router = APIRouter(prefix="/v1/auth")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest):
    return await auth_signup(user_data)