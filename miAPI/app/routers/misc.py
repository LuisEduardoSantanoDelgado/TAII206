from fastapi import FastAPI,status, HTTPException, Depends, APIRouter
from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Miscelanius"])




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

