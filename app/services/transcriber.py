import whisper
import os
from pathlib import Path
import time
from core.config import Settings

import torch
from openai import OpenAI

settings = Settings()
settings.TEMP_DIR.mkdir(exist_ok=True)

class Transcriber:
    def __init__(self):
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model = whisper.load_model(settings.WHISPER_MODEL, device=self.device)


    def transcribe(self, audio_path: str, mode='api') -> str:
        if mode=='local':
            try:
                print(f'Using device:{self.device}')
                abs_path = Path(audio_path).resolve()
                print(f'audio created: {abs_path}')
                start_time = time.time()
                while not abs_path.exists():
                    if time.time() - start_time > 10:
                        raise FileNotFoundError(f"Файл {abs_path} не найден")
                    time.sleep(0.1)

                
                if not os.access(abs_path, os.R_OK):
                    raise PermissionError(f"Нет доступа к файлу {abs_path}")

                result = self.model.transcribe(str(abs_path))
                os.unlink(abs_path)
                return result["text"]
                
            except Exception as e:
                if abs_path.exists():
                    os.unlink(abs_path)
                raise RuntimeError(f"Ошибка транскрибации: {str(e)}") from e
        if mode=='api':
            try:
                print("Using OpenAI API")
                abs_path = Path(audio_path).resolve()
                print(f'audio created: {audio_path}')
                start_time = time.time()
                while not abs_path.exists():
                    if time.time() - start_time > 10:
                        raise FileNotFoundError(f"Файл {abs_path} не найден")
                    time.sleep(0.1)

                
                if not os.access(abs_path, os.R_OK):
                    raise PermissionError(f"Нет доступа к файлу {abs_path}")

                
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                with open(audio_path, 'rb') as audio:
                    transcription = client.audio.transcriptions.create(
                        model='whisper-1',
                        file=audio,
                        response_format='text'
                    )
                    return transcription
                
            except Exception as e:
                if abs_path.exists():
                    os.unlink(abs_path)
                raise RuntimeError(f"Ошибка транскрибации: {str(e)}") from e
