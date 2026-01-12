# models/auth.py

from pydantic import BaseModel
from typing import Optional

# [회원가입 요청 데이터 규격]
# 이 클래스가 있어야 컨트롤러가 데이터를 검사할 수 있습니다.
class SignupRequest(BaseModel):
    email: str        # 필수
    password: str     # 필수
    nickname: str     # 필수
    profileimage: Optional[str] = None # 선택