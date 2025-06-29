# app/models/test_megado.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestMegado(Base):
    __tablename__ = "test_megado"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # puede ser nullable si no siempre hay usuario
    fecha = Column(DateTime, default=datetime.utcnow)
    observaciones = Column(String(255), nullable=True)

    equipo = relationship("Equipo", back_populates="tests_megado")
    usuario = relationship("Usuario", back_populates="tests_megado")
    resultados = relationship("ResultadoMegado", back_populates="test", cascade="all, delete-orphan")

class ResultadoMegado(Base):
    __tablename__ = "resultado_megado"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_megado.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String(100), nullable=False)
    referencia_valor = Column(Float, nullable=True)
    resultado_valor = Column(Float, nullable=True)
    tiempo_aplicado = Column(Float, nullable=True)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)
    tipo_alimentacion = Column(String(20), nullable=True)

    test = relationship("TestMegado", back_populates="resultados")
