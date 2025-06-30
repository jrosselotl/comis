from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.equipo import Equipo
from app.models.proyecto import Proyecto
import shutil, os, json
from datetime import datetime
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf

router = APIRouter(prefix="/formulario", tags=["Formulario"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Diccionarios para mapear el tipo de prueba con sus modelos
TEST_MODELS = {
    "continuidad": (TestContinuidad, ResultadoContinuidad),
    "megado": (TestMegado, ResultadoMegado)
    # Agrega aquí más tipos de prueba cuando existan
}

@router.post("/guardar")
async def guardar_formulario(
    proyecto_id: int = Form(...),
    ubicacion_1: str = Form(...),
    numero_ubicacion_1: str = Form(...),
    ubicacion_2: str = Form(None),
    numero_ubicacion_2: str = Form(None),
    tipo_equipo: str = Form(...),
    numero_tipo_equipo: str = Form(...),
    sub_equipo: str = Form(None),
    numero_sub_equipo: str = Form(None),
    tipo_prueba: str = Form(...),
    tipo_alimentacion: str = Form(...),
    cable_sets: int = Form(...),
    datos: str = Form(...),
    imagenes: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    try:
        datos_parsed = json.loads(datos)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de datos inválido")

    if tipo_prueba not in TEST_MODELS:
        raise HTTPException(status_code=400, detail=f"Tipo de prueba no válido: {tipo_prueba}")

    TestModel, ResultadoModel = TEST_MODELS[tipo_prueba]

    proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    partes = [proyecto.nombre, f"{ubicacion_1}{numero_ubicacion_1}"]
    ubicacion_1_completa = f"{ubicacion_1}{numero_ubicacion_1}"

    ubicacion_2_completa = None
    if ubicacion_1 == "COLO" and ubicacion_2 and numero_ubicacion_2:
        ubicacion_2_completa = f"{ubicacion_2}{numero_ubicacion_2}"
        partes.append(ubicacion_2_completa)

    partes.append(f"{tipo_equipo}{numero_tipo_equipo}")
    if sub_equipo and numero_sub_equipo:
        partes.append(f"{sub_equipo}{numero_sub_equipo}")
    codigo_equipo = "-".join(partes)

    equipo = db.query(Equipo).filter_by(codigo=codigo_equipo).first()
    if not equipo:
        equipo = Equipo(
            codigo=codigo_equipo,
            tipo_equipo=tipo_equipo,
            proyecto_id=proyecto_id,
            ubicacion_1=ubicacion_1_completa,
            ubicacion_2=ubicacion_2_completa,
            tipo_alimentacion=tipo_alimentacion,
            cable_set=cable_sets
        )
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    test = TestModel(equipo_id=equipo.id, fecha=datetime.utcnow())
    db.add(test)
    db.commit()
    db.refresh(test)

    imagenes_info = []
    for i, resultado in enumerate(datos_parsed):
        imagen_nombre = None
        imagen_path = None
        if i < len(imagenes):
            imagen = imagenes[i]
            if imagen.filename:
                extension = os.path.splitext(imagen.filename)[1]
                imagen_nombre = f"{codigo_equipo}-{tipo_prueba}-CS{resultado['cable_set']}-{resultado['punto_prueba']}{extension}"
                imagen_path = os.path.join(UPLOAD_DIR, imagen_nombre)
                with open(imagen_path, "wb") as buffer:
                    shutil.copyfileobj(imagen.file, buffer)

        campos_comunes = {
            "test_id": test.id,
            "cable_set": resultado.get("cable_set"),
            "punto_prueba": resultado.get("punto_prueba"),
            "referencia_valor": resultado.get("referencia_valor"),
            "resultado_valor": resultado.get("resultado_valor"),
            "aprobado": resultado.get("aprobado"),
            "observaciones": resultado.get("observaciones"),
            "imagen_url": imagen_nombre,
            "tipo_alimentacion": tipo_alimentacion
        }

        if tipo_prueba == "megado":
            campos_comunes["tiempo_aplicado"] = resultado.get("tiempo_aplicado")

        db.add(ResultadoModel(**campos_comunes))

        if imagen_path:
            imagenes_info.append({
                "nombre": imagen_nombre,
                "punto_prueba": resultado.get("punto_prueba"),
                "resultado": resultado.get("resultado_valor"),
                "ruta": imagen_path,
                "cable_set": resultado.get("cable_set")
            })

    db.commit()

    nombre_equipo = codigo_equipo
    detalles_equipo = {
        "Proyecto": proyecto.nombre,
        "Ubicación Principal": f"{ubicacion_1} Nº{numero_ubicacion_1}",
        "Ubicación Secundaria": f"{ubicacion_2} Nº{numero_ubicacion_2}" if ubicacion_2 else "-",
        "Tipo de Equipo": f"{tipo_equipo} Nº{numero_tipo_equipo}",
        "Subequipo": f"{sub_equipo} Nº{numero_sub_equipo}" if sub_equipo else "-",
        "Tipo de Alimentación": tipo_alimentacion
    }

    test_data = {
        "equipo_id": nombre_equipo,
        "fecha": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "observaciones": "",
        "detalles_equipo": detalles_equipo,
        "imagenes": imagenes_info
    }

    resultados_pdf = [
        {
            "punto_prueba": r["punto_prueba"],
            "referencia_valor": r["referencia_valor"],
            "resultado_valor": r["resultado_valor"],
            "aprobado": r["aprobado"],
            "observaciones": r.get("observaciones", ""),
            "cable_set": r.get("cable_set")
        }
        for r in datos_parsed
    ]

    output_pdf_path = f"output/{tipo_prueba}_{nombre_equipo}.pdf"
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    generar_pdf_test(test_data, resultados_pdf, output_path=output_pdf_path)

    enviar_correo_con_pdf(
        destinatarios=["jrosselot@alancx.com"],
        asunto=f"{tipo_prueba.capitalize()} - {nombre_equipo}",
        cuerpo=f"Informe de {tipo_prueba} para el equipo {nombre_equipo}",
        archivo_pdf=output_pdf_path
    )

    return {"mensaje": "Formulario y resultados guardados correctamente"}
