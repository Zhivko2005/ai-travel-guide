import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class TravelService:
    @staticmethod
    def generate_plan(destination: str, days: int, rating: int, image_bytes: bytes = None):
        model_id = "gemini-2.5-flash"

        prompt = (
            f"Ти си професионален туристически eксурзовод. Направи план за {days} дни в {destination}. "
        f"ВАЖНО: Препоръчай поне 3 хотела с категория {rating} звезди в тази дестинация. "
        f"Опиши защо са подходящи. Раздели плана по дни и използвай емотикони."
        )
        contents = []

        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpg"))
            prompt      +=("Анализирай внимателно тази снимка. Определи точното местоположение (град и държава). "
                f"След като го идентифицираш, направи туристически план за {days} дни в този град. "
                f"Включи хотели с {rating} звезди. Отговори на български.")
        else:
            prompt  += f" Дестинацията е: {destination}."

        contents.append(prompt)
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "Грешка: Лимитът на безплатни заявки е достигнат. Моля, изчакайте 1 минута."
            return f"Възникна грешка при връзка с ИИ: {str(e)}"