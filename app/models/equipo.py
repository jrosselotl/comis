import enum
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base

class TipoEquipo(str, Enum):
    COLO = "COLO"
    CE = "CE"
    PDU = "PDU"
    BSW = "BSW"

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(SQLEnum(TipoEquipo, name="tipo_equipo"), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con proyecto
    proyecto = relationship("Proyecto", back_populates="equipos")
