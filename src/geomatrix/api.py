from fastapi import APIRouter, Depends

from geomatrix.authorization.router import router as authorization_router
from geomatrix.ccmr.router import router as ccmr_router
from geomatrix.dependencies import validate_apikey

api_router = APIRouter()

api_router.include_router(authorization_router, prefix="/auth", tags=["authorization"])
api_router.include_router(ccmr_router, prefix="/ccmr", tags=["ccmr"] , dependencies=[Depends(validate_apikey)])
