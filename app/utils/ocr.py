from PIL import Image
import pytesseract
import io

def extraer_numero_desde_imagen(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, config='--psm 6 digits')
    # Solo números (puedes ajustar esto según el formato esperado)
    return ''.join(filter(lambda x: x.isdigit() or x == '.', text))
