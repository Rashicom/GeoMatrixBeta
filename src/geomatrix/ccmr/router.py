from fastapi import APIRouter
from geomatrix.ccmr.schemas import RequestCreateCadastreSchema, ResponseCreateCadastreSchema

router = APIRouter()


@router.post("/create-cadastre")
async def create_cadastre(request_schama: RequestCreateCadastreSchema):
    """
    Creating Single Cadastre

    Pre Checks:
        - Form validation
        - Cadastre corditates validation
        - Cadastre overlaping validation (one cadastre must not overlap other cadastre)
    """
    print(request_schama)
    return {"message": "APIKey protected endpoint"}


@router.post("/create-bulk-cadastres")
async def create_bulk_cadastres(request_schama: RequestCreateCadastreSchema):
    pass