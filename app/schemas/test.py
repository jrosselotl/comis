from pydantic import BaseModel
from typing import Optional

class TestBase(BaseModel):
    test_type: str
    description: Optional[str] = None

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    pass

class TestResponse(TestBase):
    id: int

    class Config:
        orm_mode = True
