import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.config import settings  # ✅ APP_NAME 가져오기

client = TestClient(app)

def test_check_status():
    """✅ 서버 상태 체크 API 테스트"""
    response = client.get("/api/v1/auth/status")
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "msg": "Server is running",
        "data": {"status": "running"}
    }

def test_error_response():
    """❌ 강제 에러 테스트 API"""
    response = client.get("/api/v1/auth/error_test")
    assert response.status_code == 400
    assert response.json() == {
        "code": 400,
        "msg": "This is a test error",
        "data": None
    }

def test_root():
    """✅ 기본 엔드포인트 테스트"""
    expected_message = f"Welcome to {settings.APP_NAME}"  # ✅ 실제 APP_NAME 반영
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
