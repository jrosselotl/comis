from pydantic import BaseModel, constr
from typing import Optional

class ResultInsulationBase(BaseModel):
    test_performed_id: int
    test_point: constr(min_length=1, max_length=50)
    result_value: Optional[float]
    time_applied: Optional[int]
    unit: Optional[str]
    image_url: Optional[str]
    observation: Optional[str]

class ResultInsulationCreate(ResultInsulationBase):
    pass

class ResultInsulationResponse(ResultInsulationBase):
    id: int

    class Config:
        orm_mode = True
