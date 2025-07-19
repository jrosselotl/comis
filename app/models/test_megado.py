from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestIsolation(Base):
    __tablename__ = "test_isolation"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    test_id = Column(Integer, ForeignKey("test.id"))
    date = Column(DateTime, default=datetime.utcnow)

    result = relationship("ResultIsolation", back_populates="test")
    equipment = relationship("Equipment")
    user = relationship("User", back_populates="test_isolation")
    project = relationship("Project", back_populates="test_isolation")


class ResultIsolation(Base):
    __tablename__ = "result_isolation"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_isolation.id"))
    test_point = Column(String, nullable=False)
    result_value = Column(Float, nullable=True)
    unit = Column(String, nullable=False)
    observation = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    cable_set = Column(Integer, nullable=True)
    applied_time = Column(Float, nullable=True)
    power_type = Column(String(50), nullable=True)

    test = relationship("TestIsolation", back_populates="result")
