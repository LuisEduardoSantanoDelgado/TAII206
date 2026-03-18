from pydantic import BaseModel, Field 

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0,description="identificador de usuario",example="1")
    nombre: str =Field(...,min_length=3,max_length=50, description="Nombre del usuario",example="Luis Eduardo")
    edad: int =Field(...,ge=0,le=121,description="Edad validada entre 0 y 121",example="21")
