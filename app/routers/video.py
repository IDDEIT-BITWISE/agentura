from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uuid
import os
import logging
from pydantic import BaseModel

from services.audio_processor import extract_audio
from services.transcriber import Transcriber
from services.summarizer import Summarizer
from core.config import settings
from models.BotVideoResponse import BotVideoResponse


router = APIRouter()
logger = logging.getLogger(__name__)

#templates = Jinja2Templates(directory="../templates")


# @router.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     """
#     Главная страница с формой загрузки видео.
#     """
#     return templates.TemplateResponse("index.html", {"request": request})

# @router.post("/process")
# async def process_video(video_file: UploadFile = File(...)):
#     video_path = None
#     audio_path = None
    
#     try:
#         if not video_file.content_type.startswith('video/'):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Неподдерживаемый формат файла"
#             )

#         video_path = settings.TEMP_DIR / f"{uuid.uuid4()}.mp4"
#         with open(video_path, "wb") as buffer:
#             content = await video_file.read()
#             buffer.write(content)

#         if video_path.stat().st_size > 500 * 1024 * 1024:  # 500MB
#             raise HTTPException(
#                 status_code=413,
#                 detail="Файл слишком большой (макс. 500MB)"
#             )

#         audio_path_str = extract_audio(str(video_path))
#         audio_path = Path(audio_path_str) 
        
#         if not audio_path.exists():
#             raise HTTPException(
#                 status_code=500,
#                 detail="Не удалось создать аудиофайл"
#             )

#         transcript = Transcriber().transcribe(str(audio_path)) 
#         summary = Summarizer().summarize(text=transcript)

#         return JSONResponse({
#             "status": "success",
#             "full_text":transcript, 
#             "summary": summary,
#             "filename": video_file.filename
#         })

#     except HTTPException as he:
#         logger.error(f"HTTP Error: {he.detail}")
#         raise he
        
#     except Exception as e:
#         logger.error(f"Processing error: {str(e)}", exc_info=True)
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": "error",
#                 "error": str(e)
#             }
#         )

#     finally:
#         if video_path and video_path.exists():
#             os.unlink(video_path)
#         if audio_path and audio_path.exists():
#             os.unlink(audio_path)

@router.post("/processFilename")
async def process_video_filename(data: BotVideoResponse):
    chat_id = data.chat_id
    video_path = data.video_path

    print(video_path, chat_id)
    
    try:
        audio_path_str = extract_audio(video_path)
        audio_path = Path(audio_path_str) 
        
        if not audio_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Не удалось создать аудиофайл"
            )

        transcript = Transcriber().transcribe(str(audio_path)) 
        summary = Summarizer().summarize(text=transcript)

        return JSONResponse({
            "status": "success",
            "full_text":transcript, 
            "summary": summary,
        })

    except HTTPException as he:
        logger.error(f"HTTP Error: {he.detail}")
        raise he
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )

@router.post("/process-audio")
async def process_audio_endpoint(
    file: UploadFile = File(..., description="Аудиофайл (MP3, WAV, OGG) до 100MB")
):
    """
    Пример curl запроса:
    curl -X POST "http://127.0.0.1:8000/process-audio" \
    -H "accept: application/json" \
    -F "file=@audio.mp3"
    """
    try:
        filename = file.filename or "audio"
        file_ext = filename.split('.')[-1].lower()
        if file_ext not in ["mp3", "wav", "ogg"]:
            raise HTTPException(
                status_code=400,
                detail="Поддерживаются только MP3, WAV, OGG"
            )

        temp_path = Path(settings.TEMP_DIR) / f"{uuid.uuid4()}.{file_ext}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            if len(content) > 100 * 1024 * 1024:  # 100MB лимит
                raise HTTPException(status_code=413, detail="Файл слишком большой")
            buffer.write(content)

        transcript = Transcriber().transcribe(str(temp_path))
        summary =  Summarizer().summarize(transcript)

        return {
            "status": "success",
            "text": transcript,
            "summary": summary
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обработки: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка обработки файла")
