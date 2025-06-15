from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Tomar el valor de la variable DATABASE_URL
DATABASE_URL = "postgresql://comisdb_user:hMBVHZu6kYFAirm17hJh8E3RebuMaQW2@dpg-d17hqm6mcj7s73d877qg-a.oregon-postgres.render.com/comisdb"

# Crear la conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency para usar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
