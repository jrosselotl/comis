from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroContinuidad(Base):
    __tablename__ = "parametros_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    tipo_equipo = Column(String, nullable=False)
    logica = Column(String, nullable=False)  # Ej: "<", "<=", ">", ">=", "=="
    referencia = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)

    proyecto = relationship("Proyecto", back_populates="parametros_continuidad")
