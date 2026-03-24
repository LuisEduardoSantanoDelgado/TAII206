from sqlalchemy import Column, Integer, String
from app.data.db import Base


class Usuario(Base):
    __tablename__ = "tb_usuarios"

    nombre = Column(String, primary_key=True, index=True)
    edad = Column(Integer, nullable=False)