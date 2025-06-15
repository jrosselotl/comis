from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipo import EquipoCreate, EquipoOut
from app.models.equipo import Equipo
from app.database import get_db

router = APIRouter(prefix="/equipos", tags=["Equipos"])

# Crear un equipo
@router.post("/", response_model=EquipoOut)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    nuevo = Equipo(
        proyecto_id=equipo.proyecto_id,
        codigo_equipo=equipo.codigo_equipo,
        tipo=equipo.tipo,
        descripcion=equipo.descripcion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Obtener todos los equipos
@router.get("/", response_model=list[EquipoOut])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(Equipo).all()
