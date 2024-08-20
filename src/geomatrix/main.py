from fastapi import FastAPI, Depends, HTTPException, status
from geomatrix.authorization.schemas import LoginRequestModel
from geomatrix.api import api_router
from geomatrix.database.core import get_db
from sqlalchemy.orm import Session
from typing import Annotated

app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )

app.include_router(api_router, prefix="/api/v1")


def testing(dbs: Session=Depends(get_db)):
    print(dbs)
    return "hello"

@app.post('/submit')
def get_default_resp(db:Session=Depends(get_db), tt:str=Depends(testing) ):
    print(db)
    return {"message": "Welcome to GeoMatrix!"}
    