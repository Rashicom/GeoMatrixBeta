from fastapi import FastAPI, Depends
from .config import DatabaseSettings
from sqlalchemy.orm import Session
from geomatrix.database.core import get_db

app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )


@app.get("/api/hello")
async def test_api(db:Session=Depends(get_db)):
    return {"message": "Hello, i'm Geomatrix!"}
