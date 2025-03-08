# services/transcriber.py
import whisper
import os
from pathlib import Path
import time
from core.config import settings

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model(settings.WHISPER_MODEL)

    def transcribe(self, audio_path: str) -> str:
        try:
            abs_path = Path(audio_path).resolve()
            print(abs_path)
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