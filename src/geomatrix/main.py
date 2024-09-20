from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from geomatrix.api import api_router
from geomatrix.common.email import send_template_mail


app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool",
    summary="GeoMatrix is a geo-spatial data analysis tool providing cutting edge service for government and private sectors",
    version="0.0.1",
    contact={
        "name": "GeoMatrix Team",
        "url": "http://example.com/help",
        "email": "rashid.kp484@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    )

# mound static directory
app.mount("/static",StaticFiles(directory="static"),name="static")

# add routes
app.include_router(api_router, prefix="/api/v1")


@app.post('/sent')
async def sendmail():
    await send_template_mail(["rashid.kp484@gmail.com"])
    return {"message": "Welcome to GeoMatrix!"}
