from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.services.gemini_service import TravelService

#Инициализиране основното приложение на FastApi
app = FastAPI()

# Свръзваме папката статик с URL за зареждане на frontend-a
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.post("/generate")
async def generate(
        #Зареждане на данни от HTML с Form(None)
        dest: str = Form(None),
        days: int = Form(3),
        rating: int = Form(3),
        image: UploadFile = File(None)
):
    #Провека дали потребителя е качил изображение
    image_data = None
    if image:
        #превръщане в байтове
        image_data = await image.read()

    #Пращане на данните в TravelService
    plan = TravelService.generate_plan(
        destination=dest,
        days=days,
        rating=rating,
        image_bytes=image_data
    )
    #Връщаме отговор в JSON формат към форнтенда
    return {"plan": plan}