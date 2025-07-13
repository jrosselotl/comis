from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.proyecto_tipo_test import ProyectoTipoTest

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con equipos
    equipos = relationship("Equipo", back_populates="proyecto")
    
    # ✅ Relación con tipos de test
    tipos_test = relationship("ProyectoTipoTest", back_populates="proyecto")
