import httpx
from fastapi import Request, Response
from app.core import settings

SAFE_HEADERS = [
    "content-type",
    "content-length"
]

async def forward_request(request: Request) -> Response:

    backend_url = f"{settings.TARGET_BACKEND_URL}{request.url.path}"

    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            backend_response = await client.request(
                method=request.method,
                url=backend_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
        
        # Filter unsafe headers
        filtered_headers = {
            key: value
            for key, value in backend_response.headers.items()
            if key.lower() in SAFE_HEADERS
        }
        
        return Response(
            content=backend_response.content,
            status_code=backend_response.status_code,
            headers=filtered_headers,       
        )

    except httpx.RequestError as e:
        return Response(
            content=f"Backend service unavailable: {str(e)}",
            status_code=502
        )