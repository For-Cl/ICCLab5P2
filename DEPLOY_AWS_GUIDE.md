# 🚀 Guía de Despliegue en AWS y Docker Hub - Pregunta 2

Esta guía detalla paso a paso cómo publicar la imagen en **Docker Hub** y desplegar la aplicación completa con **Docker Compose** en **Amazon Web Services (AWS EC2)**.

---

## 1. Publicar la Imagen en Docker Hub

En tu máquina local:

```bash
# 1. Iniciar sesión en Docker Hub
docker login

# 2. Definir tu usuario de Docker Hub
export DOCKER_USER="tu_usuario_dockerhub"

# 3. Etiquetar la imagen construida
docker tag marketing-ai-app:latest $DOCKER_USER/marketing-ai-app:latest

# 4. Subir la imagen a Docker Hub
docker push $DOCKER_USER/marketing-ai-app:latest
```

---

## 2. Despliegue en AWS EC2

### Paso 2.1: Lanzar una Instancia EC2
1. Ir a la consola de AWS -> **EC2** -> **Launch Instance**.
2. **Nombre:** `marketing-ai-server`.
3. **AMI:** `Ubuntu 24.04 LTS` o `Amazon Linux 2023`.
4. **Tipo de instancia:** `t2.micro` (Capa gratuita / Free tier).
5. **Key Pair:** Seleccionar o crear un par de llaves `.pem` para conectarse por SSH.
6. **Network Settings (Security Group):**
   - Permitir **SSH** (puerto `22`) desde tu IP.
   - Permitir **HTTP** personalizado (puerto `5000`) desde `0.0.0.0/0` (Anywhere).

---

### Paso 2.2: Conectarse e Instalar Docker en la Instancia

```bash
# Conectarse vía SSH
ssh -i "tu-llave.pem" ubuntu@<IP-PUBLICA-EC2>

# Actualizar el sistema e instalar Docker
sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose-v2

# Habilitar e iniciar Docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```
*(Cierra y vuelve a abrir la sesión SSH para aplicar el grupo `docker` sin requerir `sudo`)*.

---

### Paso 2.3: Desplegar la Aplicación con Docker Compose

En la máquina EC2:

```bash
# 1. Crear directorio del proyecto
mkdir -p ~/marketing-ai && cd ~/marketing-ai

# 2. Crear el archivo docker-compose.yml en el servidor
cat << 'EOF' > docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: marketing-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: marketing_user
      POSTGRES_PASSWORD: marketing_secret_pass
      POSTGRES_DB: marketing_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U marketing_user -d marketing_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    image: tu_usuario_dockerhub/marketing-ai-app:latest
    container_name: marketing-ai-app
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=marketing-ai-production-key-2026
      - DATABASE_URL=postgresql://marketing_user:marketing_secret_pass@db:5432/marketing_db
      - UPLOAD_FOLDER=app/static/uploads
      - GENERATED_FOLDER=app/static/generated
    volumes:
      - uploads_data:/app/app/static/uploads
      - generated_data:/app/app/static/generated
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  uploads_data:
  generated_data:
EOF

# 3. Levantar los contenedores en segundo plano
docker compose up -d

# 4. Verificar el estado
docker compose ps
docker compose logs -f web
```

---

## 3. Acceso y Evidencias para el Informe

Abre tu navegador e ingresa a:
👉 **`http://<IP-PUBLICA-EC2>:5000`**

### Capturas recomendadas para el informe:
1. **Consola AWS EC2:** Mostrando la instancia activa y la IP pública.
2. **Terminal EC2:** Salida de `docker compose ps` con los contenedores `marketing-ai-app` y `marketing-db` en estado `healthy` / `Up`.
3. **Página Principal (Dashboard):** Vista con las campañas creadas.
4. **Paso 1 (Nueva Campaña):** Formulario con carga de foto de la empresa.
5. **Paso 2 (Guiones de IA):** Los 3 guiones propuestos (Profesional, Divertido, Emocional).
6. **Paso 3 (Contenido Generado):** Las 3 imágenes generadas y el video animado.
7. **Paso 4 (Publicación Red Social):** Selección de Instagram / TikTok con la confirmación de despliegue.

---

## 4. Guion para el Video (5 minutos máx.)

| Minuto | Tema | Acción en pantalla |
|--------|------|--------------------|
| 0:00 - 1:00 | **Introducción y Arquitectura** | Mostrar código, Dockerfile, docker-compose.yml con app + PostgreSQL. |
| 1:00 - 2:00 | **Despliegue en AWS** | Mostrar consola AWS EC2, Security Group (puerto 5000) y `docker compose ps`. |
| 2:00 - 3:30 | **Demostración de la App** | Subir foto -> Explicar 3 guiones IA -> Seleccionar uno -> Mostrar 3 fotos + video generados. |
| 3:30 - 4:30 | **Publicación en Red Social** | Publicar en Instagram/TikTok -> Ver persistencia en PostgreSQL y recargar página. |
| 4:30 - 5:00 | **Conclusión** | Resumen de contenedores, volúmenes Docker y cierre. |
