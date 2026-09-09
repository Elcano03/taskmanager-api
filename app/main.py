from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import tareas

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Gestor de Tareas")

app.include_router(tareas.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def raiz():
    return FileResponse(STATIC_DIR / "index.html")
