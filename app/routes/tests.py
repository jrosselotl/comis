from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.test import TestCreate, TestOut
from app.models.test import Test
from app.database import get_db

router = APIRouter(prefix="/tests", tags=["Tipos de Test"])

# Crear tipo de test
@router.post("/", response_model=TestOut)
def crear_test(test: TestCreate, db: Session = Depends(get_db)):
    existente = db.query(Test).filter(Test.nombre == test.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un test con ese nombre")
    nuevo = Test(nombre=test.nombre, descripcion=test.descripcion)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Listar todos los tipos de test
@router.get("/", response_model=list[TestOut])
def listar_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()
