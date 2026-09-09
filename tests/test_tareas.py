from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from app.database import get_db
from app.main import app

_mongo_mock = AsyncMongoMockClient()["gestor_tareas_test"]


def override_get_db():
    return _mongo_mock


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_crear_tarea():
    respuesta = client.post("/tareas/", json={"titulo": "Comprar pan"})
    assert respuesta.status_code == 201
    data = respuesta.json()
    assert data["titulo"] == "Comprar pan"
    assert data["completada"] is False
    assert "id" in data


def test_listar_tareas():
    client.post("/tareas/", json={"titulo": "Tarea 1"})
    client.post("/tareas/", json={"titulo": "Tarea 2"})
    respuesta = client.get("/tareas/")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) >= 2


def test_obtener_tarea():
    creada = client.post("/tareas/", json={"titulo": "Tarea"}).json()
    respuesta = client.get(f"/tareas/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == creada["id"]


def test_obtener_tarea_inexistente():
    respuesta = client.get("/tareas/507f1f77bcf86cd799439011")
    assert respuesta.status_code == 404


def test_obtener_tarea_id_invalido():
    respuesta = client.get("/tareas/id-invalido")
    assert respuesta.status_code == 404


def test_actualizar_tarea():
    creada = client.post("/tareas/", json={"titulo": "Tarea"}).json()
    respuesta = client.put(f"/tareas/{creada['id']}", json={"completada": True})
    assert respuesta.status_code == 200
    assert respuesta.json()["completada"] is True
    assert respuesta.json()["titulo"] == "Tarea"


def test_actualizar_tarea_inexistente():
    respuesta = client.put(
        "/tareas/507f1f77bcf86cd799439011", json={"completada": True}
    )
    assert respuesta.status_code == 404


def test_eliminar_tarea():
    creada = client.post("/tareas/", json={"titulo": "Tarea"}).json()
    respuesta = client.delete(f"/tareas/{creada['id']}")
    assert respuesta.status_code == 204
    assert client.get(f"/tareas/{creada['id']}").status_code == 404


def test_eliminar_tarea_inexistente():
    respuesta = client.delete("/tareas/507f1f77bcf86cd799439011")
    assert respuesta.status_code == 404
