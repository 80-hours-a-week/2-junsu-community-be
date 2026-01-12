# controllers/auth.py

from fastapi import status
from fastapi.responses import JSONResponse
import re
from database import fake_users 
from models.auth import SignupRequest, LoginRequest

# ==========================================
# 1. 회원가입
# ==========================================
async def auth_signup(user_data: SignupRequest):
    
    # 필수값 검증
    if user_data.email == "" or user_data.password == "" or user_data.nickname == "":
        return JSONResponse(status_code=400, content={
            "code": "REQUIRED_FIELDS_MISSING",
            "message": "필수 입력 항목이 누락되었습니다.",
            "data": None
        })

    # 이메일 형식
    if re.match(r'^[a-zA-Z0-9+_\-.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', user_data.email) is None:
        return JSONResponse(status_code=400, content={
            "code": "INVALID_EMAIL_FORMAT",
            "message": "이메일 형식이 올바르지 않습니다.",
            "data": None
        })

    # 비밀번호 형식
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$', user_data.password) is None:
        return JSONResponse(status_code=400, content={
            "code": "WEAK_PASSWORD",
            "message": "비밀번호는 영문, 숫자, 특수문자 포함 8~20자여야 합니다.",
            "data": None
        })

    # 이메일 중복 체크 (가입 시점)
    for user in fake_users:
        if user["email"] == user_data.email:
            return JSONResponse(status_code=409, content={
                "code": "ALREADY_EXIST_EMAIL",
                "message": "이미 가입된 이메일입니다.",
                "data": None
            })

    # 저장
    fake_users.append(user_data.model_dump())
    
    return {
        "code": "SIGNUP_SUCCESS",
        "message": "회원가입이 완료되었습니다.",
        "data": None  # [설계도 준수] 성공 시 데이터는 null
    }

# ==========================================
# 2. 로그인
# ==========================================
async def auth_login(login_data: LoginRequest):
    
    matched_user = None
    for user in fake_users:
        if user["email"] == login_data.email:
            matched_user = user
            break
    
    if matched_user is None or matched_user["password"] != login_data.password:
        return JSONResponse(status_code=400, content={
            "code": "LOGIN_FAILED",
            "message": "이메일 또는 비밀번호가 일치하지 않습니다.",
            "data": None
        })

    # [중요] 강사님 지시(세션X)로 토큰은 발급하지 않지만,
    # 응답 포맷은 최대한 설계도와 비슷하게 유지합니다.
    return {
        "code": "LOGIN_SUCCESS",
        "message": "로그인에 성공했습니다.",
        "data": {
            "userId": matched_user.get("id", 1), # ID가 없으면 임시로 1
            "email": matched_user["email"]
        }
    }

# ==========================================
# 3. 로그아웃
# ==========================================
async def auth_logout():
    return {
        "code": "LOGOUT_SUCCESS",
        "message": "로그아웃 되었습니다.",
        "data": None
    }

# ==========================================
# 4. 중복 체크 (설계도 포맷 적용)
# ==========================================
async def check_email_duplicate(email: str):
    is_exist = False
    for user in fake_users:
        if user["email"] == email:
            is_exist = True
            break
    
    if is_exist:
        return JSONResponse(status_code=409, content={
            "code": "DUPLICATE_EMAIL",
            "message": "이미 사용 중인 이메일입니다.",
            "data": {"available": False}
        })
        
    return {
        "code": "AVAILABLE_EMAIL",
        "message": "사용 가능한 이메일입니다.",
        "data": {"available": True}
    }

async def check_nickname_duplicate(nickname: str):
    is_exist = False
    for user in fake_users:
        if user["nickname"] == nickname:
            is_exist = True
            break
            
    if is_exist:
        return JSONResponse(status_code=409, content={
            "code": "DUPLICATE_NICKNAME",
            "message": "이미 사용 중인 닉네임입니다.",
            "data": {"available": False}
        })
        
    return {
        "code": "AVAILABLE_NICKNAME",
        "message": "사용 가능한 닉네임입니다.",
        "data": {"available": True}
    }