from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field 
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

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0,description="identificador de usuario",example="1")
    nombre: str =Field(...,min_length=3,max_length=50, description="Nombre del usuario",example="Luis Eduardo")
    edad: int =Field(...,ge=0,le=121,description="Edad validada entre 0 y 121",example="21")
    
#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenido a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"Tu calificacion en TAI es 10"}

@app.get("/v1/parametroO/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
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

@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
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