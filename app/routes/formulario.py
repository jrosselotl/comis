from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad, ResultadoContinuidad
from app.models.test_megado import TestMegado, ResultadoMegado
from app.models.test_contact_resistance import TestContactResistance, ResultadoContactResistance
from app.models.test_torque import TestTorque, ResultadoTorque
from app.models.parametros_continuidad import ParametrosContinuidad
from app.models.equipo import Equipo
from app.models.proyecto import Proyecto
from app.models.usuario import Usuario
from app.models.test import Test
from app.utils.pdf_generator import generar_pdf_test
from app.utils.correo import enviar_correo_con_pdf
from datetime import datetime
import shutil, os, json

router = APIRouter(prefix="/formulario", tags=["Formulario"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

TEST_MODELS = {
    "continuidad": (TestContinuidad, ResultadoContinuidad),
    "megado": (TestMegado, ResultadoMegado),
    "contact_resistance": (TestContactResistance, ResultadoContactResistance),
    "torque": (TestTorque, ResultadoTorque)
}

@router.post("/guardar")
async def guardar_formulario(
    request: Request,
    proyecto_id: int = Form(...),
    ubicacion_1: str = Form(...),
    numero_ubicacion_1: int = Form(...),
    ubicacion_2: str = Form(""),
    numero_ubicacion_2: int = Form(0),
    tipo_equipo: str = Form(...),
    numero_tipo_equipo: int = Form(...),
    sub_equipo: str = Form(""),
    numero_sub_equipo: int = Form(0),
    tipo_prueba: str = Form(...),
    cable_sets: int = Form(...),
    tipo_alimentacion: str = Form(...),
    terminal: str = Form(""),
    datos: str = Form(...),
    imagenes: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        datos_parsed = json.loads(datos)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de datos inválido")

    if tipo_prueba not in TEST_MODELS:
        raise HTTPException(status_code=400, detail=f"Tipo de prueba no válido: {tipo_prueba}")

    TestModel, ResultadoModel = TEST_MODELS[tipo_prueba]

    test_general = db.query(Test).filter_by(nombre=tipo_prueba).first()
    if not test_general:
        raise HTTPException(status_code=400, detail=f"Tipo de prueba '{tipo_prueba}' no existe en la tabla tests")

    proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    partes = [proyecto.nombre, f"{ubicacion_1}{numero_ubicacion_1}"]
    if ubicacion_1 == "COLO" and ubicacion_2 and numero_ubicacion_2:
        partes.append(f"{ubicacion_2}{numero_ubicacion_2}")
    partes.append(f"{tipo_equipo}{numero_tipo_equipo}")
    if sub_equipo and numero_sub_equipo:
        partes.append(f"{sub_equipo}{numero_sub_equipo}")
    codigo_equipo = "-".join(partes)

    equipo = db.query(Equipo).filter_by(codigo=codigo_equipo).first()
    if not equipo:
        equipo = Equipo(
            proyecto_id=proyecto_id,
            ubicacion_1=ubicacion_1,
            numero_ubicacion_1=numero_ubicacion_1,
            ubicacion_2=ubicacion_2 if ubicacion_2 else None,
            numero_ubicacion_2=numero_ubicacion_2 if numero_ubicacion_2 else None,
            tipo_equipo=tipo_equipo,
            numero_tipo_equipo=numero_tipo_equipo,
            sub_equipo=sub_equipo if sub_equipo else None,
            numero_sub_equipo=numero_sub_equipo if numero_sub_equipo else None,
            terminal=terminal,
            tipo_alimentacion=tipo_alimentacion,
            cable_set=cable_sets,
            codigo=codigo_equipo
        )
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    test = TestModel(
        equipo_id=equipo.id,
        usuario_id=usuario_id,
        proyecto_id=proyecto_id,
        fecha=datetime.utcnow()
    )
    db.add(test)
    db.commit()
    db.refresh(test)

    # Cargar parámetros técnicos desde DB
    parametros = {}
    if tipo_prueba == "continuidad":
        parametros = {
            (p.codigo_equipo, p.proyecto_id): (p.referencia, p.logica)
            for p in db.query(ParametrosContinuidad).filter_by(proyecto_id=proyecto_id, codigo_equipo=codigo_equipo)
        }

    imagenes_info = []

    for i, resultado in enumerate(datos_parsed):
        imagen_nombre = None
        imagen_path = None
        resultado_valor = resultado.get("resultado_valor")

        if i < len(imagenes) and imagenes[i].filename:
            imagen = imagenes[i]
            extension = os.path.splitext(imagen.filename)[1]
            imagen_nombre = f"{codigo_equipo}-{tipo_prueba}-CS{resultado['cable_set']}-{resultado['punto_prueba']}{extension}"
            imagen_path = os.path.join(UPLOAD_DIR, imagen_nombre)
            with open(imagen_path, "wb") as buffer:
                contenido = await imagen.read()
                buffer.write(contenido)

        # Evaluación automática de aprobado
        aprobado = None
        if resultado_valor == "N/A":
            aprobado = True
            resultado_valor_db = None
        else:
            try:
                resultado_valor_db = float(resultado_valor)
            except:
                resultado_valor_db = None

            referencia, logica = parametros.get((codigo_equipo, proyecto_id), (None, None))

            if referencia is not None and resultado_valor_db is not None:
                if logica == "=":
                    aprobado = resultado_valor_db == referencia
                elif logica == "<":
                    aprobado = resultado_valor_db < referencia
                elif logica == ">":
                    aprobado = resultado_valor_db > referencia
                elif logica == "<=":
                    aprobado = resultado_valor_db <= referencia
                elif logica == ">=":
                    aprobado = resultado_valor_db >= referencia
                else:
                    aprobado = None

        campos_comunes = {
            "test_id": test.id,
            "cable_set": resultado.get("cable_set"),
            "punto_prueba": resultado.get("punto_prueba"),
            "resultado_valor": resultado_valor_db,
            "aprobado": aprobado,
            "observaciones": resultado.get("observaciones"),
            "imagen_url": imagen_nombre,
            "tipo_alimentacion": tipo_alimentacion,
        }

        db.add(ResultadoModel(**campos_comunes))

        if imagen_path:
            imagenes_info.append({
                "nombre": imagen_nombre,
                "punto_prueba": resultado.get("punto_prueba"),
                "resultado": resultado_valor,
                "ruta": imagen_path,
                "cable_set": resultado.get("cable_set")
            })

    db.commit()

    # Generación del PDF
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
            "referencia_valor": referencia,
            "resultado_valor": r["resultado_valor"],
            "aprobado": aprobado,
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
