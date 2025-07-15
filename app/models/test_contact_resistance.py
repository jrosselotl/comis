from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class TestContactResistance(Base):
    __tablename__ = "tests_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    tipo_alimentacion = Column(String, nullable=False)
    terminal = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    resultados = relationship("ResultadoContactResistance", back_populates="test")
    proyecto = relationship("Proyecto", back_populates="test_contact_resistance")
    equipo = relationship("Equipo", back_populates="test_contact_resistance")
    usuario = relationship("Usuario", back_populates="test_contact_resistance")


class ResultadoContactResistance(Base):
    __tablename__ = "resultados_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests_contact_resistance.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String, nullable=False)
    referencia_valor = Column(String, nullable=False)
    resultado_valor = Column(String, nullable=True)
    unidad = Column(String, nullable=False)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestContactResistance", back_populates="resultados")
