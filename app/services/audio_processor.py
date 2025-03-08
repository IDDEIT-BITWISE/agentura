from moviepy import VideoFileClip
from pathlib import Path
import uuid
from core.config import settings

def extract_audio(video_path: str) -> str:
    try:
        # Явное закрытие ресурсов
        with VideoFileClip(str(video_path)) as video:
            audio_path = settings.TEMP_DIR / f"{uuid.uuid4()}.mp3"
            video.audio.write_audiofile(
                str(audio_path),
                codec='mp3',
                logger=None,  # Отключаем логирование MoviePy
                ffmpeg_params=['-y', '-loglevel', 'quiet']
            )
        return str(audio_path.resolve())  # Возвращаем абсолютный путь
    finally:
        if video:
            video.close()