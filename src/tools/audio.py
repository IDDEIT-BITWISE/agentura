import os

from openai import OpenAI
from pydantic import BaseModel
from moviepy import VideoFileClip
from src.langchain import State

from dotenv import main
main.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def audio_to_text(audio_path): 
    try:
        audio_file = open(audio_path, 'rb')
        transcription= client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        return str(e)
    
def extract_audio_from_video(state: State):
    try:
        video = VideoFileClip(state.video_path)
        audio = video.audio 
        audio.write_audiofile('temp_audio.wav')
        state.audio_path = os.path.abspath('temp_audio.wav')
        return state 
    except Exception as e:
        return str(e)

