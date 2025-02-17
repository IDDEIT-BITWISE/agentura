import os

from openai import OpenAI
from pydantic import BaseModel, Field

from dotenv import main
from src.langchain import State

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
    


def summarize_text(state: State) -> State:
    """Суммаризация текста с GPT-4"""
    if not state.text:
        raise ValueError("Text not found in state")
    
    summary_prompt = f"""
    Суммаризируй следующий текст. Сохрани ключевые моменты.
    Язык итога: {'русский' if is_russian(state.text) else 'язык оригинала'}
    Текст: {state.text}
    """
    
    result = get_summary(summary_prompt)
    if isinstance(result, tuple):
        state.title, state.summary = result
    else:
        raise RuntimeError(f"Summarization failed: {result}")
    
    return state

def is_russian(text: str) -> bool:
    """Определение языка текста"""
    return any('а' <= c <= 'я' for c in text.lower())
