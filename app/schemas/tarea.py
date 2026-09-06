from datetime import datetime

from pydantic import BaseModel, Field


class TareaBase(BaseModel):
    titulo: str = Field(..., min_length=1)
    descripcion: str | None = None
    completada: bool = False


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1)
    descripcion: str | None = None
    completada: bool | None = None


class TareaOut(TareaBase):
    id: str
    creada_en: datetime
