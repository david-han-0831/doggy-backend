from fastapi.responses import JSONResponse
from app.utils.dto import ResponseDTO

def success_response(data, msg: str = "Success") -> JSONResponse:
    """✅ 성공 응답
    data: 응답 데이터
    msg: 응답 메시지
    """
    return JSONResponse(
        status_code=200,
        content=ResponseDTO(code=200, msg=msg, data=data).model_dump()
    )

def error_response(code: int, msg: str = "Error") -> JSONResponse:
    """❌ 실패 응답
    code: 응답 코드
    msg: 응답 메시지
    """
    return JSONResponse(
        status_code=code,
        content=ResponseDTO(code=code, msg=msg, data=None).model_dump()
    )
