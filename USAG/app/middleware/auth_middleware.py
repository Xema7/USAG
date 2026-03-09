from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core import validate_and_extract_user, TokenValidationError


PUBLIC_ROUTES = [
    "/",
    "/health",
    "/health/",
    "/docs",
    "/openapi.json",
]


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing or invalid Authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            user_data = validate_and_extract_user(token)

            request.state.user_id = user_data["user_id"]
            request.state.role = user_data["role"]

        except TokenValidationError as e:
            return JSONResponse(
                status_code=401,
                content={"error": str(e)}
            )

        return await call_next(request)