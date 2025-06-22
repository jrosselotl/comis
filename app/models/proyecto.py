from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con equipos
    equipos = relationship("Equipo", back_populates="proyecto")
