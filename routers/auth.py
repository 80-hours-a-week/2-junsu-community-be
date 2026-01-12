# routers/auth.py
from fastapi import APIRouter, status
from controllers.auth import auth_signup, auth_login
from models.auth import SignupRequest, LoginRequest

router = APIRouter(prefix="/v1/auth")
# [회원가입]
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest):
    return await auth_signup(user_data)

# [로그인]
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data: LoginRequest):
    return await auth_login(login_data)