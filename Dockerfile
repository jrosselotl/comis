FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY ./app /app/app
COPY ./static /app/static
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
