FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/backend
RUN python manage.py collectstatic --noinput || true

# ESTO ES LO QUE TE FALTABA - crea la carpeta de fotos y le da permiso
RUN mkdir -p /app/backend/media/portadas_libros /app/backend/staticfiles && chmod -R 777 /app/backend/media /app/backend/staticfiles

EXPOSE 8000
CMD sh -c "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"