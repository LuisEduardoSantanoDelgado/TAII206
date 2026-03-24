from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models.usuario import UsuarioBase
from app.security.auth import verificar_peticion
from app.data.db import get_db
from app.data.usuario import Usuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)


@router.get("/")
async def consulta_usuarios(db: Session = Depends(get_db)):
    consulta_usuarios = db.query(Usuario).all()
    return {
        "status": 200,
        "total": len(consulta_usuarios),
        "data": consulta_usuarios
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
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


@router.put("/{nombre}", status_code=status.HTTP_200_OK)
async def editar_usuario(nombre: str, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.nombre == nombre).first()

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


@router.delete("/{nombre}")
async def eliminar_usuario(
    nombre: str,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario_db = db.query(Usuario).filter(Usuario.nombre == nombre).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario_db)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}",
        "status": 200
    }