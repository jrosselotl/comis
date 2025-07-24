from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class ResultContinuity(Base):
    __tablename__ = "result_continuity"

    id = Column(Integer, primary_key=True, index=True)
    test_performed_id = Column(Integer, ForeignKey("test_performed.id"), nullable=False)

    test_point = Column(String(50), nullable=False)
    result_value = Column(Float)
    cable_set = Column(Integer)
    power_type = Column(String(50))
    unit = Column(String(20))
    image_url = Column(String(255))
    observation = Column(String)

    test_performed = relationship("TestPerformed")

