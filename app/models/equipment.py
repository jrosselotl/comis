from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    location_1_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location_2_id = Column(Integer, ForeignKey("location.id"), nullable=True)

    equipment_type_id = Column(Integer, ForeignKey("equipment_type.id"), nullable=False)
    sub_equipment_type_id = Column(Integer, ForeignKey("equipment_type.id"), nullable=True)

    number_location_1 = Column(Integer, nullable=False, default=1)
    number_location_2 = Column(Integer, nullable=True)
    number_equipment_type = Column(Integer, nullable=False, default=1)
    number_sub_equipment_type = Column(Integer, nullable=True)

    terminal = Column(String(50), nullable=True)
    power_type = Column(String(50), nullable=True)  # antes "tipo_alimentacion"
    cable_set = Column(Integer, nullable=True)
    code = Column(String(100), unique=True, nullable=False)  # antes "codigo"
    created_at = Column(DateTime, default=datetime.utcnow)  # antes "fecha_creacion"

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
