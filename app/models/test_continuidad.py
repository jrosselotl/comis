from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestContinuidad(Base):
    __tablename__ = "test_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    observaciones = Column(String(255), nullable=True)

    equipo = relationship("Equipo", back_populates="tests_continuidad")
    usuario = relationship("Usuario", back_populates="tests_continuidad")
    resultados = relationship("ResultadoContinuidad", back_populates="test", cascade="all, delete-orphan")


class ResultadoContinuidad(Base):
    __tablename__ = "resultado_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_continuidad.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String(100), nullable=False)
    referencia_valor = Column(Float, nullable=True)
    resultado_valor = Column(Float, nullable=True)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)
    tipo_alimentacion = Column(String(20), nullable=True)

    test = relationship("TestContinuidad", back_populates="resultados")
