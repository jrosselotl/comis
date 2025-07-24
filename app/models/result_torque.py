from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResultTorque(Base):
    __tablename__ = "result_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_performed_id = Column(Integer, ForeignKey("test_performed.id"), nullable=False)
    test_point = Column(String, nullable=False)
    nominal_value = Column(Float, nullable=True)        # Valor nominal especificado
    verification_value = Column(Float, nullable=True)   # Valor de comprobación real
    unit = Column(String, nullable=False)
    observation = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    cable_set = Column(Integer, nullable=True)

    # ✅ Relación con test_performed
    test_performed = relationship("TestPerformed", back_populates="result_torque")
