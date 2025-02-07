from pydantic import BaseModel
from typing import Any, Optional

class ResponseDTO(BaseModel):
    """
    ResponseDTO 클래스는 응답 데이터를 표현하는 데 사용됩니다.
    
    Attributes:
        code (int): 응답 코드 (성공 시 200, 실패 시 400 등)
        msg (str): 응답 메시지 (성공 시 "Success", 실패 시 "Error" 등)
        data (Optional[Any]): 응답 데이터 (성공 시 반환, 실패 시 None)
    """
    code: int
    msg: str
    data: Optional[Any] = None  # 응답 데이터 (성공 시 반환, 실패 시 None)

