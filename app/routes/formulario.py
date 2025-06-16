# app/routes/formulario.py
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_continuidad import TestContinuidad
from app.models.resultado_continuidad import ResultadoContinuidad
import shutil, os
from datetime import datetime

router = APIRouter(prefix="/formulario", tags=["Formulario"])

@router.post("/guardar")
async def guardar_formulario(
    equipo_id: int = Form(...),
    tipo_prueba: str = Form(...),
    cable_sets: int = Form(...),
    datos: str = Form(...),  # JSON con los resultados
    imagenes: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    # Lógica para guardar Test y Resultados
    # Aquí parsearías `datos` como JSON y recorrerías para crear los registros

    return {"mensaje": "Formulario guardado correctamente"}
