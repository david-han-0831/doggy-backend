from fastapi import FastAPI
from app.utils.config import settings
from app.db.database import engine  # database.py에서 생성한 engine을 가져옴
import os

# FastAPI 애플리케이션 초기화
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# 데이터베이스 연결 확인 (별도 engine 생성 없이 database.py의 engine 사용)
try:
    conn = engine.connect()
    print("데이터베이스 연결 성공!")
    conn.close()
except Exception as e:
    print("데이터베이스 연결 실패:", e)

# 환경변수 확인용 엔드포인트
@app.get("/config-check")
def check_config():
    """
    환경 변수가 정상적으로 로드되었는지 확인하는 엔드포인트
    """
    return {
        "DATABASE_URL": settings.DATABASE_URL,
        "REDIS_HOST": settings.REDIS_HOST,
        "JWT_SECRET_KEY": settings.JWT_SECRET_KEY[:10] + "****"
    }

# 기본 라우트
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}
