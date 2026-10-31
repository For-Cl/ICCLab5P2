from datetime import datetime
from app import db


class Campaign(db.Model):
    """Campaña de marketing: contiene la foto original y los guiones generados."""
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    original_photo = db.Column(db.String(500), nullable=False)  # ruta a la foto subida
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    scripts = db.relationship('Script', backref='campaign', lazy=True, cascade='all, delete-orphan')
    generated_content = db.relationship('GeneratedContent', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Campaign {self.id} - {self.company_name}>'


class Script(db.Model):
    """Guion propuesto por la IA para una campaña."""
    __tablename__ = 'scripts'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tone = db.Column(db.String(100), nullable=False)  # profesional, divertido, emocional
    is_selected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Script {self.id} - {self.title}>'


class GeneratedContent(db.Model):
    """Contenido generado (fotos y video) basado en el guion seleccionado."""
    __tablename__ = 'generated_content'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'photo' o 'video'
    file_path = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    published = db.Column(db.Boolean, default=False)
    published_platform = db.Column(db.String(50), nullable=True)  # 'instagram' o 'tiktok'
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    script = db.relationship('Script', backref='generated_items')

    def __repr__(self):
        return f'<GeneratedContent {self.id} - {self.content_type}>'
