from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TestPerformed(Base):
    __tablename__ = "test_performed"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("test.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="incomplete")  # Valores: incomplete, completed, sent, etc.
    date = Column(DateTime, default=datetime.utcnow)

    # ✅ Relaciones principales
    project = relationship("Project", back_populates="test_performed")
    equipment = relationship("Equipment", back_populates="test_performed")
    user = relationship("User", back_populates="test_performed")
    test = relationship("Test", back_populates="test_performed")

    # ✅ Relaciones con resultados (cascade para eliminar resultados si se elimina el test)
    result_continuity = relationship(
        "ResultContinuity",
        back_populates="test_performed",
        cascade="all, delete-orphan"
    )
    result_isolation = relationship(
        "ResultIsolation",
        back_populates="test_performed",
        cascade="all, delete-orphan"
    )
    result_contact_resistance = relationship(
        "ResultContactResistance",
        back_populates="test_performed",
        cascade="all, delete-orphan"
    )
    result_torque = relationship(
        "ResultTorque",
        back_populates="test_performed",
        cascade="all, delete-orphan"
    )
