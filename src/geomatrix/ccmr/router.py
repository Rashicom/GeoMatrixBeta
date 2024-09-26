from fastapi import APIRouter
from geomatrix.ccmr.schemas import RequestCreateCadastreSchema, ResponseCreateCadastreSchema
from geomatrix.ccmr.service import validate_cadastre
router = APIRouter()


@router.post("/create-cadastre")
async def create_cadastre(request_schema: RequestCreateCadastreSchema):
    """
    Creating Single Cadastre

    Pre Checks:
        - Form validation
        - Cadastre corditates validation
        - Cadastre overlaping validation (one cadastre must not overlap other cadastre)
    """
    print(request_schema)
    validator = validate_cadastre(request_schema)
    return {"message": "APIKey protected endpoint"}


@router.post("/create-bulk-cadastres")
async def create_bulk_cadastres(request_schama: RequestCreateCadastreSchema):
    pass