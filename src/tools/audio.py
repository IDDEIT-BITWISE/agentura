import os

from openai import OpenAI
from pydantic import BaseModel

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
