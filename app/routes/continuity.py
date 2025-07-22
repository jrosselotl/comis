from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.form import save_form  # ✅ Usamos la lógica existente de form.py

router = APIRouter(prefix="/form/continuity", tags=["Continuity Form"])

@router.post("/save")
async def save_continuity_bridge(
    project_id: int = Form(...),
    location_1: str = Form(...),
    number_location_1: str = Form(...),
    location_2: str = Form(None),
    number_location_2: str = Form(None),
    equipment_type: str = Form(...),
    number_equipment_type: str = Form(...),
    sub_equipment: str = Form(None),
    number_sub_equipment: str = Form(None),
    test_type: str = Form(...),
    cable_set: int = Form(...),
    power_type: str = Form(...),
    terminal: str = Form(None),
    data: str = Form(...),
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    # ✅ DEBUG: imprime lo recibido para verificar que no venga None o mal tipado
    print("📥 Recibido:", {
        "project_id": project_id,
        "location_1": location_1,
        "number_location_1": number_location_1,
        "location_2": location_2,
        "number_location_2": number_location_2,
        "equipment_type": equipment_type,
        "number_equipment_type": number_equipment_type,
        "sub_equipment": sub_equipment,
        "number_sub_equipment": number_sub_equipment,
        "test_type": test_type,
        "cable_set": cable_set,
        "power_type": power_type,
        "terminal": terminal
    })
    """
    ✅ Este endpoint solo actúa como puente.
    ✅ Llama a la lógica central de `form.py` para no duplicar código.
    ✅ Mantiene la URL `/form/continuity/save` que usa el frontend.
    """
    return await save_form(
        project_id=project_id,
        location_1=location_1,
        number_location_1=number_location_1,
        location_2=location_2,
        number_location_2=number_location_2,
        equipment_type=equipment_type,
        number_equipment_type=number_equipment_type,  # 🔄 Ajuste de nombre que espera form.py
        sub_equipment=sub_equipment,
        sub_equipment_number=number_sub_equipment,
        test_type=test_type,
        cable_set=cable_set,
        power_type=power_type,
        terminal=terminal,
        data=data,
        images=images,
        db=db
    )
