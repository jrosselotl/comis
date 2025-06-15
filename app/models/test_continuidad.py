from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestContinuidad(Base):
    __tablename__ = "test_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    observaciones = Column(String(255))

    equipo = relationship("Equipo", backref="tests_continuidad")
    usuario = relationship("Usuario", backref="tests_continuidad")

class ResultadoContinuidad(Base):
    __tablename__ = "resultado_continuidad"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_continuidad.id"), nullable=False)
    punto_prueba = Column(String(50), nullable=False)
    referencia_valor = Column(String(50))
    resultado_valor = Column(String(50))
    aprobado = Column(Boolean, default=False)
    imagen_url = Column(String(255))  # NUEVO: ruta del archivo de imagen

    test = relationship("TestContinuidad", backref="resultados")
