from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings

class Summarizer:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_TEMPERATURE,
            model=settings.OPENAI_MODEL
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты профессионал по извлечению выжимок. Твоя задача -- сделать краткий пересказ текста. Учти, что ты сокращаешь не просто текст, а аудио, извлеченное из видеофайла Отвечай на русском языке"),
            ("human", "Дай краткую выжимку тексту:\n\n{text}")
        ])

    def summarize(self, text: str) -> str:
        chain = self.prompt | self.llm
        return chain.invoke({"text": text}).content