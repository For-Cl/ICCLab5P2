FROM python:3.12-slim

# Instalar fuentes para la generación de imágenes y herramientas útiles
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios para almacenamiento persistente
RUN mkdir -p app/static/uploads app/static/generated instance

# Variables de entorno por defecto
ENV FLASK_ENV=production
ENV SECRET_KEY=change-me-in-production
ENV DATABASE_URL=sqlite:///instance/marketing.db
ENV UPLOAD_FOLDER=app/static/uploads
ENV GENERATED_FOLDER=app/static/generated

EXPOSE 5000

# Servidor de producción gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:app"]
