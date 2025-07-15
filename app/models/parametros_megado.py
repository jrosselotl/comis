from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ParametroMegado(Base):
    __tablename__ = "parametros_megado"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    codigo_equipo = Column(String, nullable=False)
    logica = Column(String, nullable=False)  # Ej: 'mayor_igual', 'igual'
    referencia = Column(String, nullable=False)
    unidad = Column(String, nullable=False)  # Ej: 'MΩ'
    voltaje = Column(String, nullable=True)
    duracion = Column(String, nullable=True)  # Tiempo de prueba recomendado

    proyecto = relationship("Proyecto", back_populates="parametros_megado")
