import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import jwt

from app.main import app
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.core.config import settings


def generate_token(role: str):
    payload = {
        "sub": "test_user",
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

@pytest.fixture
def client():
    # Remove existing RateLimitMiddleware
    settings.RATE_LIMIT_PER_MINUTE = 6

    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_token():
    return generate_token("admin")


@pytest.fixture
def user_token():
    return generate_token("user")