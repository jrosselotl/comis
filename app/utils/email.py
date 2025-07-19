# app/utils/email.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project_user import ProjectUser

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_email_with_pdf(recipients: list[str], subject: str, body: str, pdf_file: str):
    """
    Sends an email with a PDF attachment to the specified recipients.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    with open(pdf_file, "rb") as f:
        pdf_content = f.read()
        msg.add_attachment(
            pdf_content,
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_file)
        )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def get_admin_emails(db: Session, project_id: int) -> list[str]:
    """
    Retrieves emails of users with 'admin' or 'project' role for a given project.
    If no admin/project users are found, returns a fallback email.
    """
    admin_users = (
        db.query(User)
        .join(ProjectUser, User.id == ProjectUser.user_id)
        .filter(UProjectUser.project_id == project_id)
        .filter(User.rol.in_(["admin", "project"]))
        .all()
    )
    email = [u.email for u in admin_users]
    return email or ["jrosselot@alancx.com"]  # Fallback
