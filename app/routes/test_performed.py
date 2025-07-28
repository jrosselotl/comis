from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
import shutil, os, json

from app.database import get_db
from app.models.test_performed import TestPerformed
from app.models.equipment import Equipment
from app.models.test import Test
from app.models.test_project import TestProject

# ✅ Result models
from app.models.result_continuity import ResultContinuity
from app.models.result_insulation import ResultInsulation
from app.models.result_contact_resistance import ResultContactResistance
from app.models.result_torque import ResultTorque

router = APIRouter(prefix="/test_performed", tags=["Test Performed"])

# ✅ Carpeta para guardar imágenes
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ 1. Crear un test_performed + resultados + imágenes
@router.post("/create")
async def create_test_performed(request: Request, db: Session = Depends(get_db)):
    """
    Recibe FormData:
    - project_id, equipment_id, user_id, test_id, status
    - results (JSON string)
    - Imágenes con nombre image_${i}_${point}
    """
    form = await request.form()
    try:
        project_id = int(form["project_id"])
        equipment_id = int(form["equipment_id"])
        user_id = int(form["user_id"])
        test_id = int(form["test_id"])
        status = form.get("status", "incomplete")

        # ✅ Crear test_performed
        new_test = TestPerformed(
            project_id=project_id,
            equipment_id=equipment_id,
            user_id=user_id,
            test_id=test_id,
            status=status,
            date=datetime.utcnow()
        )
        db.add(new_test)
        db.flush()

        # ✅ Procesar resultados
        results = json.loads(form["results"])
        test_type = db.query(Test).filter(Test.id == test_id).first().test_type.lower()

        for r in results:
            image_field = r.get("image_field")
            image_file = form.get(image_field)
            image_path = None

            if image_file and hasattr(image_file, "filename") and image_file.filename:
                filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image_file.filename}"
                file_location = os.path.join(UPLOAD_DIR, filename)
                with open(file_location, "wb") as f:
                    shutil.copyfileobj(image_file.file, f)
                image_path = f"/{file_location}"

            # ✅ Datos comunes
            common_data = {
                "test_performed_id": new_test.id,
                "test_point": r["test_point"],
                "observation": r.get("observation"),
                "cable_set": r.get("cable_set"),
                "image_url": image_path,
                "unit": r.get("unit")
            }

            # ✅ Guardar según el tipo de test
            if test_type == "continuity":
                db.add(ResultContinuity(
                    **common_data,
                    result_value=r.get("result_value")
                ))

            elif test_type == "insulation":
                db.add(ResultInsulation(
                    **common_data,
                    result_value=r.get("result_value"),
                    time_applied=r.get("time_applied")
                ))

            elif test_type == "contact_resistance":
                db.add(ResultContactResistance(
                    **common_data,
                    result_value=r.get("result_value")
                ))

            elif test_type == "torque":
                db.add(ResultTorque(
                    **common_data,
                    nominal_value=r.get("nominal_value"),
                    verification_value=r.get("verification_value")
                ))

        db.commit()
        return {"message": f"✅ Test created successfully with ID {new_test.id}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Error creating test: {str(e)}")


# ✅ 2. List tests performed by user (for "My Tests")
@router.get("/list_user/{user_id}")
def list_user_tests(user_id: int, db: Session = Depends(get_db)):
    tests = (
        db.query(TestPerformed, Equipment, Test)
        .join(Equipment, TestPerformed.equipment_id == Equipment.id)
        .join(Test, TestPerformed.test_id == Test.id)
        .filter(TestPerformed.user_id == user_id)
        .order_by(TestPerformed.date.desc())
        .all()
    )

    return [
        {
            "id": t.TestPerformed.id,
            "test_type": t.Test.test_type,
            "asset": "-".join(
                filter(
                    None,
                    [
                        f"{t.Equipment.location_1}{t.Equipment.number_location_1 or ''}",
                        f"{t.Equipment.location_2}{t.Equipment.number_location_2 or ''}" if t.Equipment.location_2 else None,
                        f"{t.Equipment.equipment_type}{t.Equipment.number_equipment_type or ''}",
                        f"{t.Equipment.sub_equipment}{t.Equipment.number_sub_equipment or ''}" if t.Equipment.sub_equipment else None,
                    ],
                )
            ),
            "date": t.TestPerformed.date.strftime("%Y-%m-%d"),
            "status": t.TestPerformed.status,
        }
        for t in tests
    ]


# ✅ 3. Stats for Dashboard (for current user and project)
@router.get("/list_user_stats/{user_id}")
def list_user_stats(user_id: int, project_id: int = 1, db: Session = Depends(get_db)):
    """
    Devuelve {test_type: cantidad_realizada_por_usuario} solo para tests asignados al proyecto.
    """
    assigned_tests = (
        db.query(Test)
        .join(TestProject, TestProject.test_id == Test.id)
        .filter(TestProject.project_id == project_id, TestProject.active == True)
        .all()
    )

    if not assigned_tests:
        raise HTTPException(status_code=404, detail="No hay tests asignados a este proyecto")

    results = {}
    for test in assigned_tests:
        total = (
            db.query(TestPerformed)
            .filter(
                TestPerformed.test_id == test.id,
                TestPerformed.project_id == project_id,
                TestPerformed.user_id == user_id
            )
            .count()
        )
        results[test.test_type] = total

    return results


# ✅ 4. Change status to "Sent" (after sending the PDF)
@router.post("/mark_sent/{test_id}")
def mark_test_as_sent(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestPerformed).filter(TestPerformed.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test.status = "sent"
    db.commit()
    return {"message": f"✅ Test {test_id} marked as Sent"}
