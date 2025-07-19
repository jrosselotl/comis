from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultIsolationSchema(BaseModel):
    test_point: str
    result_value: Optional[float]
    unit: str
    applied_time: Optional[float] = None  # 🔹 Entered manually by technician
    observation: Optional[str] = None
    image: Optional[str] = None
    cable_set: Optional[int] = None

class TestIsolationSchema(BaseModel):
    equipment_id: int
    user_id: int
    test_id: int
    date: Optional[datetime] = None
    result: List[ResultIsolationSchema]

    class Config:
        from_attributes = True
