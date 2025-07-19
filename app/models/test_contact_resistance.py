from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class TestContactResistance(Base):
    __tablename__ = "test_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    power_type = Column(String, nullable=False)  # tipo_alimentacion → power_type
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, default=datetime.utcnow)

    result = relationship("ResultContactResistance", back_populates="test")
    project = relationship("Project", back_populates="test_contact_resistance")
    equipment = relationship("Equipment", back_populates="test_contact_resistance")
    user = relationship("User", back_populates="test_contact_resistance")


class ResultContactResistance(Base):
    __tablename__ = "result_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_contact_resistance.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    cable_point = Column(String, nullable=False)  # punto_prueba → cable_point
    reference_value = Column(String, nullable=False)  # referencia_valor → reference_value
    result_value = Column(String, nullable=True)  # resultado_valor → result_value
    unit = Column(String, nullable=False)  # unidad → unit
    observation = Column(String, nullable=True)  # observaciones → observation
    image = Column(String, nullable=True)  # imagen → image

    test = relationship("TestContactResistance", back_populates="result")
