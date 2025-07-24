from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResultContinuity(Base):
    __tablename__ = "result_continuity"

    id = Column(Integer, primary_key=True, index=True)
    test_performed_id = Column(Integer, ForeignKey("test_performed.id"), nullable=False)
    test_point = Column(String, nullable=False)
    result_value = Column(Float, nullable=True)
    unit = Column(String, nullable=False)
    observation = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    cable_set = Column(Integer, nullable=True)

    # ✅ Relación con test_performed
    test_performed = relationship("TestPerformed", back_populates="result_continuity")


