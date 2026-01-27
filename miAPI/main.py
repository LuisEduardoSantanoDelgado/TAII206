#importaciones
from fastapi import FastAPI

#inicializacion
app= FastAPI()


#EndPoint

@app.get("/")
async def HolaAnuel():
    return{"mensaje":"Hola Mundo FastAPI"}


@app.get("/bienvenidos")
async def Bienvenidos():
    return{"mensaje":"Bienvenidos a tu FastAPI"}
