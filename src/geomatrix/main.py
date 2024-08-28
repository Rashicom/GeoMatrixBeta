from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from geomatrix.api import api_router
from geomatrix.common.email import send_template_mail


app = FastAPI(
    title="GeoMatrix",
    description="A geospatial data analysis tool"
    )

# mound static directory
app.mount("/static",StaticFiles(directory="static"),name="static")

# add routes
app.include_router(api_router, prefix="/api/v1")


@app.post('/sent')
async def sendmail():
    await send_template_mail(["rashid.kp484@gmail.com"])
    return {"message": "Welcome to GeoMatrix!"}
