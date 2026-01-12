from fastapi import status
from fastapi.responses import JSONResponse
import re

# 가짜 DB와 모델 가져오기
from database import fake_users 
from models.auth import SignupRequest

async def auth_signup(user_data: SignupRequest):
    """
    회원가입 비즈니스 로직 (요리사)
    """
    
    # 1. 필수값 누락 검증 (명시적 확인)
    # "만약 하나라도 비어있다면" -> 에러
    if user_data.email == "" or user_data.password == "" or user_data.nickname == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "REQUIRED_FIELDS_MISSING",
                "message": "모든 항목을 입력해주세요.",
                "data": None
            }
        )

    # 2. 이메일 형식 검증
    # "매치되는 게 없으면(None)" -> 에러
    email_regex = r'^[a-zA-Z0-9+_\-.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, user_data.email) is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "INVALID_EMAIL_FORMAT",
                "message": "이메일 형식이 올바르지 않습니다.",
                "data": None
            }
        )

    # 3. 비밀번호 강도 검증 (추가된 부분)
    pw_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
    if re.match(pw_regex, user_data.password) is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "WEAK_PASSWORD",
                "message": "비밀번호는 영문, 숫자, 특수문자 포함 8~20자여야 합니다.",
                "data": None
            }
        )

    # 4. 중복 이메일 체크 (반복문 사용)
    is_duplicate = False
    for user in fake_users:
        if user["email"] == user_data.email:
            is_duplicate = True
            break
            
    if is_duplicate is True:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": "ALREADY_EXIST_EMAIL",
                "message": "이미 가입된 이메일입니다.",
                "data": None
            }
        )

    # 5. 저장 (메모리에 추가)
    fake_users.append(user_data.model_dump())
    
    return {
        "code": "SIGNUP_SUCCESS",
        "message": "회원가입 완료",
        "data": {
            "email": user_data.email,
            "nickname": user_data.nickname
        }
    }