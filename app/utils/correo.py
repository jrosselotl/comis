# app/utils/correo.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def enviar_correo_con_pdf(destinatarios: list[str], asunto: str, cuerpo: str, archivo_pdf: str):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(destinatarios)
    msg.set_content(cuerpo)

    with open(archivo_pdf, "rb") as f:
        contenido_pdf = f.read()
        msg.add_attachment(contenido_pdf, maintype="application", subtype="pdf", filename=os.path.basename(archivo_pdf))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
