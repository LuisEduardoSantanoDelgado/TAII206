from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@localhost:5432/DB_miapi"
)

# 2. Motor de conexión
engine = create_engine(DATABASE_URL)

# 3. Gestor de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base declarativa
Base = declarative_base()

# 5. Manejo de sesiones por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()