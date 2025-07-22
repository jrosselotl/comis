from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    location_1 = Column(String, nullable=False)
    number_location_1 = Column(Integer)
    location_2 = Column(String)
    number_location_2 = Column(Integer)
    equipment_type = Column(String)
    number_equipment_type = Column(Integer)
    sub_equipment = Column(String)
    number_sub_equipment = Column(Integer)
    terminal = Column(String)
    power_type = Column(String)
    cable_set = Column(Integer)
    code = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    test_continuity = relationship("TestContinuity", back_populates="equipment")
    test_isolation = relationship("TestIsolation", back_populates="equipment")
    test_contact_resistance = relationship("TestContactResistance", back_populates="equipment")
    test_torque = relationship("TestTorque", back_populates="equipment")
