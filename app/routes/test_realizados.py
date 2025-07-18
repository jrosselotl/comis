from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_realizados import TestRealizado
from app.models.equipo import Equipo
from app.models.test import Test

router = APIRouter(prefix="/test_realizados", tags=["Test Realizados"])

# ✅ Listar tests realizados por usuario (para "My Tests")
@router.get("/listar_usuario/{usuario_id}")
def listar_tests_usuario(usuario_id: int, db: Session = Depends(get_db)):
    tests = (
        db.query(TestRealizado, Equipo, Test)
        .join(Equipo, TestRealizado.equipo_id == Equipo.id)
        .join(Test, TestRealizado.test_id == Test.id)
        .filter(TestRealizado.usuario_id == usuario_id)
        .all()
    )

    return [
        {
            "id": t.TestRealizado.id,
            "tipo": t.Test.nombre,
            "equipo": t.Equipo.codigo,
            "fecha": t.TestRealizado.fecha.strftime("%Y-%m-%d"),
            "estado": t.TestRealizado.estado
        }
        for t in tests
    ]

# ✅ Cambiar estado a "Enviado" (tras enviar el PDF)
@router.post("/enviar_pdf/{test_id}")
def marcar_como_enviado(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestRealizado).filter(TestRealizado.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")

    test.estado = "Enviado"
    db.commit()
    return {"mensaje": f"Test {test_id} marcado como Enviado"}
