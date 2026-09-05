from datetime import datetime, timezone


class Tarea:
    """Entidad de dominio: una tarea, con su comportamiento e invariantes."""

    def __init__(
        self,
        titulo: str,
        descripcion: str | None = None,
        completada: bool = False,
        id: str | None = None,
        creada_en: datetime | None = None,
    ):
        self._id = id
        self.titulo = titulo
        self._descripcion = descripcion
        self._completada = completada
        self._creada_en = creada_en or datetime.now(timezone.utc)

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El titulo de la tarea no puede estar vacio")
        self._titulo = valor

    @property
    def descripcion(self) -> str | None:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str | None) -> None:
        self._descripcion = valor

    @property
    def completada(self) -> bool:
        return self._completada

    @property
    def creada_en(self) -> datetime:
        return self._creada_en

    def completar(self) -> None:
        self._completada = True

    def reabrir(self) -> None:
        self._completada = False

    def aplicar_cambios(
        self,
        titulo: str | None = None,
        descripcion: str | None = None,
        completada: bool | None = None,
    ) -> None:
        if titulo is not None:
            self.titulo = titulo
        if descripcion is not None:
            self.descripcion = descripcion
        if completada is not None:
            self._completada = completada
