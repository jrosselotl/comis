from pydantic import BaseModel, constr
from typing import Optional

class ResultTorqueBase(BaseModel):
    test_performed_id: int
    test_point: constr(min_length=1, max_length=50)
    nominal_value: float
    check_value: Optional[float]
    unit: Optional[str]
    image_url: Optional[str]
    observation: Optional[str]

class ResultTorqueCreate(ResultTorqueBase):
    pass

class ResultTorqueResponse(ResultTorqueBase):
    id: int

    class Config:
        orm_mode = True
