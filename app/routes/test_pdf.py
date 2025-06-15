from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import smtplib
from email.message import EmailMessage

router = APIRouter()

@router.post("/enviar-pdf")
async def enviar_pdf_correo(
    email: str = Form(...),
    archivo: UploadFile = File(...)
):
    try:
        # Leer el archivo subido
        contenido_pdf = await archivo.read()

        # Crear mensaje de correo
        mensaje = EmailMessage()
        mensaje["Subject"] = "📎 PDF desde el formulario"
        mensaje["From"] = "contacto@simocore.com"
        mensaje["To"] = email
        mensaje.set_content("Adjunto el archivo enviado desde el formulario.")

        # Adjuntar PDF
        mensaje.add_attachment(
            contenido_pdf,
            maintype="application",
            subtype="pdf",
            filename=archivo.filename
        )

        # Enviar usando SMTP SSL
        with smtplib.SMTP_SSL("mail.simocore.com", 465) as smtp:
            smtp.login("contacto@simocore.com", "esb?@60PyLD}Nrk4")  # ⚠️ asegúrate de que las credenciales son correctas
            smtp.send_message(mensaje)

        return JSONResponse(status_code=200, content={"mensaje": "📧 Correo enviado con éxito"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
