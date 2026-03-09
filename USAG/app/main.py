import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app import __version__
from app.core import settings, setup_logging, get_logger
from app.db import connect_to_mongo, close_mongo_connection, create_indexes

# Middleware (import via package)
from app.middleware import (
    ComplianceMiddleware,
    RateLimitMiddleware,
    AuthMiddleware,
    LoggingMiddleware,
    RequestIDMiddleware,
)

# Routes
from app.routes import health_router, audit_router, ai_router, proxy_router

# ---------------------------------------------------------
# Initialize Logging FIRST
# ---------------------------------------------------------

setup_logging()
logger = get_logger(__name__)

# ---------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await create_indexes()
    print("✅ MongoDB connected & indexes ensured")

    yield

    # Shutdown
    await close_mongo_connection()
    print("❌ MongoDB connection closed")


# ---------------------------------------------------------
# FastAPI Initialization
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Plug-and-Play Enterprise Security Layer for Any Backend",
    lifespan=lifespan,
)

# ---------------------------------------------------------
# Middleware Registration (Correct Order)
# ---------------------------------------------------------
app.add_middleware(ComplianceMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
)
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(audit_router, prefix="/audit", tags=["Audit"])
app.include_router(ai_router, prefix="/ai", tags=["AI Security"])

# Catch-all proxy (must be last)
app.include_router(proxy_router)
# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

# ---------------------------------------------------------
# Local Development Entry
# ---------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )