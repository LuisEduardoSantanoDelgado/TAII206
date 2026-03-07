from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import asyncio
import  jwt 

#conf del jwt

SECRET_KEY = "1942"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(
    title='Mi API con JWT',
    description='Luis Eduardo Santano Delgado - Práctica 7',
    version='2.0',
)

usuarios_db = [
    {"id": 1, "Nombre": "Anuel", "edad": 32},
    {"id": 2, "Nombre": "Mauricio", "edad": 20},
    {"id": 3, "Nombre": "Luis Eduardo", "edad": 21},
]

USUARIO_SISTEMA = {"username": "admin", "password": "1942"}


class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=0, le=121)

class Token(BaseModel):
    access_token: str
    token_type: str

def crear_token_acceso(data: dict):
    datos_a_cifrar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_cifrar.update({"exp": expiracion})
    encoded_jwt = jwt.encode(datos_a_cifrar, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validar_token(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token o ha expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha caducado, por favor obtenga uno nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token", response_model=Token, tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    if form_data.username != USUARIO_SISTEMA["username"] or form_data.password != USUARIO_SISTEMA["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = crear_token_acceso(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ENDPOINTS

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola mundo FastAPI con JWT"}

@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return {"status": "200", "total": len(usuarios_db), "data": usuarios_db}

@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario: UsuarioBase):
    for usr in usuarios_db:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios_db.append(usuario.dict())
    return {"mensaje": "Usuario Agregado", "datos": usuario, "status": "200"}

# endpoints jwt

@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario: dict, username: str = Depends(validar_token)):
    for idx, usr in enumerate(usuarios_db):
        if usr["id"] == id:
            usuarios_db[idx].update(usuario)
            return {
                "mensaje": f"Usuario actualizado por {username}",
                "datos": usuarios_db[idx],
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, username: str = Depends(validar_token)):
    for idx, usr in enumerate(usuarios_db):
        if usr["id"] == id:
            del usuarios_db[idx]
            return {
                "mensaje": f"Usuario eliminado correctamente por {username}",
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

