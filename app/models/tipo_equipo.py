from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class TipoEquipo(Base):
    __tablename__ = "tipo_equipos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_equipo = Column(String(50), nullable=False)
    numero_tipo_equipo = Column(JSON, nullable=True)  # Ej: [1,2,3,4]
    sub_equipo = Column(String(50), nullable=True)
    numero_sub_equipo = Column(JSON, nullable=True)   # Ej: [1,2,3]
