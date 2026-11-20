from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from musica_api.database import get_session
from musica_api.models import Cancion
from musica_api.schemas import CancionCreate, CancionUpdate

router = APIRouter()


@router.get("/", response_model=list[Cancion])
def listar_canciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Cancion).offset(skip).limit(limit)).all()


@router.get("/buscar", response_model=list[Cancion])
def buscar_canciones(
    titulo: str | None = None,
    artista: str | None = None,
    genero: str | None = None,
    session: Session = Depends(get_session),
):
    q = select(Cancion)
    if titulo:
        q = q.where(Cancion.titulo.contains(titulo))
    if artista:
        q = q.where(Cancion.artista.contains(artista))
    if genero:
        q = q.where(Cancion.genero.contains(genero))
    return session.exec(q).all()


@router.post("/", response_model=Cancion, status_code=201)
def crear_cancion(data: CancionCreate, session: Session = Depends(get_session)):
    c = Cancion(**data.model_dump())
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


@router.get("/{id}", response_model=Cancion)
def obtener_cancion(id: int, session: Session = Depends(get_session)):
    c = session.get(Cancion, id)
    if not c:
        raise HTTPException(404, "Canción no encontrada")
    return c


@router.put("/{id}", response_model=Cancion)
def actualizar_cancion(id: int, data: CancionUpdate, session: Session = Depends(get_session)):
    c = session.get(Cancion, id)
    if not c:
        raise HTTPException(404, "Canción no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


@router.delete("/{id}")
def eliminar_cancion(id: int, session: Session = Depends(get_session)):
    c = session.get(Cancion, id)
    if not c:
        raise HTTPException(404, "Canción no encontrada")
    session.delete(c)
    session.commit()
    return {"mensaje": "Canción eliminada"}
