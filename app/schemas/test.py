from pydantic import BaseModel

class TestBase(BaseModel):
    nombre: str

class TestCreate(TestBase):
    pass

class TestOut(TestBase):
    id: int

    class Config:
        orm_mode = True
