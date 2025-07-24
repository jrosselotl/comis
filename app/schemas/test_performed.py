from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestPerformedBase(BaseModel):
    project_id: int
    equipment_id: int
    user_id: int
    test_id: int
    status: Optional[str] = "incomplete"

class TestPerformedCreate(TestPerformedBase):
    pass

class TestPerformedResponse(TestPerformedBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
