import jwt
from jwt import PyJWTError
from typing import Dict, Any, Optional
from .config import settings

class TokenValidationError(Exception):
    """Raised when JWT validation fails."""
    pass

def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decodes and validates a JWT token.
    Raises TokenValidationError if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={
                "verify_aud": settings.JWT_AUDIENCE is not None,
                "verify_iss": settings.JWT_ISSUER is not None,
            },
        )
        return payload

    except PyJWTError as e:
        raise TokenValidationError(f"Invalid or expired token: {str(e)}")

def validate_and_extract_user(token: str) -> Dict[str, Any]:
    """
    High-level function:
    - Decode JWT
    - Extract user info
    - Return user dict
    """
    payload = decode_jwt_token(token)
    user_id: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")

    if not user_id or not role:
        raise TokenValidationError("Invalid token payload")

    return {"user_id": user_id, "role": role}
