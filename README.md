# 🤖 Marketing AI Suite

Aplicación de marketing con inteligencia artificial que permite generar contenido visual y publicarlo en redes sociales.

## 📋 Descripción

El sistema implementa un flujo completo de marketing digital:

1. **📸 Subir Foto** — El usuario sube una foto de su producto/empresa
2. **📝 Generar Guiones** — La IA propone 3 guiones creativos (profesional, divertido, emocional)
3. **🎬 Generar Contenido** — Se selecciona un guion y se generan 3 fotos + 1 video
4. **📱 Publicar** — Se despliega el contenido en Instagram o TikTok (simulado)

## 🛠️ Tecnologías

- **Backend:** Flask + SQLAlchemy
- **Base de datos:** SQLite
- **Generación de imágenes:** Pillow (mock de IA)
- **Frontend:** HTML5 + CSS3 (dark theme premium)
- **Contenedores:** Docker + Docker Compose
- **Producción:** Gunicorn

## 📦 Instalación y Ejecución

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd L5p2

# Construir y ejecutar
docker compose up --build -d

# Acceder a la aplicación
# http://localhost:5000
```

### Opción 2: Ejecución Local

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python wsgi.py
```

## 🐳 Docker

### Construir imagen

```bash
docker build -t marketing-ai-app .
```

### Ejecutar contenedor

```bash
docker run -p 5000:5000 -e SECRET_KEY=mi-clave-secreta marketing-ai-app
```

### Publicar en Docker Hub

```bash
# Login
docker login

# Tag
docker tag marketing-ai-app <TU_USUARIO>/marketing-ai-app:latest

# Push
docker push <TU_USUARIO>/marketing-ai-app:latest
```

## ☁️ Despliegue en AWS

### Opción A: EC2 con Docker

1. Lanzar instancia EC2 (Amazon Linux 2 / Ubuntu)
2. Instalar Docker y Docker Compose
3. Clonar el repositorio
4. Ejecutar `docker compose up -d`
5. Configurar Security Group para abrir puerto 5000

```bash
# En la instancia EC2
sudo yum install docker -y       # Amazon Linux
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clonar y ejecutar
git clone <URL_REPO>
cd L5p2
docker compose up --build -d
```

### Opción B: AWS ECS (Elastic Container Service)

1. Subir imagen a Docker Hub o ECR
2. Crear cluster ECS
3. Definir Task Definition con la imagen
4. Crear servicio con ALB (Application Load Balancer)

## 📁 Estructura del Proyecto

```
L5p2/
├── app/
│   ├── __init__.py          # Factory de la aplicación Flask
│   ├── models.py            # Modelos SQLAlchemy (Campaign, Script, GeneratedContent)
│   ├── routes.py            # Rutas y controladores
│   ├── services.py          # Servicios de IA (mock)
│   ├── static/
│   │   ├── css/style.css    # Estilos premium dark theme
│   │   ├── js/app.js        # JavaScript interactivo
│   │   ├── uploads/         # Fotos subidas por usuarios
│   │   └── generated/       # Contenido generado por IA
│   └── templates/
│       ├── base.html        # Template base
│       ├── index.html       # Dashboard principal
│       ├── new_campaign.html # Formulario nueva campaña
│       └── campaign.html    # Detalle de campaña
├── docker-compose.yml       # Orquestación de contenedores
├── Dockerfile               # Imagen Docker
├── .env                     # Variables de entorno
├── .dockerignore            # Exclusiones de Docker
├── requirements.txt         # Dependencias Python
├── wsgi.py                  # Entry point WSGI
└── README.md                # Esta documentación
```

## 🔧 Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Flask | `dev-secret-key` |
| `DATABASE_URL` | URI de la base de datos | `sqlite:///marketing.db` |
| `UPLOAD_FOLDER` | Carpeta de uploads | `app/static/uploads` |
| `GENERATED_FOLDER` | Carpeta de contenido generado | `app/static/generated` |
| `MAX_CONTENT_LENGTH` | Tamaño máximo de archivo (bytes) | `16777216` (16MB) |

## 📌 Notas

- La generación de IA está **simulada (mock)** para demostración
- En producción, reemplazar `app/services.py` con llamadas a APIs reales (OpenAI DALL-E, Stability AI, etc.)
- Los volúmenes Docker garantizan **persistencia de datos** entre reinicios
