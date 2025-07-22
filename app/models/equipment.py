from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    # 👇 Se guardan como texto porque solo se consultan de tablas estáticas
    location_1 = Column(String(100), nullable=False)
    location_2 = Column(String(100), nullable=True)

    equipment_type = Column(String(50), nullable=False)
    sub_equipment = Column(String(100), nullable=True)

    number_location_1 = Column(Integer, nullable=False, default=1)
    number_location_2 = Column(Integer, nullable=True)
    number_equipment_type = Column(Integer, nullable=False, default=1)
    number_sub_equipment = Column(Integer, nullable=True)

    terminal = Column(String(50), nullable=True)
    power_type = Column(String(50), nullable=True)
    cable_set = Column(Integer, nullable=True)
    code = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="equipment")

    # ✅ Relación lógica con las tablas de test
    test_continuity = relationship("TestContinuity", back_populates="equipment")
    test_isolation = relationship("TestIsolation", back_populates="equipment")
    test_contact_resistance = relationship("TestContactResistance", back_populates="equipment")
    test_torque = relationship("TestTorque", back_populates="equipment")
