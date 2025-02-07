from fastapi import APIRouter, Depends, HTTPException
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
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
@router.get("/status")
async def check_status():
    """✅ 서버 상태 체크 API"""
    return success_response(data={"status": "running"}, msg="Server is running")

@router.get("/error_test")
async def error_test():
    """❌ 강제 에러 테스트 API"""
    return error_response(400, "This is a test error")

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ ✅ Firebase 로그인 및 Refresh Token 저장 """
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

    jwt_token = create_jwt_token(uid, user.role)
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

    return success_response(
        data={"access_token": jwt_token, "refresh_token": refresh_token},
        msg="Login 성공"
    )

@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """ ✅ Refresh Token을 사용하여 새로운 Access Token 발급 """
    token_entry = db.query(RefreshToken).filter(
        RefreshToken.refresh_token == request.refresh_token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(datetime.utcnow())
    ).first()

    if not token_entry:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(User).filter(User.id == token_entry.user_id).first()
    return success_response(
        data={"access_token": create_jwt_token(user.firebase_uid, user.role)},
        msg="Token refreshed 성공"
    )

@router.post("/logout")
async def logout(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """ ✅ Refresh Token 무효화 """
    db.query(RefreshToken).filter(RefreshToken.refresh_token == request.refresh_token).update({"revoked": True})
    db.commit()
    return success_response(data=None, msg="Logged out 성공")