from fastapi import APIRouter
from app.utils.response_utils import success_response, error_response

router = APIRouter()

@router.get("/status")
async def check_status():
    """✅ 서버 상태 체크 API"""
    return success_response(data={"status": "running"}, msg="Server is running")

@router.get("/error_test")
async def error_test():
    """❌ 강제 에러 테스트 API"""
    return error_response(400, "This is a test error")
