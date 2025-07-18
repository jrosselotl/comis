from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ubicacion import Ubicacion

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

@router.get("/listar")
def listar_ubicaciones(proyecto_id: int, db: Session = Depends(get_db)):
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.project_id == proyecto_id).all()
    return [
        {
            "id": u.id,
            "ubicacion_1": u.ubicacion_1,
            "numero_ubicacion_1": u.numero_ubicacion_1,
            "ubicacion_2": u.ubicacion_2,
            "numero_ubicacion_2": u.numero_ubicacion_2
        } for u in ubicaciones
    ]
