# app/models/test_contact_resistance.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestContactResistance(Base):
    __tablename__ = "test_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    equipo = relationship("Equipo", back_populates="tests_contact_resistance")
    usuario = relationship("Usuario", back_populates="tests_contact_resistance")
    resultados = relationship("ResultadoContactResistance", back_populates="test", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="tests_contact_resistance")


class ResultadoContactResistance(Base):
    __tablename__ = "resultado_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_contact_resistance.id", ondelete="CASCADE"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String(100), nullable=False)
    resultado_valor = Column(Float, nullable=True)
    referencia_valor = Column(Float, nullable=True)
    unidad = Column(String(50), nullable=True)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)
    tipo_alimentacion = Column(String(50), nullable=True)

    test = relationship("TestContactResistance", back_populates="resultados")
