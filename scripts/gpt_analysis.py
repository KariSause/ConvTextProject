
import os
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



class CallAnalysisSchema(BaseModel):
    date: str = Field(description="Дата дзвінка у форматі YYYY-MM-DD")
    call_type: str = Field(description="Тип дзвінка (incoming або outgoing)")
    script: int = Field(description="Привітання та початок за скриптом (1 або 0)")
    car_info: int = Field(description="Уточнення кузова/року/пробігу авто (1 або 0)")
    upsell: int = Field(description="Спроба додаткового продажу або пропозиція діагностики (1 або 0)")
    service_history: int = Field(description="Питання про історію обслуговування раніше (1 або 0)")
    closing: int = Field(description="Коректне закриття та прощання (1 або 0)")
    
    call_result: str = Field(description="Тип робіт чи результат дзвінка (наприклад: Запис на ТО, Відмова)")
    parts: str = Field(description="Які запчастини обговорювались")
    comment: str = Field(description="Коментар щодо помилок менеджера та стилю розмови")
    score: int = Field(description="Оцінка менеджера за розмову від 1 до 5")
    bad_call: bool = Field(description="Чи є розмова некоректною, а відповіді менеджера поганими (True/False)")

def analyze(transcript: str) -> dict:
    prompt = f"""
        Ти — суворий QA-аналітик контролю якості автосервісу.
        Проаналізуй розмову менеджера з клієнтом за критеріями.
        Якщо менеджер відповідає грубо, не знає відповідей, ігнорує правила або клієнт незадоволений — обов'язково постав bad_call = true.
        
        ТЕКСТ РОЗМОВИ:
        {transcript}
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=CallAnalysisSchema,
    )
    return response.choices[0].message.parsed.model_dump()