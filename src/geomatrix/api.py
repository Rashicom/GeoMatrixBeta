from fastapi import APIRouter

from geomatrix.authorization.router import router as authorization_router

api_router = APIRouter()

api_router.include_router(authorization_router, prefix="/auth", tags=["authorization"])
