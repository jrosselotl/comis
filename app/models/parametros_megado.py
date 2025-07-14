from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroMegado(Base):
    __tablename__ = "parametros_megado"

    id = Column(Integer, primary_key=True, index=True)
    tipo_equipo = Column(String, nullable=False)
    unidad = Column(String, nullable=False)
    voltaje = Column(String, nullable=True)     # visible solo para referencia
    corriente = Column(String, nullable=True)   # también como referencia
    duracion = Column(String, nullable=True)    # visible, no editable
    logica = Column(String, nullable=False)     # Ej: 'mayor_igual'
    referencia = Column(String, nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)

    proyecto = relationship("Proyecto", back_populates="parametros_megado")
