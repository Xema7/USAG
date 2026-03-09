from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.core import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            raise

        process_time = round((time.time() - start_time) * 1000, 2)

        log_data = {
            "request_id": getattr(request.state, "request_id", "N/A"),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "client_ip": request.client.host if request.client else "unknown",
            "user_id": getattr(request.state, "user_id", "anonymous"),
            "role": getattr(request.state, "role", "unknown"),
            "compliance_tag": getattr(request.state, "compliance_tag", "N/A"),
            "response_time_ms": process_time
        }

        logger.info(str(log_data))

        return response