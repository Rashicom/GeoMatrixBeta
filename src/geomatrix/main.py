from fastapi import FastAPI
from geomatrix.api import api_router

app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )

app.include_router(api_router, prefix="/api/v1")

@app.get('/')
def get_default_resp():
    return {"message": "Welcome to GeoMatrix!"}
