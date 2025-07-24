from pydantic import BaseModel, constr
from typing import Optional

class ResultContinuityBase(BaseModel):
    test_performed_id: int
    test_point: constr(min_length=1, max_length=50)
    result_value: Optional[float]
    cable_set: Optional[int]
    power_type: Optional[str]
    unit: Optional[str]
    image_url: Optional[str]
    observation: Optional[str]

class ResultContinuityCreate(ResultContinuityBase):
    pass

class ResultContinuityResponse(ResultContinuityBase):
    id: int

    class Config:
        orm_mode = True
