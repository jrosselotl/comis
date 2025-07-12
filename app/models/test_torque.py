from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestTorque(Base):
    __tablename__ = "test_torque"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    equipo = relationship("Equipo", back_populates="tests_torque")
    usuario = relationship("Usuario", back_populates="tests_torque")
    resultados = relationship("ResultadoTorque", back_populates="test", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="tests_torque")


class ResultadoTorque(Base):
    __tablename__ = "resultado_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_torque.id", ondelete="CASCADE"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String(100), nullable=False)
    valor_nominal = Column(Float, nullable=False)
    valor_comprobado = Column(Float, nullable=True)
    aprobado = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)
    tipo_alimentacion = Column(String(50), nullable=True)

    test = relationship("TestTorque", back_populates="resultados")
