# Task Manager API

API REST para gestión de tareas (CRUD) construida con **FastAPI** y **MongoDB**, siguiendo una arquitectura por capas.

Proyecto académico — UADE.

## Stack

- **FastAPI** — framework web
- **MongoDB** (via **Motor**, driver async) — base de datos NoSQL
- **Pydantic** — validación de datos (DTOs)
- **Docker / Docker Compose** — contenerización
- **pytest** + **mongomock-motor** — testing sin depender de una base real

## Arquitectura

```
app/
├── models/       # Entidades de dominio (POO): Tarea, con su comportamiento e invariantes
├── schemas/      # DTOs de Pydantic: forma de los datos que entran/salen por HTTP
├── repositories/ # Única capa que habla con MongoDB
├── services/     # Lógica de negocio, agnóstica de HTTP y de la base de datos
├── routers/      # Endpoints HTTP: reciben el request, llaman al service, devuelven la respuesta
├── database.py   # Conexión a MongoDB
└── main.py       # Punto de entrada de la app FastAPI
```

Cada capa solo conoce a la de al lado (routers → services → repositories → models/schemas). Si el día de mañana se cambia MongoDB por otra base, solo se toca `repositories/`.

## Cómo correrlo

### Con Docker (recomendado)

Requiere Docker Desktop corriendo.

```bash
docker compose up -d --build
```

Levanta dos servicios:

- **api** — la aplicación FastAPI en `http://localhost:8000`
- **mongo** — MongoDB en `localhost:27017`

Para bajarlo:

```bash
docker compose down
```

### Sin Docker (local)

Requiere una instancia de MongoDB corriendo (local o remota).

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt

set MONGO_URI=mongodb://localhost:27017   # opcional, este es el default
set MONGO_DB=gestor_tareas                # opcional, este es el default

uvicorn app.main:app --reload
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/tareas/` | Crear una tarea |
| `GET` | `/tareas/` | Listar tareas (con `skip`/`limit` opcionales) |
| `GET` | `/tareas/{id}` | Obtener una tarea por id |
| `PUT` | `/tareas/{id}` | Actualizar una tarea |
| `DELETE` | `/tareas/{id}` | Eliminar una tarea |

Documentación interactiva (Swagger) disponible en `http://localhost:8000/docs` con la app corriendo.

## Tests

Los tests usan `mongomock-motor` (una base Mongo simulada en memoria), por lo que no requieren Docker ni una base real corriendo:

```bash
pip install -r requirements.txt
pytest tests/ -v
```
