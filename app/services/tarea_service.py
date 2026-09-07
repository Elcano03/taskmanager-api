from app.models.tarea import Tarea
from app.repositories.tarea_repository import TareaRepository
from app.schemas.tarea import TareaCreate, TareaUpdate


class TareaService:
    """Logica de negocio del CRUD de tareas, agnostica de HTTP y de Mongo."""

    def __init__(self, repository: TareaRepository):
        self._repository = repository

    async def crear_tarea(self, datos: TareaCreate) -> Tarea:
        tarea = Tarea(
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            completada=datos.completada,
        )
        return await self._repository.crear(tarea)

    async def listar_tareas(self, skip: int = 0, limit: int = 100) -> list[Tarea]:
        return await self._repository.listar(skip, limit)

    async def obtener_tarea(self, tarea_id: str) -> Tarea | None:
        return await self._repository.obtener_por_id(tarea_id)

    async def actualizar_tarea(self, tarea_id: str, cambios: TareaUpdate) -> Tarea | None:
        datos = cambios.model_dump(exclude_unset=True)
        return await self._repository.actualizar(tarea_id, datos)

    async def eliminar_tarea(self, tarea_id: str) -> bool:
        return await self._repository.eliminar(tarea_id)
