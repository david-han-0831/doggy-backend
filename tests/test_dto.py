import json
from app.utils.dto import ResponseDTO
from app.utils.response_utils import success_response, error_response
from fastapi.responses import JSONResponse

def test_response_dto():
    """✅ ResponseDTO가 올바르게 생성되는지 테스트"""
    response = ResponseDTO(code=200, msg="OK", data={"user": "test_user"})
    
    assert response.code == 200
    assert response.msg == "OK"
    assert response.data == {"user": "test_user"}

def test_success_response():
    """✅ success_response() 함수 테스트"""
    response: JSONResponse = success_response(data={"user_id": 123}, msg="User created")
    json_data = response.body.decode("utf-8")  # FastAPI JSON 응답을 문자열로 변환

    expected_response = {
        "code": 200,
        "msg": "User created",
        "data": {"user_id": 123}
    }

    # 🔹 JSON 문자열 변환 후 비교
    assert response.status_code == 200
    assert json_data == json.dumps(expected_response, separators=(",", ":"))  # ✅ JSON 포맷 차이 해결

def test_error_response():
    """✅ error_response() 함수 테스트"""
    response: JSONResponse = error_response(code=400, msg="Bad Request")
    json_data = response.body.decode("utf-8")  # FastAPI JSON 응답을 문자열로 변환

    expected_response = {
        "code": 400,
        "msg": "Bad Request",
        "data": None
    }

    # 🔹 JSON 문자열 변환 후 비교
    assert response.status_code == 400
    assert json_data == json.dumps(expected_response, separators=(",", ":"))  # ✅ JSON 포맷 차이 해결
