from fastapi import FastAPI

from app.routers import tareas

app = FastAPI(title="Gestor de Tareas")

app.include_router(tareas.router)


@app.get("/")
def raiz():
    return {"mensaje": "API Gestor de Tareas"}
