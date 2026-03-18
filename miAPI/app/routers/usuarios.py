from fastapi import FastAPI,status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_peticion
from flask import app
import asyncio
from typing import Optional


router= APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]

)

#Endpoints
@router.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@router.get("/v1/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenido a tu API REST"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"Tu calificacion en TAI es 10"}

@router.get("/v1/parametroO/{id}")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }

@router.get("/v1/parametroOp/")
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                 return { "usuario encontrado":id ,"Datos":usuario}
        else:
            return { "Mensaje":"Usuario no encontrado"}
    else: 
        return { "Aviso":"No se proporciono Id"}

@router.get("/v1/usuarios/")
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@router.post("/v1/usuarios/")
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios: 
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usario Agregado",
        "datos":usuario,
        "status":"200"
    }
    
@router.put("/v1/usuarios/{id}")
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuarios[idx],
                "status": "200"
            }
            
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )

@router.delete("/v1/usuarios/{id}")
async def eliminar_usuario(id: int, usuarioAuth:str= Depends(verificar_peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuarioAuth}",
                "status": "200"
            }
        raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )
    