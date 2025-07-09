from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipo import EquipoCreate, EquipoOut
from app.models.equipo import Equipo
from app.database import get_db

router = APIRouter(prefix="/equipos", tags=["Equipos"])

@router.post("/", response_model=EquipoOut)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    codigo = f"{equipo.ubicacion_1}{equipo.numero_ubicacion_1}"
    if equipo.ubicacion_2:
        codigo += f"-{equipo.ubicacion_2}{equipo.numero_ubicacion_2}"
    codigo += f"-{equipo.tipo}{equipo.numero_tipo_equipo}"
    if equipo.sub_equipo:
        codigo += f"-{equipo.sub_equipo}{equipo.numero_sub_equipo or ''}"

    nuevo = Equipo(
        proyecto_id=equipo.proyecto_id,
        ubicacion_1=equipo.ubicacion_1,
        numero_ubicacion_1=equipo.numero_ubicacion_1,
        ubicacion_2=equipo.ubicacion_2,
        numero_ubicacion_2=equipo.numero_ubicacion_2,
        tipo_equipo=equipo.tipo,
        numero_tipo_equipo=equipo.numero_tipo_equipo,
        sub_equipo=equipo.sub_equipo,
        numero_sub_equipo=equipo.numero_sub_equipo,
        terminal=equipo.terminal,
        tipo_alimentacion=equipo.tipo_alimentacion,
        cable_set=equipo.cable_set,
        codigo=codigo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[EquipoOut])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(Equipo).all()
