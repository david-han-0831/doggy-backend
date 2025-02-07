import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            f"📌 [Request] {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.2f}s"
        )
        return response
