from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services import forward_request, validate_request, log_event

router = APIRouter()

@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(full_path: str, request: Request):

    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except Exception:
            body = None

    # Validate request if rules exist
    validate_request(f"/{full_path}", request.method, body)

    # Forward to backend
    response = await forward_request(request)

    # Log audit event
    await log_event(
        request_id=getattr(request.state, "request_id", None),
        user_id=getattr(request.state, "user_id", None),
        role=getattr(request.state, "role", None),
        path=f"/{full_path}",
        method=request.method,
        status_code=response.status_code,
        client_ip=request.client.host if request.client else "unknown",
        compliance_tag=getattr(request.state, "compliance_tag", None),
    )

    return response