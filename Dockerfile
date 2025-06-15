FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo al contenedor (incluye app, static, requirements.txt)
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
