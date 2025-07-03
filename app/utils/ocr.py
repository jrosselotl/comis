import easyocr
from PIL import Image
import io
import os
import re

# Inicializa el lector OCR (sin GPU por compatibilidad con Render)
reader = easyocr.Reader(['en', 'es'], gpu=False)

def extraer_texto_desde_imagen(image_bytes: bytes) -> str:
    """
    Extrae el texto más probable desde una imagen usando EasyOCR
    y retorna solo el número más confiable (permitiendo unidades como Ω, kV, etc).
    """
    # Convertimos los bytes en imagen temporal
    image = Image.open(io.BytesIO(image_bytes))
    temp_path = "temp_ocr.jpg"
    image.save(temp_path)

    try:
        # Leer con OCR
        results = reader.readtext(temp_path)
        if not results:
            return ""

        # Buscar número más confiable entre los textos detectados
        mejores = sorted(results, key=lambda r: r[2], reverse=True)

        for _, texto, _ in mejores:
            texto = texto.strip()
            # Buscar números con posible decimal y unidad
            match = re.search(r"[\d]+(?:[\.,]\d+)?\s?(?:kV|KV|Ω|ohm|MΩ|GΩ|V|mA|A)?", texto)
            if match:
                return match.group(0).replace(",", ".")  # Reemplazar coma decimal por punto

        return mejores[0][1]  # Si no se encontró patrón numérico, devolvemos el mejor texto crudo

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
