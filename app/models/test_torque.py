from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class TestTorque(Base):
    __tablename__ = "test_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    power_type = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    result = relationship("ResultTorque", back_populates="test")
    project = relationship("Project", back_populates="test_torque")
    equipment = relationship("Equipment", back_populates="test_torque")
    user = relationship("User", back_populates="test_torque")


class ResultTorque(Base):
    __tablename__ = "result_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test_torque.id"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    test_point = Column(String, nullable=False)
    nominal_value = Column(Float, nullable=False)      # copied from torque parameter
    verification_value = Column(Float, nullable=True)  # entered by technician
    unit = Column(String, nullable=False)
    observation = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    test = relationship("TestTorque", back_populates="result")
