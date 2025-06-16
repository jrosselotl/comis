# app/routes/formulario.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad
from app.models.resultado_continuidad import ResultadoContinuidad
from app.models.test_megado import TestMegado
from app.models.resultado_megado import ResultadoMegado
import shutil, os, json
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/formulario", tags=["Formulario"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/guardar")
async def guardar_formulario(
    equipo_id: int = Form(...),
    tipo_prueba: str = Form(...),  # "continuidad" o "megado"
    cable_sets: int = Form(...),
    datos: str = Form(...),  # JSON con estructura [{cable_set, punto_prueba, referencia_valor, resultado_valor, aprobado}]
    imagenes: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    try:
        datos_parsed = json.loads(datos)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de datos inválido")

    # 1. Guardar el test
    if tipo_prueba == "continuidad":
        test = TestContinuidad(equipo_id=equipo_id, fecha=datetime.utcnow())
        db.add(test)
        db.commit()
        db.refresh(test)
    elif tipo_prueba == "megado":
        test = TestMegado(equipo_id=equipo_id, fecha=datetime.utcnow())
        db.add(test)
        db.commit()
        db.refresh(test)
    else:
        raise HTTPException(status_code=400, detail="Tipo de prueba no válido")

    # 2. Guardar resultados
    for i, resultado in enumerate(datos_parsed):
        imagen_nombre = None
        if i < len(imagenes):
            imagen = imagenes[i]
            extension = os.path.splitext(imagen.filename)[1]
            imagen_nombre = f"{uuid4().hex}{extension}"
            imagen_path = os.path.join(UPLOAD_DIR, imagen_nombre)
            with open(imagen_path, "wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)

        if tipo_prueba == "continuidad":
            resultado_obj = ResultadoContinuidad(
                test_id=test.id,
                punto_prueba=resultado.get("punto_prueba"),
                referencia_valor=resultado.get("referencia_valor"),
                resultado_valor=resultado.get("resultado_valor"),
                aprobado=resultado.get("aprobado"),
                imagen_url=imagen_nombre
            )
        else:
            resultado_obj = ResultadoMegado(
                test_id=test.id,
                punto_prueba=resultado.get("punto_prueba"),
                referencia_valor=resultado.get("referencia_valor"),
                resultado_valor=resultado.get("resultado_valor"),
                aprobado=resultado.get("aprobado"),
                imagen_url=imagen_nombre
            )

        db.add(resultado_obj)

    db.commit()
    return {"mensaje": "Formulario y resultados guardados correctamente"}
