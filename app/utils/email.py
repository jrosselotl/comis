# app/utils/email.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_project import UserProject

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_email_with_pdf(recipients: list[str], subject: str, body: str, pdf_file: str):
    """
    Sends an email with a PDF attachment to the specified recipients.
    Includes detailed debug logs for troubleshooting.
    """
    print(f"📧 Preparing email to: {recipients}")
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

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.set_debuglevel(1)  # ✅ Activa logs detallados
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
            print(f"✅ Email sent successfully to: {recipients}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        raise


def get_admin_emails(db: Session, project_id: int) -> list[str]:
    """
    Retrieves emails of users with 'admin' or 'project' role for a given project.
    If no admin/project users are found, returns a fallback email.
    """
    admin_users = (
        db.query(User)
        .join(UserProject, User.id == UserProject.user_id)
        .filter(UserProject.project_id == project_id)
        .filter(User.role.in_(["admin", "project"]))  # ✅ Corrected
        .all()
    )
    emails = [u.email for u in admin_users if u.email]
    print(f"📧 Admin/project emails found: {emails}")
    return emails or ["jrosselot@alancx.com"]  # Fallback
