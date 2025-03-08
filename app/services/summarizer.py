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
            ("system", "You are a professional summarizer. Create concise Russian summary."),
            ("human", "Summarize this text:\n\n{text}")
        ])

    def summarize(self, text: str) -> str:
        chain = self.prompt | self.llm
        return chain.invoke({"text": text}).content