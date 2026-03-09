from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core import get_compliance_metadata, is_role_allowed

class ComplianceMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path
        metadata = get_compliance_metadata(path)

        allowed_roles = metadata.get("allowed_roles", [])
        role = getattr(request.state, "role", None)

        # Enforce role-based access
        if allowed_roles and not role:
            return JSONResponse(
                status_code=403,
                content={"error": "Authentication required"}
            )
        
        if role and not is_role_allowed(path, role):
            return JSONResponse(
                status_code=403,
                content={"error": "Access denied for this role"}
            )

        request.state.compliance_tag = metadata["level"]

        response = await call_next(request)

        response.headers["X-Compliance-Level"] = metadata["level"]

        return response