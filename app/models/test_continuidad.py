from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestContinuidad(Base):
    __tablename__ = "test_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))  # ✅ NUEVO
    fecha = Column(DateTime, default=datetime.utcnow)

    resultados = relationship("ResultadoContinuidad", back_populates="test")
    equipo = relationship("Equipo")
    usuario = relationship("Usuario", back_populates="tests_continuidad")
    test_ref = relationship("Test")
    proyecto = relationship("Proyecto", back_populates="tests_continuidad")  # ✅ NUEVO

class ResultadoContinuidad(Base):
    __tablename__ = "resultados_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_continuidad.id"))
    punto = Column(String, nullable=False)
    resultado_valor = Column(Float, nullable=True)
    unidad = Column(String, nullable=False)
    aprobado = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestContinuidad", back_populates="resultados")
