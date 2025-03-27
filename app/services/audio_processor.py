from moviepy import VideoFileClip
from pathlib import Path
import uuid
from core.config import settings
import subprocess
import os


def extract_audio(video_path: str) -> str:
    video = None
    try:
        video = VideoFileClip(str(video_path))
        audio_path = settings.TEMP_DIR / f"{uuid.uuid4()}.mp3"
        
        ffmpeg_params = [
            '-y',
            '-loglevel', 'quiet',
            '-b:a', '64k',    # Битрейт 64 kbit/s
            '-ar', '22050',    # Частота дискретизации 22.05 kHz
            '-ac', '1'         # Моно-звук
        ]
        
        video.audio.write_audiofile(
            str(audio_path),
            codec='mp3',
            logger=None,
            ffmpeg_params=ffmpeg_params
        )
        
        if not audio_path.exists():
            raise RuntimeError("Не удалось создать аудиофайл")
            
        return str(audio_path.resolve())
        
    except Exception as e:
        if audio_path and audio_path.exists():
            try: os.unlink(audio_path)
            except: pass
        raise
        
    finally:
        if video:
            try: video.close()
            except: pass
        if Path(video_path).exists():
            try: os.unlink(video_path)
            except: pass
