from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TestPerformed(Base):
    __tablename__ = "test_performed"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    status = Column(String, default="incomplete")  # Valores: incomplete, completed, sent, etc.
    date = Column(DateTime, default=datetime.utcnow)

    # ✅ Relaciones
    project = relationship("Project", back_populates="test_performed")
    equipment = relationship("Equipment", back_populates="test_performed")
    user = relationship("User", back_populates="test_performed")
    test = relationship("Test", back_populates="test_performed")

    # ✅ Relaciones con resultados
    result_continuity = relationship("ResultContinuity", back_populates="test_performed", cascade="all, delete-orphan")
    result_isolation = relationship("ResultIsolation", back_populates="test_performed", cascade="all, delete-orphan")
    result_contact_resistance = relationship("ResultContactResistance", back_populates="test_performed", cascade="all, delete-orphan")
    result_torque = relationship("ResultTorque", back_populates="test_performed", cascade="all, delete-orphan")
