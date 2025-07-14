from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestMegado(Base):
    __tablename__ = "test_megado"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    fecha = Column(DateTime, default=datetime.utcnow)

    resultados = relationship("ResultadoMegado", back_populates="test")
    equipo = relationship("Equipo")
    usuario = relationship("Usuario", back_populates="tests_megado")
    test_ref = relationship("Test")

class ResultadoMegado(Base):
    __tablename__ = "resultados_megado"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_megado.id"))
    punto = Column(String, nullable=False)
    resultado_valor = Column(Float, nullable=True)
    unidad = Column(String, nullable=False)
    aprobado = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestMegado", back_populates="resultados")
