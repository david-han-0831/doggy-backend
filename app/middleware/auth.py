from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security import verify_jwt_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """ JWT 인증 미들웨어 """
        if request.url.path.startswith("/api/v1/auth"):
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
