from pydantic import BaseModel
from typing import Optional

class TestProjectBase(BaseModel):
    project_id: int
    test_id: int
    active: Optional[bool] = True

class TestProjectCreate(TestProjectBase):
    pass

class TestProjectUpdate(BaseModel):
    active: bool

class TestProjectResponse(TestProjectBase):
    id: int

    class Config:
        orm_mode = True
