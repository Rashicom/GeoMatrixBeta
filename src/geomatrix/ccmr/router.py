from fastapi import APIRouter




router = APIRouter()

@router.get("/protected")
async def test():
    return {"message": "APIKey protected endpoint"}