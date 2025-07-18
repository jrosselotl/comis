from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipo import EquipoCreate, EquipoOut
from app.models.equipo import Equipo
from app.database import get_db

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.post("/", response_model=EquipoOut)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db)):
    # ✅ Construimos el código dinámico usando los nombres de las tablas relacionadas
    ubicacion_1 = db.query(Ubicacion).filter_by(id=equipo.ubicacion_1_id).first()
    ubicacion_2 = db.query(Ubicacion).filter_by(id=equipo.ubicacion_2_id).first() if equipo.ubicacion_2_id else None
    tipo_equipo = db.query(TipoEquipo).filter_by(id=equipo.tipo_equipo_id).first()
    sub_equipo = db.query(TipoEquipo).filter_by(id=equipo.sub_equipo_id).first() if equipo.sub_equipo_id else None

    if not ubicacion_1 or not tipo_equipo:
        raise HTTPException(status_code=400, detail="Ubicación o tipo de equipo no válido")

    codigo = f"{ubicacion_1.nombre}{equipo.numero_ubicacion_1}"
    if ubicacion_2:
        codigo += f"-{ubicacion_2.nombre}{equipo.numero_ubicacion_2 or ''}"
    codigo += f"-{tipo_equipo.nombre}{equipo.numero_tipo_equipo}"
    if sub_equipo:
        codigo += f"-{sub_equipo.nombre}{equipo.numero_sub_equipo or ''}"

    nuevo = Equipo(
        proyecto_id=equipo.proyecto_id,
        ubicacion_1_id=equipo.ubicacion_1_id,
        numero_ubicacion_1=equipo.numero_ubicacion_1,
        ubicacion_2_id=equipo.ubicacion_2_id,
        numero_ubicacion_2=equipo.numero_ubicacion_2,
        tipo_equipo_id=equipo.tipo_equipo_id,
        numero_tipo_equipo=equipo.numero_tipo_equipo,
        sub_equipo_id=equipo.sub_equipo_id,
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
