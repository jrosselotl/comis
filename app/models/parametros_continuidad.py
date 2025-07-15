from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroContinuidad(Base):
    __tablename__ = "parametros_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    codigo_equipo = Column(String, nullable=False)
    logica = Column(String, nullable=False)  # Ej: 'menor_igual', 'igual'
    referencia = Column(String, nullable=False)
    unidad = Column(String, nullable=False)  # Ej: 'Ω', 'mΩ'

    proyecto = relationship("Proyecto", back_populates="parametros_continuidad")
