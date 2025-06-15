from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.test_continuidad import TestContinuidadCreate, TestContinuidadOut
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.equipo import Equipo
from app.models.proyecto import Proyecto
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf

router = APIRouter(prefix="/continuidad", tags=["Test de Continuidad"])

# Crear nuevo test de continuidad
@router.post("/", response_model=TestContinuidadOut)
def crear_test_continuidad(data: TestContinuidadCreate, db: Session = Depends(get_db)):
    nuevo_test = TestContinuidad(
        equipo_id=data.equipo_id,
        usuario_id=data.usuario_id,
        observaciones=data.observaciones
    )
    db.add(nuevo_test)
    db.commit()
    db.refresh(nuevo_test)

    for resultado in data.resultados:
        r = ResultadoContinuidad(
            test_id=nuevo_test.id,
            punto_prueba=resultado.punto_prueba,
            referencia_valor=resultado.referencia_valor,
            resultado_valor=resultado.resultado_valor,
            aprobado=resultado.aprobado,
            imagen_url=resultado.imagen_url
        )
        db.add(r)

    db.commit()
    return nuevo_test

# Listar todos los tests
@router.get("/{test_id}/pdf")
def generar_pdf_test_continuidad(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestContinuidad).filter(TestContinuidad.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")

    resultados = db.query(ResultadoContinuidad).filter(ResultadoContinuidad.test_id == test_id).all()

    test_data = {
        "equipo_id": test.equipo_id,
        "usuario_id": test.usuario_id,
        "observaciones": test.observaciones,
        "fecha": test.created_at.strftime("%Y-%m-%d %H:%M:%S") if test.created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    resultados_data = [{
        "punto_prueba": r.punto_prueba,
        "referencia_valor": r.referencia_valor,
        "resultado_valor": r.resultado_valor,
        "aprobado": r.aprobado,
        "imagen_url": r.imagen_url
    } for r in resultados]

    pdf_path = generar_informe_test(
        test_type="CONTINUIDAD",
        test_data=test_data,
        resultados=resultados_data
    )

    equipo = db.query(Equipo).filter(Equipo.id == test.equipo_id).first()
    proyecto = db.query(Proyecto).filter(Proyecto.id == equipo.proyecto_id).first()

    usuarios = db.execute(
        """SELECT u.correo FROM usuarios u
           JOIN usuarios_proyectos up ON u.id = up.usuario_id
           WHERE up.proyecto_id = :proyecto_id""",
        {"proyecto_id": proyecto.id}
    ).fetchall()

    destinatarios = [u[0] for u in usuarios]

    if not destinatarios:
        raise HTTPException(status_code=400, detail="No hay usuarios asignados al proyecto para enviar el correo.")

    asunto = f"Informe de Test de Continuidad - Equipo {test.equipo_id}"
    cuerpo = f"Adjunto se encuentra el informe en PDF del test de continuidad realizado el {test_data['fecha']}."
    enviar_correo_con_pdf(destinatarios, asunto, cuerpo, pdf_path)

    return FileResponse(pdf_path)