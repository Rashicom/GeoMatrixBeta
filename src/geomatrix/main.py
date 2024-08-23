from fastapi import FastAPI, Depends
from geomatrix.api import api_router
from geomatrix.common.email import send_mail


app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )

app.include_router(api_router, prefix="/api/v1")



@app.post('/sent')
async def sendmail():
    await send_mail(["rashid.kp484@gmail.com"])
    return {"message": "Welcome to GeoMatrix!"}
