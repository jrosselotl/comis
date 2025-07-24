from pydantic import BaseModel, constr
from typing import Optional

class ResultContactResistanceBase(BaseModel):
    test_performed_id: int
    test_point: constr(min_length=1, max_length=50)
    result_value: Optional[float]
    unit: Optional[str]
    image_url: Optional[str]
    observation: Optional[str]

class ResultContactResistanceCreate(ResultContactResistanceBase):
    pass

class ResultContactResistanceResponse(ResultContactResistanceBase):
    id: int

    class Config:
        orm_mode = True
