from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestContinuity(Base):
    __tablename__ = "test_continuity"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    test_id = Column(Integer, ForeignKey("test.id"))
    date = Column(DateTime, default=datetime.utcnow)

    result = relationship("ResultContinuity", back_populates="test")
    equipment = relationship("Equipment")
    user = relationship("User", back_populates="test_continuity")
    project = relationship("Project", back_populates="test_continuity")


class ResultContinuity(Base):
    __tablename__ = "result_continuity"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_continuity.id"))
    test_point = Column(String, nullable=False)
    result_value = Column(Float, nullable=True)
    unit = Column(String, nullable=False)
    observation = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    cable_set = Column(Integer, nullable=True)

    test = relationship("TestContinuity", back_populates="result")
