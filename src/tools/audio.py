import sys 
sys.path.append('..')

import os

from openai import OpenAI
from pydantic import BaseModel
from moviepy import VideoFileClip
from src.states import SummarizeState

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
    
def extract_audio_from_video(state: SummarizeState):
    try:
        video = VideoFileClip(state.video_path)
        audio = video.audio 
        audio.write_audiofile('temp_audio.wav')
        state.audio_path = os.path.abspath('temp_audio.wav')
        return state 
    except Exception as e:
        return str(e)
    
def transcribe_audio(state: SummarizeState) -> SummarizeState:
    """Транскрибация аудио в текст"""
    if not state.audio_path:
        raise ValueError("Audio path not found in state")
    
    transcription = audio_to_text(state.audio_path)
    if isinstance(transcription, str):
        state.text = transcription
    else:
        raise RuntimeError(f"Transcription failed: {transcription}")
    
    return state

def extract_audio(state: SummarizeState):
    audio_path = extract_audio_from_video(state["video_path"])
    return {"audio_text": audio_to_text(audio_path), **state}
