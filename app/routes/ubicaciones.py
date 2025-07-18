from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ubicacion import Ubicacion  # Modelo que vamos a crear

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

@router.get("/listar")
def listar_ubicaciones(proyecto_id: int = Query(...), db: Session = Depends(get_db)):
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.proyecto_id == proyecto_id).all()
    return [
        {
            "ubicacion_1": u.ubicacion_1,
            "numero_ubicacion_1": u.numero_ubicacion_1,  # ARRAY en BD
            "ubicacion_2": u.ubicacion_2,
            "numero_ubicacion_2": u.numero_ubicacion_2,  # ARRAY en BD
        }
        for u in ubicaciones
    ]
