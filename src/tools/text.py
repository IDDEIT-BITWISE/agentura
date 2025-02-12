import os

from openai import OpenAI
from pydantic import BaseModel, Field

from dotenv import main

main.load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SummaryText(BaseModel):
    title: str = Field(description='Краткий заголовок из 3-5 слов.')
    summary: str = Field(description='Краткое содержание текста')


def get_summary(prompt):
    try:
        chat_completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content":prompt},
                      {"role":"system", "content": "Ты агент для создании суммаризации текста. Генерируй ответ на том языке, на котором попросил пользователь. Если пользователь не указал язык, делай ответ на языке исходного текста"}],
            response_format=SummaryText
        )
        response = chat_completion.choices[0].message.parsed
        return response.title, response.summary
    except Exception as e:
        return str(e)
    
