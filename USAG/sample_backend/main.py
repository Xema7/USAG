import uvicorn
from fastapi import FastAPI
from sample_backend.routes import router

app = FastAPI(
    title="Sample Backend Service",
    version="1.0.0",
    description="Backend service protected by Universal Secure API Gateway"
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "service": "Sample Backend",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(
        "sample_backend.main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
    )