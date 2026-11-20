from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from musica_api.database import get_session
from musica_api.models import Favorito
from musica_api.schemas import FavoritoCreate

router = APIRouter()


@router.get("/", response_model=list[Favorito])
def listar_favoritos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Favorito).offset(skip).limit(limit)).all()


@router.post("/", response_model=Favorito, status_code=201)
def crear_favorito(data: FavoritoCreate, session: Session = Depends(get_session)):
    if session.exec(
        select(Favorito).where(
            Favorito.id_usuario == data.id_usuario,
            Favorito.id_cancion == data.id_cancion,
        )
    ).first():
        raise HTTPException(400, "Ya es favorito")
    f = Favorito(**data.model_dump())
    session.add(f)
    session.commit()
    session.refresh(f)
    return f


@router.get("/{id}", response_model=Favorito)
def obtener_favorito(id: int, session: Session = Depends(get_session)):
    f = session.get(Favorito, id)
    if not f:
        raise HTTPException(404, "Favorito no encontrado")
    return f


@router.delete("/{id}")
def eliminar_favorito(id: int, session: Session = Depends(get_session)):
    f = session.get(Favorito, id)
    if not f:
        raise HTTPException(404, "Favorito no encontrado")
    session.delete(f)
    session.commit()
    return {"mensaje": "Favorito eliminado"}
