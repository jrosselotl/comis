from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultTorqueSchema(BaseModel):
    cable_set: Optional[int] = None
    test_point: str
    nominal_value: Optional[float] = None
    verification_value: Optional[float] = None  # 🔹 Technician input
    unit: Optional[str] = None
    observation: Optional[str] = None
    image: Optional[str] = None

class TestTorqueSchema(BaseModel):
    equipment_id: int
    user_id: Optional[int] = None
    test_id: Optional[int] = None
    date: Optional[datetime] = None
    result: List[ResultTorqueSchema]

    class Config:
        from_attributes = True
