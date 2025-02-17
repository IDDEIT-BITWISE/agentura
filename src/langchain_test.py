from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image

from tools.audio import extract_audio
from tools.text import summarize_text

import os
from dotenv import main

from states import SummarizeState


main.load_dotenv()



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)



workflow = StateGraph(SummarizeState)

workflow.add_node("extract_audio", extract_audio)
workflow.add_node("summarize_text", summarize_text)

workflow.set_entry_point("extract_audio")
workflow.add_edge("extract_audio", "summarize_text")
workflow.add_edge("summarize_text", END)


app = workflow.compile()

def process_video(video_path: str, user_prompt: str = None) -> str:
    initial_state = {"video_path": video_path}
    result = app.invoke(initial_state)
    
    if user_prompt:
        # Если есть пользовательский промпт, обрабатываем его
        response = llm.invoke([
            HumanMessage(content=f"User prompt: {user_prompt}\n\nSummary: {result['summary']}")
        ])
        return response.content
    return result["summary"]

if __name__ == "__main__":
    
    video_path = input("Путь к видеофайлу")
    user_prompt = input("Промпт")


    # Запуск обработки
    try:
        result = process_video(video_path, user_prompt)
        print("Результат обработки:")
        print(result)
    except Exception as e:
        print(f"Ошибка при обработке видео: {e}")





        







    
