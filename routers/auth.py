# routers/auth.py
from fastapi import APIRouter, status
from controllers.auth import auth_signup, auth_login, auth_logout, check_email_duplicate, check_nickname_duplicate
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

# [로그아웃]
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    return await auth_logout()

# [이메일 중복 확인]
# URL 예시: /v1/auth/check-email?email=test@test.com
@router.get("/check-email", status_code=status.HTTP_200_OK)
async def check_email(email: str):
    return await check_email_duplicate(email)

# [닉네임 중복 확인]
# URL 예시: /v1/auth/check-nickname?nickname=준수
@router.get("/check-nickname", status_code=status.HTTP_200_OK)
async def check_nickname(nickname: str):
    return await check_nickname_duplicate(nickname)