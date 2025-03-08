from fastapi import FastAPI
from routers import video
from core.config import settings
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.PROJECT_NAME)
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(video.router)