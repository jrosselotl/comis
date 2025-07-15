from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env (opcional si usas env)
load_dotenv()

# URL de la base de datos (Render requiere sslmode=require)
DATABASE_URL = (
    "postgresql+psycopg2://comisdb_user:hMBVHZu6kYFAirm17hJh8E3RebuMaQW2"
    "@dpg-d17hqm6mcj7s73d877qg-a.oregon-postgres.render.com/comisdb"
)

# ✅ Crear engine con reconexión automática y SSL habilitado
engine = create_engine(
    DATABASE_URL,
    echo=False,                 # pon True solo si quieres logs en consola
    pool_pre_ping=True,         # Verifica conexión antes de usarla
    pool_recycle=1800,          # Recicla conexiones cada 30 min (Render corta a veces)
    connect_args={"sslmode": "require"}  # Render requiere SSL
)

# ✅ Crear la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base declarativa
Base = declarative_base()

# ✅ Dependency para rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
