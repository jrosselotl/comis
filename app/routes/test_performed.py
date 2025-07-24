from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db

from app.models.test_performed import TestPerformed
from app.models.equipment import Equipment
from app.models.test import Test
from app.models.test_project import TestProject

# ✅ Result models
from app.models.result_continuity import ResultContinuity
from app.models.result_isolation import ResultIsolation
from app.models.result_contact_resistance import ResultContactResistance
from app.models.result_torque import ResultTorque

router = APIRouter(prefix="/test_performed", tags=["Test Performed"])


# ✅ 1. Crear un test_performed + resultados
@router.post("/create")
def create_test_performed(data: dict, db: Session = Depends(get_db)):
    """
    Crea un nuevo test_performed y sus resultados.
    Espera un JSON:
    {
        "project_id": 1,
        "equipment_id": 10,
        "user_id": 3,
        "test_id": 2,
        "status": "completed",
        "results": [
            {
              "test_point": "L-N",
              "result_value": 0.3,
              "unit": "Ohm",
              "observation": "OK",
              "image_url": "img1.jpg",
              "cable_set": 1
            }
        ]
    }
    """
    try:
        # ✅ Crear test_performed
        new_test = TestPerformed(
            project_id=data["project_id"],
            equipment_id=data["equipment_id"],
            user_id=data["user_id"],
            test_id=data["test_id"],
            status=data.get("status", "incomplete"),
            date=datetime.utcnow()
        )
        db.add(new_test)
        db.flush()  # Obtener ID antes de insertar resultados

        # ✅ Determinar tipo de test
        test_type = db.query(Test).filter(Test.id == data["test_id"]).first().test_type.lower()

        for r in data["results"]:
            if test_type == "continuity":
                db.add(ResultContinuity(test_performed_id=new_test.id, **r))
            elif test_type == "isolation":
                db.add(ResultIsolation(test_performed_id=new_test.id, **r))
            elif test_type == "contact_resistance":
                db.add(ResultContactResistance(test_performed_id=new_test.id, **r))
            elif test_type == "torque":
                db.add(ResultTorque(test_performed_id=new_test.id, **r))

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
                        f"{t.Equipment.location_2}{t.Equipment.number_location_2 or ''}"
                        if t.Equipment.location_2 else None,
                        f"{t.Equipment.equipment_type}{t.Equipment.number_equipment_type or ''}",
                        f"{t.Equipment.sub_equipment}{t.Equipment.number_sub_equipment or ''}"
                        if t.Equipment.sub_equipment else None,
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
