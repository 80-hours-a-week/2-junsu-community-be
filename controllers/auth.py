from fastapi import Response, status
from fastapi.responses import JSONResponse
import uuid  # 세션 ID 생성용
import re
from database import fake_users, fake_sessions
from models.auth import SignupRequest, LoginRequest

async def auth_signup(user_data: SignupRequest):
    # 필수값, 정규식 체크 생략 (이전과 동일하게 구현했다고 가정)
    # 중복 체크
    for user in fake_users:
        if user["email"] == user_data.email:
            return JSONResponse(status_code=409, content={"code": "DUPLICATE", "message": "이미 가입된 이메일"})

    new_id = len(fake_users) + 1
    new_user = user_data.model_dump()
    new_user["userId"] = new_id
    fake_users.append(new_user)
    
    return {"code": "SIGNUP_SUCCESS", "message": "회원가입 완료", "data": None}

async def auth_login(response: Response, login_data: LoginRequest):
    user = next((u for u in fake_users if u["email"] == login_data.email and u["password"] == login_data.password), None)
    
    if not user:
        return JSONResponse(status_code=400, content={"code": "LOGIN_FAIL", "message": "정보 불일치"})

    # [중요] 세션 생성 및 쿠키 굽기
    session_id = str(uuid.uuid4())
    fake_sessions[session_id] = user["email"]
    
    # 쿠키 설정 (HttpOnly로 보안 강화)
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    return {"code": "LOGIN_SUCCESS", "message": "로그인 성공", "data": {"email": user["email"]}}

async def auth_logout(response: Response, session_id: str):
    # 세션 삭제
    if session_id in fake_sessions:
        del fake_sessions[session_id]
    
    # 쿠키 삭제
    response.delete_cookie("session_id")
    return {"code": "LOGOUT_SUCCESS", "message": "로그아웃 성공", "data": None}