from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    location_1 = Column(String(50), nullable=False)
    number_location_1 = Column(Integer, nullable=False, default=1)
    location_2 = Column(String(50), nullable=True)
    number_location_2 = Column(Integer, nullable=True)

    equipment_type = Column(String(50), nullable=False)
    number_equipment_type = Column(Integer, nullable=False, default=1)
    sub_equipment = Column(String(50), nullable=True)
    number_sub_equipment = Column(Integer, nullable=True)

    terminal = Column(String(50), nullable=True)
    power_type = Column(String(50), nullable=True)
    cable_set = Column(Integer, nullable=True)
    code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationships
    project = relationship("Project", back_populates="equipment")
    location_1 = relationship("Location", foreign_keys=[location_1_id])
    location_2 = relationship("Location", foreign_keys=[location_2_id])
    equipment_type = relationship("EquipmentType", foreign_keys=[equipment_type_id])
    sub_equipment_type = relationship("EquipmentType", foreign_keys=[sub_equipment_type_id])

    
    test_continuity = relationship("TestContinuity", back_populates="equipment")
    test_isolation = relationship("TestIsolation", back_populates="equipment")
    test_contact_resistance = relationship("TestContactResistance", back_populates="equipment")
    test_torque = relationship("TestTorque", back_populates="equipment")
