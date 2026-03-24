import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class TravelService:
    @staticmethod
    def generate_plan(destination: str, days: int):
        """Изпраща промпт към Gemini и връща генерирания план."""

        model_id = "gemini-2.5-flash"

        prompt = (
            f"Ти си професионален ескурзовод. Направи вълнуващ и кратък "
            f"туристически план за {days} дни в {destination}. Използвай булети и емотикони."
        )

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