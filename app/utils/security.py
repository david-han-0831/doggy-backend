import jwt
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import auth, credentials
from typing import Dict
from app.utils.config import settings  # 환경변수에서 SECRET_KEY 가져옴
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# # JWT 설정값
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

firebase_credentials_path = settings.FIREBASE_CREDENTIALS



if not os.path.exists(firebase_credentials_path):
    raise FileNotFoundError(f"Firebase JSON 파일을 찾을 수 없습니다: {firebase_credentials_path}")

# # Firebase Admin SDK 초기화 (한 번만 실행)
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)  # Firebase 서비스 계정 JSON 경로
    firebase_admin.initialize_app(cred)

def create_jwt_token(uid: str, role: str):
    """ JWT 액세스 토큰 생성 """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"uid": uid, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(uid: str):
    """ Refresh Token 생성 """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"uid": uid, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str):
    """ JWT 토큰 검증 """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # ✅ 검증된 사용자 정보 반환 (예: {"uid": "1234", "role": "user"})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def verify_firebase_token(firebase_token: str):
    """ Firebase ID Token 검증 """
    try:
        decoded_token = auth.verify_id_token(firebase_token)  # Firebase 토큰 검증
        uid = decoded_token.get("uid")  # uid 가져오기
        email = decoded_token.get("email")  # 이메일 가져오기
        return {"uid": uid, "email": email}
    except Exception:
        raise ValueError("Invalid Firebase Token")
