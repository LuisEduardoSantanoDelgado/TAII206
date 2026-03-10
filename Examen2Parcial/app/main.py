from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
from datetime import date
import secrets

app = FastAPI(
    title="API de Gestión de Citas",
    description="Una API para gestionar citas médicas",
    version="1.0",
)

security = HTTPBasic()

usuario = "root"
contraseña = "1234"

citas = [
    {
        "id": 1,
        "nombre": "Emmanuel Gazmey",
        "fecha": "2026-04-20",
        "motivo": "Consulta general",
        "confirmada": False
    },
    {
        "id": 2,
        "nombre": "Luis Santano",
        "fecha": "2026-04-20",
        "motivo": "Revisión médica",
        "confirmada": False
    }
]


def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credentials.username, usuario)
    password_correcto = secrets.compare_digest(credentials.password, contraseña)

    if not (usuario_correcto and password_correcto):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class CitaBase(BaseModel):
    id: int = Field(..., gt=0, description="ID de la cita", example=1)
    nombre: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Nombre del paciente",
        example="Luis Eduardo"
    )
    fecha: date = Field(
        ...,
        description="Fecha de la cita en formato YYYY-MM-DD",
        example="2026-04-20"
    )
    motivo: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Motivo de la cita",
        example="Consulta general"
    )
    confirmada: bool = Field(
        default=False,
        description="Estado de confirmación de la cita"
    )

    @field_validator("fecha")
    @classmethod
    def validar_fecha(cls, value: date):
        if value < date.today():
            raise ValueError("La fecha no puede ser menor a la actual")
        return value


class ConfirmarCita(BaseModel):
    confirmada: bool = Field(..., description="Estado de confirmación", example=True)



@app.post("/v1/citas/crear", tags=["Citas"], status_code=status.HTTP_201_CREATED)
async def crear_cita(cita: CitaBase):


    citas_mismo_paciente_mismo_dia = 0
    for c in citas:
        if c["nombre"].lower() == cita.nombre.lower() and c["fecha"] == str(cita.fecha):
            citas_mismo_paciente_mismo_dia += 1

    if citas_mismo_paciente_mismo_dia >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se permiten más de 3 citas en un día por paciente"
        )

    nueva_cita = cita.model_dump()
    nueva_cita["fecha"] = str(nueva_cita["fecha"])
    citas.append(nueva_cita)

    return {
        "mensaje": "Cita creada correctamente",
        "datos": nueva_cita,
        "status": 201
    }


@app.get("/v1/citas/lista", tags=["Citas"])
async def listar_citas(usuario: str = Depends(verificar_credenciales)):
    return {
        "status": 200,
        "usuario": usuario,
        "total": len(citas),
        "data": citas
    }



@app.get("/v1/citas/{id}/consulta", tags=["Citas"])
async def consultar_cita_por_id(id: int):
    for c in citas:
        if c["id"] == id:
            return {
                "status": 200,
                "data": c
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cita con id {id} no encontrada"
    )


@app.put("/v1/citas/{id}/confirmar", tags=["Citas"])
async def confirmar_cita(id: int, datos_confirmacion: ConfirmarCita):
    for idx, c in enumerate(citas):
        if c["id"] == id:
            citas[idx]["confirmada"] = datos_confirmacion.confirmada
            return {
                "mensaje": "Estado de confirmación actualizado correctamente",
                "datos": citas[idx],
                "status": 200
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cita con id {id} no encontrada"
    )


@app.delete("/v1/citas/{id}/eliminar", tags=["Citas"])
async def eliminar_cita(id: int, usuario: str = Depends(verificar_credenciales)):
    for idx, c in enumerate(citas):
        if c["id"] == id:
            eliminada = citas[idx]
            del citas[idx]
            return {
                "mensaje": f"Cita con id {id} eliminada correctamente.",
                "usuario": usuario,
                "data": eliminada,
                "status": 200
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cita con id {id} no encontrada"
    )