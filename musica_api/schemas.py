from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2)
    correo: EmailStr | None = None


class CancionCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    artista: str = Field(min_length=1, max_length=150)
    album: str | None = None
    duracion: int = Field(gt=0)
    año: int = Field(ge=1900, le=2026)
    genero: str = Field(min_length=1, max_length=50)


class CancionUpdate(BaseModel):
    titulo: str | None = None
    artista: str | None = None
    album: str | None = None
    duracion: int | None = Field(default=None, gt=0)
    año: int | None = Field(default=None, ge=1900, le=2026)
    genero: str | None = None


class FavoritoCreate(BaseModel):
    id_usuario: int
    id_cancion: int
