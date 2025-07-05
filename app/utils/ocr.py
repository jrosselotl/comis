from functools import lru_cache
import easyocr
from PIL import Image
import io
import re

# Usa lru_cache para cargar el modelo solo una vez
@lru_cache(maxsize=1)
def get_reader():
    return easyocr.Reader(['en', 'es'], gpu=False)

def extraer_texto_desde_imagen(image_bytes: bytes) -> str:
    """
    Extrae el texto más probable desde una imagen usando EasyOCR
    y retorna el número más confiable (permitiendo unidades como Ω, kV, etc).
    """
    image = Image.open(io.BytesIO(image_bytes))
    results = get_reader().readtext(image)

    if not results:
        return ""

    mejores = sorted(results, key=lambda r: r[2], reverse=True)

    for _, texto, _ in mejores:
        texto = texto.strip()
        match = re.search(r"[\d]+(?:[.,]\d+)?\s?(?:kV|KV|Ω|ohm|MΩ|GΩ|V|mA|A)?", texto)
        if match:
            return match.group(0).replace(",", ".")  # coma decimal por punto

    return mejores[0][1]  # fallback
