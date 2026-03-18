from fastapi import FastAPI
from app.routers.usuarios import router as usuarios_router
from app.routers.misc import router as misc_router

app = FastAPI(
    title='Mi API ',
    description='Luis Eduardo Santano Delgado - Práctica 8',
    version='1.0',
)


app.include_router(usuarios_router)
app.include_router(misc_router)


