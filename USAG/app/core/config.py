from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # -----------------------------------------------------
    # Application
    # -----------------------------------------------------
    APP_NAME: str = "Universal Secure API Gateway"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # -----------------------------------------------------
    # Security
    # -----------------------------------------------------
    JWT_SECRET_KEY: str = Field(..., description="Secret key for JWT validation")
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str | None = None
    JWT_ISSUER: str | None = None

    # -----------------------------------------------------
    # Rate Limiting
    # -----------------------------------------------------
    RATE_LIMIT_PER_MINUTE: int = 60

    # -----------------------------------------------------
    # MongoDB
    # -----------------------------------------------------
    MONGODB_URI: str = Field(..., description="MongoDB connection string")
    MONGODB_DB_NAME: str = "secure_gateway_db"

    # -----------------------------------------------------
    # AI Configuration
    # -----------------------------------------------------
    AI_PROVIDER: str = "gemini"  # openai | gemini | claude
    AI_API_KEY: str | None = None
    AI_MODEL_NAME: str = "gemini-2.5-flash"

    # -----------------------------------------------------
    # Backend Service (Target Service Gateway Protects)
    # -----------------------------------------------------
    TARGET_BACKEND_URL: str = "http://localhost:9000"

    class Config:
        env_file = ".env"
        case_sensitive = True


# ---------------------------------------------------------
# Cached Settings Instance
# ---------------------------------------------------------

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()