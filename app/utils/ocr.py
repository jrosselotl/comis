import easyocr
from PIL import Image
import io
import os

# Inicializa el lector de OCR (puedes activar GPU si tu entorno lo permite)
reader = easyocr.Reader(['en', 'es'], gpu=False)

def extraer_texto_desde_imagen(image_bytes: bytes) -> str:
    # Convertir los bytes a imagen y guardarla temporalmente
    image = Image.open(io.BytesIO(image_bytes))
    temp_path = "temp_ocr.jpg"
    image.save(temp_path)

    # Leer texto con EasyOCR
    results = reader.readtext(temp_path)

    # Borrar la imagen temporal si fue creada
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not results:
        return ""

    # Extraer el texto con mayor nivel de confianza
    texto_confianza = sorted(results, key=lambda r: r[2], reverse=True)[0][1]

    return texto_confianza.strip()
