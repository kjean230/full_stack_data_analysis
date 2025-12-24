from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Urban Ecology Analytics Platform", version="0.1.0")

@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
app.include_router(api_router, prefix="/api/v1")