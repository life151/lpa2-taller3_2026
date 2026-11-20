from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def ahora():
    return datetime.now(UTC)


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100)
    correo: str = Field(unique=True, index=True, max_length=150)
    fecha_registro: datetime = Field(default_factory=ahora)


class Cancion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(min_length=1, max_length=200)
    artista: str = Field(min_length=1, max_length=150)
    album: str | None = Field(default=None, max_length=200)
    duracion: int = Field(gt=0)
    año: int = Field(ge=1900, le=2026)
    genero: str = Field(max_length=50)
    fecha_creacion: datetime = Field(default_factory=ahora)


class Favorito(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id")
    id_cancion: int = Field(foreign_key="cancion.id")
    fecha_marcado: datetime = Field(default_factory=ahora)
