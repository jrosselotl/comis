from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_torque import TestTorque, ResultadoTorque
from app.schemas.test_torque import TestTorqueCreate, TestTorque

router = APIRouter(prefix="/test/torque", tags=["Test Torque"])

@router.post("/crear", response_model=TestTorque)
def crear_test_torque(test_data: TestTorqueCreate, db: Session = Depends(get_db)):
    test = TestTorque(
        proyecto_id=test_data.proyecto_id,
        equipo_id=test_data.equipo_id,
        usuario_id=test_data.usuario_id
    )
    db.add(test)
    db.commit()
    db.refresh(test)

    for resultado_data in test_data.resultados:
        resultado = ResultadoTorque(**resultado_data.dict(), test_id=test.id)
        db.add(resultado)

    db.commit()
    db.refresh(test)
    return test


@router.get("/{test_id}", response_model=TestTorque)
def obtener_test_torque(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestTorque).filter(TestTorque.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test de torque no encontrado")
    return test
