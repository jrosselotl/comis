from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.equipo import Equipo
from app.schemas.test_contact_resistance import TestContactResistanceCreate, TestContactResistance
from datetime import datetime

router = APIRouter(prefix="/contact_resistance", tags=["Contact Resistance"])

@router.post("/crear", response_model=TestContactResistance)
def crear_test_contact_resistance(test_data: TestContactResistanceCreate, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter_by(id=test_data.equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    nuevo_test = TestContactResistance(
        proyecto_id=test_data.proyecto_id,
        equipo_id=test_data.equipo_id,
        usuario_id=test_data.usuario_id,
        fecha=datetime.utcnow()
    )
    db.add(nuevo_test)
    db.commit()
    db.refresh(nuevo_test)

    for resultado in test_data.resultados:
        nuevo_resultado = ResultadoContactResistance(
            test_id=nuevo_test.id,
            cable_set=resultado.cable_set,
            punto_prueba=resultado.punto_prueba,
            referencia_valor=resultado.referencia_valor,
            resultado_valor=resultado.resultado_valor,
            aprobado=resultado.aprobado,
            observaciones=resultado.observaciones,
            imagen_url=resultado.imagen_url,
            tipo_alimentacion=resultado.tipo_alimentacion,
            unidad=resultado.unidad
        )
        db.add(nuevo_resultado)

    db.commit()
    db.refresh(nuevo_test)
    return nuevo_test
