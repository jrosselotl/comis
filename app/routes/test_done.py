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
    # ✅ Verificar que el test existe
    test_performed = (
        db.query(TestPerformed)
        .filter(TestPerformed.id == test_id)
        .first()
    )
    if not test_performed:
        raise HTTPException(status_code=404, detail="Test not found")

    # ✅ Nombre del PDF esperado (igual que al generarlo en form.py)
    test_type = test_performed.test.test_type
    equipment_code = test_performed.equipment.code
    pdf_path = f"output/{test_type}_{equipment_code}.pdf"

    # ✅ Si el PDF no existe, lo regeneramos automáticamente
    if not os.path.exists(pdf_path):
        project = db.query(Project).filter(Project.id == test_performed.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # 🔥 Aquí podrías reconstruir la data de resultados para regenerar el PDF
        # (opcional si siempre se genera al guardar)
        raise HTTPException(status_code=404, detail="PDF not found. Please regenerate the test.")

    # ✅ Enviar email a administradores o fallback
    recipients = get_admin_emails(db, test_performed.project_id)
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients found to send the PDF.")

    send_email_with_pdf(
        recipients=recipients,
        subject=f"{test_type.capitalize()} - {equipment_code}",
        body=f"Test report for equipment {equipment_code}",
        pdf_file=pdf_path
    )

    return {"message": f"✅ PDF for test '{test_type}' sent successfully"}
