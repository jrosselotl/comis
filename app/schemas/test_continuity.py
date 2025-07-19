from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultContinuitySchema(BaseModel):
    test_point: str
    cable_set: Optional[int]
    result_value: Optional[float]
    unit: str
    observation: Optional[str]
    image: Optional[str]

class TestContinuitySchema(BaseModel):
    equipment_id: int
    user_id: int
    test_id: int
    date: Optional[datetime] = None
    result: List[ResultContinuitySchema]

    class Config:
        from_attributes = True
