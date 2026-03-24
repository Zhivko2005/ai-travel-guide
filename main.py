from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.services.gemini_service import TravelService

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.post("/generate")
async def generate(
        dest: str = Form(None),
        days: int = Form(3),
        rating: int = Form(3),
        image: UploadFile = File(None)
):
    image_data = None
    if image:
        image_data = await image.read()

    plan = TravelService.generate_plan(
        destination=dest,
        days=days,
        rating=rating,
        image_bytes=image_data
    )

    return {"plan": plan}