from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.equipo import Equipo
from app.models.proyecto import Proyecto
import shutil, os, json
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/formulario", tags=["Formulario"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/guardar")
async def guardar_formulario(
    proyecto_id: int = Form(...),
    codigo_equipo: str = Form(...),
    tipo: str = Form(...),  # tipo de equipo: PDU, BSW, etc.
    tipo_prueba: str = Form(...),  # continuidad o megado
    cable_sets: int = Form(...),
    datos: str = Form(...),  # JSON: [{punto_prueba, referencia_valor, resultado_valor, tiempo_aplicado, observaciones, aprobado}]
    imagenes: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    try:
        datos_parsed = json.loads(datos)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de datos inválido")

    # 1. Buscar o crear equipo
    equipo = db.query(Equipo).filter_by(codigo=codigo_equipo).first()
    if not equipo:
        equipo = Equipo(
            codigo=codigo_equipo,
            tipo=tipo,
            proyecto_id=proyecto_id
        )
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    # 2. Crear test
    if tipo_prueba == "continuidad":
        test = TestContinuidad(equipo_id=equipo.id, fecha=datetime.utcnow())
    elif tipo_prueba == "megado":
        test = TestMegado(equipo_id=equipo.id, fecha=datetime.utcnow())
    else:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")

    db.add(test)
    db.commit()
    db.refresh(test)

    # 3. Resultados
    for i, resultado in enumerate(datos_parsed):
        imagen_nombre = None
        if i < len(imagenes):
            imagen = imagenes[i]
            if imagen.filename:
                extension = os.path.splitext(imagen.filename)[1]
                imagen_nombre = f"{uuid4().hex}{extension}"
                imagen_path = os.path.join(UPLOAD_DIR, imagen_nombre)
                with open(imagen_path, "wb") as buffer:
                    shutil.copyfileobj(imagen.file, buffer)

        campos_comunes = {
            "test_id": test.id,
            "punto_prueba": resultado.get("punto_prueba"),
            "referencia_valor": resultado.get("referencia_valor"),
            "resultado_valor": resultado.get("resultado_valor"),
            "tiempo_aplicado": resultado.get("tiempo_aplicado"),
            "observaciones": resultado.get("observaciones"),
            "aprobado": resultado.get("aprobado"),
            "imagen_url": imagen_nombre
        }

        if tipo_prueba == "continuidad":
            resultado_obj = ResultadoContinuidad(**campos_comunes)
        else:
            resultado_obj = ResultadoMegado(**campos_comunes)

        db.add(resultado_obj)

    db.commit()
    return {"mensaje": "Formulario y resultados guardados correctamente"}
