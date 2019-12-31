from fastapi import FastAPI
from routers import video
from core.config import settings
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(video.router)