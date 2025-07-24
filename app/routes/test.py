from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test import Test
from app.schemas.test import TestCreate, TestUpdate, TestResponse

router = APIRouter(prefix="/tests", tags=["Tests"])

# ✅ Listar todos los tests
@router.get("/", response_model=List[TestResponse])
def list_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()

# ✅ Crear un test
@router.post("/", response_model=TestResponse)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    existing = db.query(Test).filter(Test.test_type == test.test_type).first()
    if existing:
        raise HTTPException(status_code=400, detail="Test already exists")
    
    new_test = Test(test_type=test.test_type, description=test.description)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

# ✅ Actualizar un test
@router.put("/{test_id}", response_model=TestResponse)
def update_test(test_id: int, test: TestUpdate, db: Session = Depends(get_db)):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    db_test.test_type = test.test_type
    db_test.description = test.description
    db.commit()
    db.refresh(db_test)
    return db_test

# ✅ Eliminar un test
@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")

    db.delete(db_test)
    db.commit()
    return {"message": "Test deleted successfully"}
