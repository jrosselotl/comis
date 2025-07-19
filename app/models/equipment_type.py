from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class EquipmentType(Base):
    __tablename__ = "equipment_type"

    id = Column(Integer, primary_key=True, index=True)
    equipment_type = Column(String(50), nullable=False)
    equipment_type_number = Column(JSON, nullable=True)  # Example: [1,2,3,4]
    sub_equipment = Column(String(50), nullable=True)
    sub_equipment_number = Column(JSON, nullable=True)   # Example: [1,2,3]
