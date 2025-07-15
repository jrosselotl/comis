from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.equipo import Equipo
from app.schemas.test_contact_resistance import (
    TestContactResistanceCreate,
    TestContactResistance as TestContactResistanceSchema
)

router = APIRouter(prefix="/contact_resistance", tags=["Contact Resistance"])

@router.post("/crear", response_model=TestContactResistanceSchema)
def crear_test_contact_resistance(test_data: TestContactResistanceCreate, db: Session = Depends(get_db)):
    # ✅ Verificar que el equipo existe
    equipo = db.query(Equipo).filter_by(id=test_data.equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # ✅ Crear el test
    nuevo_test = TestContactResistance(
        test_id=test_data.test_id,
        proyecto_id=test_data.proyecto_id,
        equipo_id=test_data.equipo_id,
        usuario_id=test_data.usuario_id,
        tipo_alimentacion=test_data.tipo_alimentacion,
        terminal=test_data.terminal,
        fecha=datetime.utcnow()
    )
    db.add(nuevo_test)
    db.commit()
    db.refresh(nuevo_test)

    # ✅ Guardar los resultados asociados
    for resultado in test_data.resultados:
        nuevo_resultado = ResultadoContactResistance(
            test_id=nuevo_test.id,
            cable_set=resultado.cable_set,
            punto_prueba=resultado.punto_prueba,
            referencia_valor=resultado.referencia_valor,
            resultado_valor=resultado.resultado_valor,
            unidad=resultado.unidad,
            aprobado=resultado.aprobado,
            observaciones=resultado.observaciones,
            imagen=resultado.imagen  # (asegúrate que en schemas esté como 'imagen')
        )
        db.add(nuevo_resultado)

    db.commit()
    db.refresh(nuevo_test)
    return nuevo_test


@router.get("/listar")
def listar_tests(db: Session = Depends(get_db)):
    return db.query(TestContactResistance).all()


@router.get("/{test_id}")
def obtener_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestContactResistance).filter(TestContactResistance.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    return test


@router.delete("/{test_id}/eliminar")
def eliminar_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestContactResistance).filter(TestContactResistance.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    db.delete(test)
    db.commit()
    return {"mensaje": "Test eliminado correctamente"}
