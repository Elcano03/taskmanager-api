import os
import socket

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "gestor_tareas")

# Algunos hosts en la nube (ej. Render) tienen salida IPv6 con problemas que
# rompen el handshake TLS contra Atlas. Forzamos resolucion DNS a IPv4.
_getaddrinfo_original = socket.getaddrinfo


def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _getaddrinfo_original(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = _getaddrinfo_ipv4

# Atlas (mongodb+srv://) siempre usa TLS; el Mongo local de Docker Compose no.
if MONGO_URI.startswith("mongodb+srv://"):
    client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
else:
    client = AsyncIOMotorClient(MONGO_URI)


def get_db() -> AsyncIOMotorDatabase:
    return client[MONGO_DB]
