from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello")
async def test_api():
    return {"message": "Hello, i'm Geomatrix!"}
