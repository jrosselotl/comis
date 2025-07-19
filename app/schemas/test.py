from pydantic import BaseModel

class TestBase(BaseModel):
    name: str

class TestCreate(TestBase):
    pass

class TestOut(TestBase):
    id: int

    class Config:
        from_attributes = True
