from fastapi import FastAPI, status, Request, HTTPException # HTTPException 추가 필요
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional, List
import re  # 이메일, 비밀번호 정규식 검증용

app = FastAPI(title="Community API - Task 2-1")

# ==========================================
# 1. [Models] 요청 데이터 규격 (클래스 정의부)
# ==========================================

# [회원가입 전용 클래스] - 설계도(CSV) 반영
class SignupRequest(BaseModel):
    email: str        # 필수
    password: str     # 필수
    nickname: str     # 필수
    profileimage: Optional[str] = None # 선택

# (참고: 게시글 조회의 경우 GET 방식이므로 별도의 클래스 없이 
#  함수 인자의 offset, limit으로 처리하는 것이 더 효율적입니다.)

# [설정] 세션 미들웨어 추가 (이 코드가 없으면 로그인이 안 됩니다!)
# secret_key는 암호화에 쓰이는 비밀번호입니다.
# 실무에서는 환경변수로 관리
app.add_middleware(SessionMiddleware, secret_key="your-secret-session-key")

# [로그인 전용 클래스]
class LoginRequest(BaseModel):
    email: str
    password: str

# ==========================================
# 2. [Mock Data] 가짜 데이터베이스 (데이터 저장소)
# ==========================================

# 게시글 데이터 (기존 코드 유지)
fake_posts = [
    {"postId": 1, "title": "안녕하세요, 첫 글입니다!", "writer": "준수", "viewCount": 10, "createdAt": "2026-01-12T10:00:00Z"},
    {"postId": 2, "title": "영상 디자인에서 AI로 전향 중이에요", "writer": "준수", "viewCount": 25, "createdAt": "2026-01-12T10:05:00Z"},
    {"postId": 3, "title": "FastAPI 생각보다 재밌네요", "writer": "테스터", "viewCount": 5, "createdAt": "2026-01-12T11:00:00Z"},
    {"postId": 4, "title": "AWS AI School 2기 파이팅", "writer": "동기", "viewCount": 100, "createdAt": "2026-01-12T12:00:00Z"},
]

# 유저 데이터 (회원가입 시 여기에 저장됩니다)
fake_users = []


# ==========================================
# 3. [Routes - Posts] 게시글 관련 기능 (구현부)
# ==========================================

@app.get("/v1/posts")
async def get_posts(offset: int = 0, limit: int = 10):
    """설계도 반영: 게시글 목록 페이징 조회"""
    paginated_posts = fake_posts[offset : offset + limit]
    return {
        "code": "GET_POSTS_SUCCESS",
        "message": "게시글 목록을 성공적으로 불러왔습니다.",
        "data": {
            "posts": paginated_posts,
            "totalCount": len(fake_posts)
        }
    }

# ==========================================
# 4. [Routes - Auth] 회원가입 기능 (강사님 피드백: 부정문 제거)
# ==========================================

# ... (위쪽 import 및 모델 정의는 동일) ...

@app.post("/v1/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest):
    """
    설계도 반영: 회원가입 (ChatGPT 피드백 반영 완료)
    """
    
    # 1. 필수값 누락 검증 (빈 문자열)
    if user_data.email == "" or user_data.password == "" or user_data.nickname == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "REQUIRED_FIELDS_MISSING",
                "message": "이메일, 비밀번호, 닉네임은 필수입니다.",
                "data": None
            }
        )

    # 2. 이메일 형식 검증 (하이픈 이스케이프 처리 \- 추가)
    email_regex = r'^[a-zA-Z0-9+_\-.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    match_result = re.match(email_regex, user_data.email)
    
    if match_result is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "INVALID_EMAIL_FORMAT",
                "message": "유효하지 않은 이메일 형식입니다.",
                "data": None
            }
        )

    # 3. 비밀번호 강도 검증
    pw_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
    pw_match_result = re.match(pw_regex, user_data.password)
    
    if pw_match_result is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "WEAK_PASSWORD",
                "message": "비밀번호는 영문, 숫자, 특수문자 포함 8~20자여야 합니다.",
                "data": None
            }
        )

    # 4. 중복 이메일 체크
    is_duplicate = False
    for user in fake_users:
        # 딕셔너리 접근 방식은 그대로 유지
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

    # 5. 저장 및 성공 응답 (수정: .dict() -> .model_dump())
    fake_users.append(user_data.model_dump())
    
    return {
        "code": "SIGNUP_SUCCESS",
        "message": "회원가입이 완료되었습니다.",
        "data": {
            "nickname": user_data.nickname,
            "email": user_data.email
        }
    }

# ==========================================
# 5. [Routes - Login] 로그인 기능 (설계도 완벽 반영)
# ==========================================

@app.post("/v1/auth/login", status_code=status.HTTP_200_OK)
async def login(request: Request, login_data: LoginRequest):
    """
    설계도 반영: 로그인 (세션 방식)
    - 성공 (200): LOGIN_SUCCESS
    - 실패 (400): LOGIN_FAILED (이메일 없음 또는 비밀번호 불일치)
    """
    
    # 1. 사용자 조회 (이메일로 찾기)
    matched_user = None
    for user in fake_users:
        if user["email"] == login_data.email:
            matched_user = user
            break
    
    # 2. 예외 처리: 사용자가 없거나(None) 비밀번호가 틀린 경우(!=)
    # 설계도상 '로그인 실패'는 보통 400 Bad Request로 처리합니다.
    if matched_user is None or matched_user["password"] != login_data.password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "LOGIN_FAILED",
                "message": "이메일 또는 비밀번호가 일치하지 않습니다.",
                "data": None
            }
        )

    # 3. [세션 생성] 로그인 성공 처리
    request.session["user_email"] = matched_user["email"]
    request.session["user_nickname"] = matched_user["nickname"]
    
    # 4. 성공 응답 반환
    return {
        "code": "LOGIN_SUCCESS",
        "message": "로그인에 성공했습니다.",
        "data": {
            "email": matched_user["email"],
            "nickname": matched_user["nickname"]
        }
    }


# ==========================================
# 6. [Routes - Logout] 로그아웃 기능 (설계도 완벽 반영)
# ==========================================

@app.post("/v1/auth/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):
    """
    설계도 반영: 로그아웃
    - 성공 (200): LOGOUT_SUCCESS
    - 실패 (401): UNAUTHORIZED_ACCESS (로그인 상태가 아님)
    """
    
    # 1. 세션 확인 (로그인 여부 검사)
    user_email = request.session.get("user_email")
    
    # 2. 예외 처리: 세션 정보가 없는 경우 (로그인 안 함)
    # 설계도에 명시된 401 Unauthorized 에러를 반환합니다.
    if user_email is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "code": "UNAUTHORIZED_ACCESS",
                "message": "로그인이 필요한 기능입니다.",
                "data": None
            }
        )
    
    # 3. 로그아웃 처리 (세션 삭제)
    request.session.clear()
    
    # 4. 성공 응답 반환
    return {
        "code": "LOGOUT_SUCCESS",
        "message": "로그아웃 되었습니다.",
        "data": None
    }