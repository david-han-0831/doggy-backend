from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import uuid
from app.utils.security import verify_firebase_token, create_jwt_token, create_refresh_token
from app.db.database import get_db
from app.db.models.user import User
from app.db.models.refresh_tokens import RefreshToken
from pydantic import BaseModel
from app.utils.response_utils import success_response, error_response


router = APIRouter()
class LoginRequest(BaseModel):
    firebase_token: str  # Next.js가 전달하는 Firebase ID Token
    
    
@router.get("/status")
async def check_status():
    """✅ 서버 상태 체크 API"""
    return success_response(data={"status": "running"}, msg="Server is running")

@router.get("/error_test")
async def error_test():
    """❌ 강제 에러 테스트 API"""
    return error_response(400, "This is a test error")

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)) -> Response:
    """
    ✅ Firebase 로그인 및 Refresh Token 저장 후,
       Refresh Token을 httpOnly 쿠키에 설정하는 엔드포인트
    """
    print(f'request: {request}')
    
    firebase_user = verify_firebase_token(request.firebase_token)
    print(f'firebase_user: {firebase_user}')

    uid = firebase_user["uid"]
    email = firebase_user["email"]

    user = db.query(User).filter(User.firebase_uid == uid).first()
    
    if not user:
        user = User(firebase_uid=uid, email=email, role="user", created_at=datetime.utcnow())
        db.add(user)
        db.commit()
        db.refresh(user)
    # JWT Access Token 생성 (Next.js 클라이언트에 전달)
    jwt_token = create_jwt_token(uid, user.role)
    
    # Refresh Token 생성 (httpOnly 쿠키에 저장)
    refresh_token = create_refresh_token(uid)

    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"revoked": True})
    new_refresh_token = RefreshToken(
        id=uuid.uuid4(),
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        created_at=datetime.now(timezone.utc),
        revoked=False
    )
    db.add(new_refresh_token)
    db.commit()
    
    # JSON 응답에는 Access Token만 포함
    response = success_response(
        data={"access_token": jwt_token},
        msg="Login 성공"
    )
    # httpOnly 쿠키에 Refresh Token 설정 (max_age: 7일)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,        # JavaScript 접근 불가
        secure=False,          # 배포 시 HTTPS 환경에서 True, 개발 환경에서는 False로 설정 가능
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )

    return response

@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_db)):
    """
    ✅ httpOnly 쿠키에 저장된 Refresh Token을 사용하여
       새로운 Access Token을 발급하는 엔드포인트
    """
    
    # 쿠키에서 refresh token 읽기
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not provided")
    
    
    token_entry = db.query(RefreshToken).filter(
        RefreshToken.refresh_token == refresh_token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not token_entry:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(User).filter(User.id == token_entry.user_id).first()
    new_access_token = create_jwt_token(user.firebase_uid, user.role)
    return success_response(
        data={"access_token": new_access_token},
        msg="Token refreshed 성공"
    )

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """
    ✅ Refresh Token 무효화 후,
       클라이언트 쿠키에서 Refresh Token을 삭제하는 엔드포인트
    """
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).update({"revoked": True})
        db.commit()
    response = success_response(data=None, msg="Logged out 성공")
    # 클라이언트 쿠키에서 refresh token 삭제
    response.delete_cookie("refresh_token")
    return response