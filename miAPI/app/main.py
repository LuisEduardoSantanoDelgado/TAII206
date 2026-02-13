from fastapi import FastAPI, HTTPException
from typing import Optional
import asyncio

# Inicialización
app = FastAPI(
    title='Mi Primer API',
    description='Luis Eduardo Santano Delgado',
    version='1.0',
)

usuarios = [
    {"id": 1, "Nombre": "Anuel", "edad": 32},
    {"id": 2, "Nombre": "Mauricio", "edad": 20},
    {"id": 3, "Nombre": "Luis Eduardo", "edad": 21},
]

# EndPoint
@app.get("/", tags=['inicio'])
async def HolaAnuel():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['inicio'])
async def Bienvenidos():
    return {"mensaje": "Bienvenidos a tu FastAPI"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "Tu calificacion en TAI es 10"}

@app.get("/v1/usuarios/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id: int):
    return {"Usuario Encontrado": id}

@app.get("/v1/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)
    if id is not None:
        return {"Usuario Encontrado": id}

@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
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

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": "Usuario eliminado",
                "status": "200"
            }
    
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )