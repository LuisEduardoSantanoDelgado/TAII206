from pydantic import BaseModel, Field 

from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Luis Eduardo")
    edad: int = Field(..., ge=0, le=121, description="Edad validada entre 0 y 121", example="21")


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre del usuario", example="Luis Eduardo")
    edad: Optional[int] = Field(None, ge=0, le=121, description="Edad validada entre 0 y 121", example="21")


class UsuarioSchema(UsuarioBase):
    id: int = Field(..., gt=0, description="identificador de usuario", example="1")

    class Config:
        from_attributes = True
