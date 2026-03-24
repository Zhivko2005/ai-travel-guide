from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.services.gemini_service import TravelService

app = FastAPI(title="AI Travel Guide API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/generate")
def generate(dest: str, days: int = 2):
    plan = TravelService.generate_plan(dest, days)
    return {"plan": plan}