# controllers/user.py

from database import fake_users
from utils import APIException

async def get_my_info(user: dict):
    """
    내 정보 조회 (세션 기반)
    """
    # 5. [403] 탈퇴한 회원 접근 금지 (get_current_user에서 처리되지 않았다면)
    if user.get("is_deleted") == True:
        raise APIException(code="FORBIDDEN", message="접근이 거부되었습니다.", status_code=403)

    return {
        "code": "GET_MY_INFO_SUCCESS",
        "message": "내 정보 조회 성공",
        "data": {
            "userId": user["userId"],
            "email": user["email"],
            "nickname": user["nickname"],
            "profileimage": user.get("profileimage")
        }
    }

async def get_user_by_id(user_id: int):
    """
    특정 사용자 정보 조회 (ID 기반)
    """
    # 3. 사용자 찾기
    matched_user = None
    for user in fake_users:
        if user["userId"] == user_id:
            matched_user = user
            break
    
    # 4. [404] 사용자 없음 (설계도: USER_NOT_FOUND)
    if matched_user is None:
        raise APIException(code="USER_NOT_FOUND", message="해당 사용자를 찾을 수 없습니다.", status_code=404)
        
    # (참고) 5. [403] 탈퇴한 회원 접근 금지
    if matched_user.get("is_deleted") == True:
        raise APIException(code="FORBIDDEN", message="접근이 거부되었습니다.", status_code=403)

    # 6. 성공 응답
    return {
        "code": "GET_USER_SUCCESS",
        "message": "사용자 정보 조회 성공",
        "data": {
            "userId": matched_user["userId"],
            "email": matched_user["email"],
            "nickname": matched_user["nickname"],
            "profileimage": matched_user.get("profileimage")
        }
    }