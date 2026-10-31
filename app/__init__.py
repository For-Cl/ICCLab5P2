import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    db_url = os.getenv('DATABASE_URL', 'sqlite:///marketing.db')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    elif db_url.startswith('postgresql://') and not db_url.startswith('postgresql+'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')
    app.config['GENERATED_FOLDER'] = os.getenv('GENERATED_FOLDER', 'app/static/generated')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

    # Crear carpetas necesarias
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)

    # Registrar rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Crear tablas con reintentos para contenedores
    with app.app_context():
        from app import models  # noqa: F401
        import time
        for attempt in range(10):
            try:
                db.create_all()
                break
            except Exception as e:
                if attempt == 9:
                    print(f"Error conectando a la base de datos tras 10 intentos: {e}")
                    raise e
                print(f"Esperando a que la base de datos esté lista (intento {attempt + 1}/10)...")
                time.sleep(2)

    return app
