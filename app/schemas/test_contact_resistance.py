from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultContactResistanceSchema(BaseModel):
    cable_set: Optional[int]
    test_point: str
    result_value: Optional[float]
    unit: Optional[str]
    observation: Optional[str]
    image: Optional[str]

class TestContactResistanceSchema(BaseModel):
    project_id: int
    equipment_id: int
    user_id: Optional[int] = None
    test_id: Optional[int] = None
    date: Optional[datetime] = None
    result: List[ResultContactResistanceSchema]

    class Config:
        from_attributes = True
