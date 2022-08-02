from fastapi import FastAPI

from app.settings import app_settings

app = FastAPI(
    version=app_settings.app_version
)


@app.get("/")
def root():
    return {"message": "URL shortener app"}
