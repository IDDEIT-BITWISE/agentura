from moviepy import VideoFileClip
from pathlib import Path
import uuid
from core.config import settings

def extract_audio(video_path: str) -> str:
    try:
        with VideoFileClip(str(video_path)) as video:
            audio_path = settings.TEMP_DIR / f"{uuid.uuid4()}.mp3"
            video.audio.write_audiofile(
                str(audio_path),
                codec='mp3',
                logger=None,  
                ffmpeg_params=['-y', '-loglevel', 'quiet']
            )
        return str(audio_path.resolve())  
    finally:
        if video:
            video.close()