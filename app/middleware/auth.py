from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security import verify_jwt_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """ JWT 인증 미들웨어 """
        
        # 인증 없이 접근 허용할 경로들을 화이트리스트로 지정합니다.
        whitelist = [
            "/api/v1/auth/login",  # 로그인 엔드포인트
            "/api/v1/auth/logout",  # 로그아웃 엔드포인트 추가
            "/docs",               # Swagger UI
            "/openapi.json",       # OpenAPI 스펙
            "/favicon.ico",        # 파비콘
        ]
        
        # 현재 요청 경로가 whitelist에 해당하면 토큰 검사를 건너뜁니다.
        if any(request.url.path.startswith(path) for path in whitelist):
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized: Missing token")

        token = auth_header.split("Bearer ")[1]
        user_payload = verify_jwt_token(token)

        if not user_payload:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        request.state.user = {"uid": user_payload["uid"], "role": user_payload["role"]}
        response = await call_next(request)
        return response
