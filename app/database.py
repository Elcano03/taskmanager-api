import os

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "gestor_tareas")

# Atlas (mongodb+srv://) siempre usa TLS; el Mongo local de Docker Compose no.
if MONGO_URI.startswith("mongodb+srv://"):
    client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
else:
    client = AsyncIOMotorClient(MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return client[MONGO_DB]
