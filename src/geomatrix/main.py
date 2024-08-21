from fastapi import FastAPI, Depends, HTTPException, status
from geomatrix.authorization.schemas import LoginRequestModel
from geomatrix.api import api_router
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )

app.include_router(api_router, prefix="/api/v1")



@app.post('/submit')
def get_default_resp(form_data: OAuth2PasswordRequestForm=Depends()):
    print(form_data.username)
    return {"message": "Welcome to GeoMatrix!"}
