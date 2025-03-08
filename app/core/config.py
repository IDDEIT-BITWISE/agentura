from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "Video Analyzer"
    TEMP_DIR: Path = Path("temp")
    
    # OpenAI настройки
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo-1106"
    OPENAI_TEMPERATURE: float = 0.3
    
    # Whisper настройки
    WHISPER_MODEL: str = "base"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
settings.TEMP_DIR.mkdir(exist_ok=True)