import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

#Зареждане на GEMINI_API_KEY
load_dotenv()
#Инициализация на клиента
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class TravelService:
    @staticmethod
    def generate_plan(destination: str, days: int, rating: int, image_bytes: bytes = None):

        #Идентификатор на модела
        model_id = "gemini-2.5-flash"

        #Списък с частите, които изпращаме на ИИ
        contents = []

        #Логика в случай в който използваме снимка
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))

            prompt_text = (
                f"Ти си професионален туристически eкскурзовод."
                f"Анализирай какво виждаш на снимката: архитектура, надписи, регистрационни номера, специфични обекти, без да ги поясняваш в отговора си"
                f"Въз основа на тези доказателства, идентифицирай града и държавата, като стриктно по шаблон : Въз основа на снимковия материал идентифицирах че града е /.../"
                f"СЛЕД разпознаването, препоръчай поне 3 хотела с категория {rating} звезди в тази дестинация. "
                f"Направи туристически план за {days} дни в тази дестинация"
                f"Използвай емотикони и НЕ използвай bold-ване на текста"
            )
        #Логика в случай в който използваме информацията от текстбокса
        else:
            prompt_text = (
            f"Ти си професионален туристически eкскурзовод. Направи план за {days} дни в {destination}. "
            f"ВАЖНО: Препоръчай поне 3 хотела с категория {rating} звезди в тази дестинация. "
            f"Опиши защо са подходящи. Раздели плана по дни и използвай емотикони и НЕ използвай bold-ване на текста."
            )
        #Добавяне на промпта към компонентите
        contents.append(prompt_text)

        try:
            #Изпращане на заявката към API-то
            response = client.models.generate_content(
                model=model_id,
                contents=contents,
                #Задаване на настройки
                config=types.GenerateContentConfig(
                    temperature=0.3, #По-ниска температура - баланс между логично мислене и креативност
                    top_p=0.95, #Контрол на разнообразието на думите
                    max_output_tokens=5000 #Лимит на дължината на отговора
                )
            )
            return response.text
        except Exception as e:
            #HTTP error 429 - Too many requests - За да не гърми приложението при достигнат лимит при заявки
            if "429" in str(e):
                return "Грешка: Лимитът на безплатни заявки е достигнат. Моля, изчакайте 1 минута."
            return f"Възникна грешка при връзка с ИИ: {str(e)}"