from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# URL de la base de datos
DATABASE_URL = "postgresql://comisdb_user:hMBVHZu6kYFAirm17hJh8E3RebuMaQW2@dpg-d17hqm6mcj7s73d877qg-a.oregon-postgres.render.com/comisdb"

# Crear la conexión con esquema por defecto "public"
engine = create_engine(
    DATABASE_URL,
    echo=True,
    execution_options={"schema_translate_map": {None: "public"}}  # 👈 CLAVE
)

# Crear SessionLocal con el mismo esquema por defecto
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    execution_options={"schema_translate_map": {None: "public"}}  # 👈 CLAVE
)

Base = declarative_base()

# Dependency para usar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
