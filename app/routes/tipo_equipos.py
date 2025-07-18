from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tipo_equipo import TipoEquipo  # Modelo que vamos a crear

router = APIRouter(prefix="/tipo_equipos", tags=["Tipos de Equipos"])

@router.get("/listar")
def listar_tipo_equipos(db: Session = Depends(get_db)):
    equipos = db.query(TipoEquipo).all()
    return [
        {
            "tipo_equipo": e.tipo_equipo,
            "numero_tipo_equipo": e.numero_tipo_equipo,  # ARRAY en BD
            "sub_equipo": e.sub_equipo,
            "numero_sub_equipo": e.numero_sub_equipo,    # ARRAY en BD
        }
        for e in equipos
    ]
