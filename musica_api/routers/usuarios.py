from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from musica_api.database import get_session
from musica_api.models import Cancion, Favorito, Usuario
from musica_api.schemas import UsuarioCreate, UsuarioUpdate

router = APIRouter()


@router.get("/", response_model=list[Usuario])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Usuario).offset(skip).limit(limit)).all()


@router.post("/", response_model=Usuario, status_code=201)
def crear_usuario(data: UsuarioCreate, session: Session = Depends(get_session)):
    if session.exec(select(Usuario).where(Usuario.correo == data.correo)).first():
        raise HTTPException(400, "Correo ya registrado")
    u = Usuario(nombre=data.nombre, correo=data.correo)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@router.get("/{id}", response_model=Usuario)
def obtener_usuario(id: int, session: Session = Depends(get_session)):
    u = session.get(Usuario, id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u


@router.put("/{id}", response_model=Usuario)
def actualizar_usuario(id: int, data: UsuarioUpdate, session: Session = Depends(get_session)):
    u = session.get(Usuario, id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    if data.nombre:
        u.nombre = data.nombre
    if data.correo:
        u.correo = data.correo
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@router.delete("/{id}")
def eliminar_usuario(id: int, session: Session = Depends(get_session)):
    u = session.get(Usuario, id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    session.delete(u)
    session.commit()
    return {"mensaje": "Usuario eliminado"}


@router.get("/{id}/favoritos")
def favoritos_usuario(id: int, session: Session = Depends(get_session)):
    favs = session.exec(select(Favorito).where(Favorito.id_usuario == id)).all()
    return [session.get(Cancion, f.id_cancion) for f in favs]


@router.post("/{id_usuario}/favoritos/{id_cancion}", status_code=201)
def marcar_favorito_usuario(id_usuario: int, id_cancion: int, session: Session = Depends(get_session)):
    if not session.get(Usuario, id_usuario):
        raise HTTPException(404, "Usuario no encontrado")
    if not session.get(Cancion, id_cancion):
        raise HTTPException(404, "Canción no encontrada")
    if session.exec(
        select(Favorito).where(Favorito.id_usuario == id_usuario, Favorito.id_cancion == id_cancion)
    ).first():
        raise HTTPException(400, "Ya es favorito")
    f = Favorito(id_usuario=id_usuario, id_cancion=id_cancion)
    session.add(f)
    session.commit()
    session.refresh(f)
    return f


@router.delete("/{id_usuario}/favoritos/{id_cancion}")
def eliminar_favorito_usuario(id_usuario: int, id_cancion: int, session: Session = Depends(get_session)):
    f = session.exec(
        select(Favorito).where(Favorito.id_usuario == id_usuario, Favorito.id_cancion == id_cancion)
    ).first()
    if not f:
        raise HTTPException(404, "Favorito no encontrado")
    session.delete(f)
    session.commit()
    return {"mensaje": "Favorito eliminado"}
