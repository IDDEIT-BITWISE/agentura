from pydantic import BaseModel 
from pathlib import Path
class BotVideoResponse(BaseModel):
    chat_id: str 
    video_path: str