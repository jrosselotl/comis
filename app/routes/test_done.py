# app/routes/test_done.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_performed import TestPerformed
from app.models.project import Project
from app.utils.pdf_generator import generate_test_pdf
from app.utils.email import send_email_with_pdf, get_admin_emails
import os

router = APIRouter(prefix="/test_done", tags=["Test Done"])

@router.post("/send_pdf/{test_id}")
async def send_pdf(test_id: int, db: Session = Depends(get_db)):
    test_performed = db.query(TestPerformed).filter(TestPerformed.id == test_id).first()
    if not test_performed:
        raise HTTPException(status_code=404, detail="Test not found")

    # ✅ Nombre del PDF esperado
    pdf_path = f"output/{test_performed.test.test_type}_{test_performed.equipment.code}.pdf"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found. Please generate it first.")

    emails = get_admin_emails(db, test_performed.project_id)
    send_email_with_pdf(
        recipients=emails,
        subject=f"{test_performed.test.test_type.capitalize()} - {test_performed.equipment.code}",
        body=f"Test report for {test_performed.equipment.code}",
        pdf_file=pdf_path
    )

    return {"message": "✅ PDF sent successfully"}
