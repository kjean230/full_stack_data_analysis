from fastapi import APIRouter

api_router = APIRouter()

# Later:
# from app.api.v1.endpoints import auth, presets, trees
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(presets.router, prefix="/presets", tags=["presets"])
# api_router.include_router(trees.router, prefix="/trees", tags=["trees"])