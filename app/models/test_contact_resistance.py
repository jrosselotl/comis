from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class TestContactResistance(Base):
    __tablename__ = "tests_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    tipo_alimentacion = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    resultados = relationship("ResultadoContactResistance", back_populates="test")
    project = relationship("Project", back_populates="tests_contact_resistance")
    equipment = relationship("Equipment", back_populates="tests_contact_resistance")
    user= relationship("User", back_populates="tests_contact_resistance")

class ResultadoContactResistance(Base):
    __tablename__ = "resultados_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests_contact_resistance.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    punto_prueba = Column(String, nullable=False)
    referencia_valor = Column(String, nullable=False)
    resultado_valor = Column(String, nullable=True)
    unidad = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

    test = relationship("TestContactResistance", back_populates="resultados")
