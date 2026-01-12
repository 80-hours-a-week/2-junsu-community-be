# models/auth.py

from pydantic import BaseModel
from typing import Optional

# [회원가입]
class SignupRequest(BaseModel):
    email: str
    password: str
    nickname: str
    profileimage: Optional[str] = None

# [로그인]
class LoginRequest(BaseModel):
    email: str
    password: str