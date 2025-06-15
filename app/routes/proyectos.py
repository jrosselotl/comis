from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.proyecto import ProyectoCreate, ProyectoOut
from app.models.proyecto import Proyecto
from app.database import get_db

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

# Crear nuevo proyecto
@router.post("/", response_model=ProyectoOut)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    nuevo = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Obtener todos los proyectos
@router.get("/", response_model=list[ProyectoOut])
def listar_proyectos(db: Session = Depends(get_db)):
    return db.query(Proyecto).all()
