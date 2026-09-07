from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.tarea import Tarea


def _a_documento(tarea: Tarea) -> dict:
    return {
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "completada": tarea.completada,
        "creada_en": tarea.creada_en,
    }


def _a_tarea(documento: dict) -> Tarea:
    return Tarea(
        id=str(documento["_id"]),
        titulo=documento["titulo"],
        descripcion=documento.get("descripcion"),
        completada=documento.get("completada", False),
        creada_en=documento.get("creada_en"),
    )


class TareaRepository:
    """Unico punto de contacto con la coleccion 'tareas' de MongoDB."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self._coleccion = db["tareas"]

    async def crear(self, tarea: Tarea) -> Tarea:
        resultado = await self._coleccion.insert_one(_a_documento(tarea))
        documento = await self._coleccion.find_one({"_id": resultado.inserted_id})
        return _a_tarea(documento)

    async def listar(self, skip: int = 0, limit: int = 100) -> list[Tarea]:
        cursor = self._coleccion.find().skip(skip).limit(limit)
        return [_a_tarea(doc) async for doc in cursor]

    async def obtener_por_id(self, tarea_id: str) -> Tarea | None:
        oid = self._a_object_id(tarea_id)
        if oid is None:
            return None
        documento = await self._coleccion.find_one({"_id": oid})
        return _a_tarea(documento) if documento else None

    async def actualizar(self, tarea_id: str, cambios: dict) -> Tarea | None:
        oid = self._a_object_id(tarea_id)
        if oid is None:
            return None
        if cambios:
            await self._coleccion.update_one({"_id": oid}, {"$set": cambios})
        documento = await self._coleccion.find_one({"_id": oid})
        return _a_tarea(documento) if documento else None

    async def eliminar(self, tarea_id: str) -> bool:
        oid = self._a_object_id(tarea_id)
        if oid is None:
            return False
        resultado = await self._coleccion.delete_one({"_id": oid})
        return resultado.deleted_count == 1

    @staticmethod
    def _a_object_id(tarea_id: str) -> ObjectId | None:
        try:
            return ObjectId(tarea_id)
        except InvalidId:
            return None
