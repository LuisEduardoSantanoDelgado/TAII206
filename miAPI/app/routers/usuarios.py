from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.models.usuario import UsuarioCreate, UsuarioUpdate, UsuarioSchema
from app.security.auth import verificar_peticion
from app.data.db import get_db
from app.data.usuario import Usuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)


@router.get("/", response_model=None)
async def consulta_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {
        "status": 200,
        "total": len(usuarios),
        "data": usuarios
    }


@router.get("/{id}")
async def consulta_usuario_por_id(id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return {
        "status": 200,
        "data": usuario_db
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario agregado",
        "datos": nuevo_usuario,
        "status": 201
    }


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def editar_usuario(id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario editado",
        "datos": usuario_db,
        "status": 200
    }


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(usuario_db, key, value)

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario actualizado",
        "datos": usuario_db,
        "status": 200
    }


@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario_db = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario_db)
    db.commit()

    return {
        "mensaje": f"Usuario con ID {usuario_id} eliminado correctamente por {usuarioAuth}",
        "status": 200
    }