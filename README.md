# 🚀 아무 말 대잔치 - 커뮤니티 백엔드 API

> FastAPI 기반 커뮤니티 게시판 RESTful API 서버입니다.

<br>

## 📖 목차

- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#️-설치-및-실행)
- [API 명세](#-api-명세)
  - [인증 API](#-인증-api-v1auth)
  - [게시글 API](#-게시글-api-v1posts)
  - [댓글 API](#-댓글-api-v1postspost_idcomments)
  - [사용자 API](#-사용자-api-v1users)
  - [파일 API](#-파일-api-v1files)
- [데이터베이스](#️-데이터베이스)
- [에러 처리](#-에러-처리)
- [관련 저장소](#-관련-저장소)

<br>

---

## 🛠 기술 스택

| 구분 | 기술 |
|:---:|:---|
| **Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) |
| **Language** | ![Python](https://img.shields.io/badge/Python_3.9+-3776AB?style=flat&logo=python&logoColor=white) |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) |
| **Validation** | ![Pydantic](https://img.shields.io/badge/Pydantic_V2-E92063?style=flat&logo=pydantic&logoColor=white) |
| **Auth** | 세션 기반 인증 (쿠키) |

<br>

---

## 📁 프로젝트 구조

```
📦 2-junsu-community-be
├── 📂 controllers            # 비즈니스 로직
│   ├── auth.py               # 인증 로직 (로그인, 회원가입 등)
│   ├── post.py               # 게시글 CRUD, 좋아요
│   ├── comment.py            # 댓글 CRUD
│   ├── user.py               # 사용자 정보 관리
│   └── file.py               # 파일 업로드
│
├── 📂 routers                # API 라우터 (엔드포인트 정의)
│   ├── index.py              # 라우터 통합
│   ├── auth.py               # /v1/auth/*
│   ├── post.py               # /v1/posts/*
│   ├── comment.py            # /v1/posts/{id}/comments/*
│   ├── user.py               # /v1/users/*
│   └── file.py               # /v1/files/*
│
├── 📂 models                 # Pydantic 모델 (Request/Response)
│   ├── __init__.py
│   ├── user.py               # UserCreate, UserLogin, UserUpdate
│   ├── post.py               # PostCreate, PostUpdate
│   ├── comment.py            # CommentCreate, CommentUpdate
│   └── file.py               # FileUploadResponse
│
├── 📂 uploads                # 업로드된 이미지 저장소
│
├── 📄 main.py                # FastAPI 앱 진입점
├── 📄 database.py            # MySQL 연결 설정
├── 📄 dependencies.py        # 의존성 주입 (인증 등)
├── 📄 utils.py               # 유틸리티 (커스텀 예외 등)
├── 📄 pyproject.toml         # 프로젝트 설정 및 의존성
└── 📄 bulk_insert.sql        # 테스트 데이터 삽입 스크립트
```

<br>

---

## ⚙️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/hahark-ops/2-junsu-community-be.git
cd 2-junsu-community-be
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -e .
```

### 4. 데이터베이스 설정
```sql
-- MySQL에서 실행
CREATE DATABASE community_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

`database.py`에서 DB 연결 정보 수정:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "community_db",
}
```

### 5. 서버 실행
```bash
uvicorn main:app --reload --port 8000
```

### 6. API 문서 확인
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

<br>

---

## 📚 API 명세

> 모든 응답은 아래 형식을 따릅니다:
> ```json
> {
>   "code": "success",
>   "message": "요청 성공",
>   "data": { ... }
> }
> ```

---

### 🔐 인증 API (`/v1/auth`)

| Method | Endpoint | 설명 | 인증 |
|:---:|:---|:---|:---:|
| `GET` | `/emails/availability?email=...` | 이메일 중복 확인 | ❌ |
| `GET` | `/nicknames/availability?nickname=...` | 닉네임 중복 확인 | ❌ |
| `POST` | `/signup` | 회원가입 | ❌ |
| `POST` | `/login` | 로그인 | ❌ |
| `POST` | `/logout` | 로그아웃 | ✅ |
| `GET` | `/me` | 현재 사용자 정보 조회 | ✅ |

<details>
<summary><b>📝 상세 스펙</b></summary>

#### POST `/signup`
```json
// Request Body
{
  "email": "user@example.com",
  "password": "Password1!",
  "nickname": "닉네임",
  "profileImage": "http://..." // optional
}
```

#### POST `/login`
```json
// Request Body
{
  "email": "user@example.com",
  "password": "Password1!"
}

// Response (Set-Cookie: session_id=...)
{
  "code": "success",
  "message": "로그인 성공",
  "data": {
    "user": {
      "userId": 1,
      "email": "user@example.com",
      "nickname": "닉네임",
      "profileImage": "http://..."
    }
  }
}
```
</details>

---

### 📝 게시글 API (`/v1/posts`)

| Method | Endpoint | 설명 | 인증 |
|:---:|:---|:---|:---:|
| `GET` | `?offset=0&limit=10` | 게시글 목록 조회 | ❌ |
| `GET` | `/{post_id}` | 게시글 상세 조회 | ❌ |
| `POST` | `/` | 게시글 작성 | ✅ |
| `PATCH` | `/{post_id}` | 게시글 수정 | ✅ |
| `DELETE` | `/{post_id}` | 게시글 삭제 | ✅ |
| `POST` | `/{post_id}/likes` | 좋아요 | ✅ |
| `DELETE` | `/{post_id}/likes` | 좋아요 취소 | ✅ |

<details>
<summary><b>📝 상세 스펙</b></summary>

#### POST `/` (게시글 작성)
```json
// Request Body
{
  "title": "게시글 제목",
  "content": "게시글 내용",
  "postImage": "http://..." // optional
}
```

#### GET `/{post_id}` (게시글 상세)
```json
// Response
{
  "code": "success",
  "message": "게시글 조회 성공",
  "data": {
    "postId": 1,
    "title": "제목",
    "content": "내용",
    "postImage": "http://...",
    "writer": "닉네임",
    "authorId": 1,
    "authorProfileImage": "http://...",
    "likeCount": 5,
    "commentCount": 3,
    "viewCount": 100,
    "createdAt": "2024-01-01T12:00:00",
    "updatedAt": "2024-01-01T12:00:00"
  }
}
```
</details>

---

### 💬 댓글 API (`/v1/posts/{post_id}/comments`)

| Method | Endpoint | 설명 | 인증 |
|:---:|:---|:---|:---:|
| `GET` | `/` | 댓글 목록 조회 | ❌ |
| `POST` | `/` | 댓글 작성 | ✅ |
| `PATCH` | `/{comment_id}` | 댓글 수정 | ✅ |
| `DELETE` | `/{comment_id}` | 댓글 삭제 | ✅ |

<details>
<summary><b>📝 상세 스펙</b></summary>

#### POST `/` (댓글 작성)
```json
// Request Body
{
  "content": "댓글 내용"
}

// Response
{
  "code": "success",
  "message": "댓글 작성 성공",
  "data": {
    "commentId": 1,
    "content": "댓글 내용",
    "authorId": 1,
    "authorNickname": "닉네임",
    "authorProfileImage": "http://...",
    "createdAt": "2024-01-01T12:00:00"
  }
}
```
</details>

---

### 👤 사용자 API (`/v1/users`)

| Method | Endpoint | 설명 | 인증 |
|:---:|:---|:---|:---:|
| `GET` | `/{user_id}` | 사용자 정보 조회 | ❌ |
| `PATCH` | `/{user_id}` | 프로필 수정 | ✅ |
| `PATCH` | `/{user_id}/password` | 비밀번호 변경 | ✅ |
| `DELETE` | `/me` | 회원 탈퇴 | ✅ |

<details>
<summary><b>📝 상세 스펙</b></summary>

#### PATCH `/{user_id}` (프로필 수정)
```json
// Request Body
{
  "nickname": "새닉네임",      // optional
  "profileImage": "http://..." // optional
}
```

#### PATCH `/{user_id}/password` (비밀번호 변경)
```json
// Request Body
{
  "currentPassword": "OldPassword1!",
  "newPassword": "NewPassword1!"
}
```
</details>

---

### 📁 파일 API (`/v1/files`)

| Method | Endpoint | 설명 | 인증 |
|:---:|:---|:---|:---:|
| `POST` | `/upload` | 파일 업로드 | ⚠️ |

> ⚠️ 회원가입 시 프로필 이미지는 인증 없이 업로드 가능

<details>
<summary><b>📝 상세 스펙</b></summary>

#### POST `/upload`
```
// Request (multipart/form-data)
file: (binary)
type: "post" | "profile"

// Response
{
  "code": "success",
  "message": "파일 업로드 성공",
  "data": {
    "imageUrl": "http://localhost:8000/uploads/xxx.jpg"
  }
}
```
</details>

<br>

---

## 🗄️ 데이터베이스

### ERD 개요

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   users     │     │    posts    │     │  comments   │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ user_id  PK │◄────│ author_id FK│     │ comment_id  │
│ email       │     │ post_id  PK │◄────│ post_id  FK │
│ password    │     │ title       │     │ author_id FK│
│ nickname    │     │ content     │     │ content     │
│ profile_img │     │ post_image  │     │ created_at  │
│ created_at  │     │ view_count  │     └─────────────┘
└─────────────┘     │ created_at  │
                    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │    likes    │
                    ├─────────────┤
                    │ post_id  FK │
                    │ user_id  FK │
                    └─────────────┘
```

### 주요 테이블

| 테이블 | 설명 |
|:---|:---|
| `users` | 사용자 정보 |
| `posts` | 게시글 정보 |
| `comments` | 댓글 정보 |
| `likes` | 좋아요 (user_id + post_id 복합키) |
| `sessions` | 세션 정보 (인메모리 또는 DB) |

<br>

---

## 🚨 에러 처리

### 공통 에러 응답 형식
```json
{
  "code": "error_code",
  "message": "에러 메시지",
  "data": null
}
```

### 주요 에러 코드

| HTTP Status | Code | 설명 |
|:---:|:---|:---|
| 400 | `bad_request` | 잘못된 요청 |
| 401 | `unauthorized` | 인증 필요 |
| 403 | `forbidden` | 권한 없음 |
| 404 | `not_found` | 리소스 없음 |
| 409 | `conflict` | 충돌 (중복 등) |
| 422 | `validation_error` | 유효성 검사 실패 |
| 500 | `internal_server_error` | 서버 오류 |

<br>

---

## 🔗 관련 저장소

| 저장소 | 설명 |
|:---|:---|
| [2-junsu-community-fe](https://github.com/hahark-ops/2-junsu-community-fe) | 프론트엔드 (HTML/CSS/JS) |

<br>

---

<p align="center">
  Made with ❤️ by junsu
</p>