import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "gestor_tareas")

client = AsyncIOMotorClient(MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return client[MONGO_DB]
