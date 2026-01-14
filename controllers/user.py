# controllers/user.py

from fastapi import status
from fastapi.responses import JSONResponse
from database import fake_users 

async def get_user_info(email: str):
    """
    사용자 정보 조회 로직
    - 이메일을 받아서 fake_users에서 찾은 뒤 정보를 반환
    """
    
    # 1. 사용자 찾기
    matched_user = None
    for user in fake_users:
        if user["email"] == email:
            matched_user = user
            break
    
    # 2. 없으면 404 에러 (Not Found)
    if matched_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": "USER_NOT_FOUND",
                "message": "해당 사용자를 찾을 수 없습니다.",
                "data": None
            }
        )

    # 3. 있으면 성공
    return {
        "code": "GET_USER_SUCCESS",
        "message": "사용자 정보 조회 성공",
        "data": {
            "email": matched_user["email"],
            "nickname": matched_user["nickname"],
            "profileimage": matched_user.get("profileimage") # 없으면 None
        }
    }