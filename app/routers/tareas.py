from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.models.tarea import Tarea
from app.repositories.tarea_repository import TareaRepository
from app.schemas.tarea import TareaCreate, TareaOut, TareaUpdate
from app.services.tarea_service import TareaService

router = APIRouter(prefix="/tareas", tags=["tareas"])


def get_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> TareaService:
    return TareaService(TareaRepository(db))


def _a_schema(tarea: Tarea) -> TareaOut:
    return TareaOut(
        id=tarea.id,
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        completada=tarea.completada,
        creada_en=tarea.creada_en,
    )


@router.post("/", response_model=TareaOut, status_code=201)
async def crear_tarea(tarea: TareaCreate, service: TareaService = Depends(get_service)):
    creada = await service.crear_tarea(tarea)
    return _a_schema(creada)


@router.get("/", response_model=list[TareaOut])
async def listar_tareas(
    skip: int = 0, limit: int = 100, service: TareaService = Depends(get_service)
):
    tareas = await service.listar_tareas(skip=skip, limit=limit)
    return [_a_schema(t) for t in tareas]


@router.get("/{tarea_id}", response_model=TareaOut)
async def obtener_tarea(tarea_id: str, service: TareaService = Depends(get_service)):
    tarea = await service.obtener_tarea(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return _a_schema(tarea)


@router.put("/{tarea_id}", response_model=TareaOut)
async def actualizar_tarea(
    tarea_id: str, cambios: TareaUpdate, service: TareaService = Depends(get_service)
):
    tarea = await service.actualizar_tarea(tarea_id, cambios)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return _a_schema(tarea)


@router.delete("/{tarea_id}", status_code=204)
async def eliminar_tarea(tarea_id: str, service: TareaService = Depends(get_service)):
    eliminado = await service.eliminar_tarea(tarea_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
