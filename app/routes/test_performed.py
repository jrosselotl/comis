from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_performed import TestPerformed
from app.models.equipment import Equipment
from app.models.test import Test

router = APIRouter(prefix="/test_performed", tags=["Test Performed"])

# ✅ List tests performed by user (for "My Tests")
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
            "test_type": t.Test.name,
            # ✅ Asset completo concatenado (COLO1-CE1-PDU1-BSW1)
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


# ✅ Change status to "Sent" (after sending the PDF)
@router.post("/mark_sent/{test_id}")
def mark_test_as_sent(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestPerformed).filter(TestPerformed.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test.status = "Sent"
    db.commit()
    return {"message": f"Test {test_id} marked as Sent"}
