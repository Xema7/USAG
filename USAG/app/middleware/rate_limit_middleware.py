from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core import RateLimiter

class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(
            max_requests=requests_per_minute,
            window_seconds=60,
        )

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host if request.client else "testclient"

        if not self.limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded. Try again later."}
            )

        response = await call_next(request)

        remaining = self.limiter.get_remaining_requests(client_ip)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response