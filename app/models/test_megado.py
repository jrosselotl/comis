from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestMegado(Base):
    __tablename__ = "test_megado"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    test_id = Column(Integer, ForeignKey("test.id"))
    date = Column(DateTime, default=datetime.utcnow)

    resultados = relationship("ResultadoMegado", back_populates="test")
    equipment = relationship("Equipment")
    user = relationship("User", back_populates="tests_megado")
    project = relationship("Project", back_populates="tests_megado")


class ResultadoMegado(Base):
    __tablename__ = "resultados_megado"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_megado.id"))
    punto = Column(String, nullable=False)
    resultado_valor = Column(Float, nullable=True)
    unidad = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)
    cable_set = Column(Integer, nullable=True)

    test = relationship("TestMegado", back_populates="resultados")
