from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.test import TestCreate, TestOut
from app.models.test import Test
from app.database import get_db
from app.utils.unit_conversion import get_units_by_test

router = APIRouter(prefix="/test", tags=["Test Types"])

# ✅ Create test type
@router.post("/", response_model=TestOut)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    existing = db.query(Test).filter(Test.name == test.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="A test with this name already exists")

    new_test = Test(name=test.name, description=test.description)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

# ✅ List all test types
@router.get("/", response_model=list[TestOut])
def list_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()

# ✅ Alias to list (keeps JS compatibility)
@router.get("/list", response_model=list[TestOut])
def alias_list_tests(db: Session = Depends(get_db)):
    return list_tests(db)

# ✅ List valid units by test type
@router.get("/unit")
def list_units(test_type: str = Query(...)):
    return {"units": get_units_by_test(test_type)}
