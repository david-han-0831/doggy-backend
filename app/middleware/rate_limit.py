from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import aioredis

redis = None

async def init_redis():
    global redis
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        # Redis에서 현재 요청 횟수 조회
        count = await redis.get(key)
        count = int(count) if count else 0

        if count >= 10:  # 10초 동안 10개 요청 제한
            raise HTTPException(status_code=429, detail="Too many requests")

        await redis.setex(key, 10, count + 1)  # 10초 TTL 설정
        response = await call_next(request)
        return response
