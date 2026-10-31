import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models import Campaign, Script, GeneratedContent
from app.services import generate_scripts, generate_photos, generate_video, simulate_publish

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Página principal ────────────────────────────────────────────
@main_bp.route('/')
def index():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('index.html', campaigns=campaigns)


# ─── Paso 1: Subir foto y crear campaña ─────────────────────────
@main_bp.route('/campaign/new', methods=['GET', 'POST'])
def new_campaign():
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        description = request.form.get('description', '').strip()
        file = request.files.get('photo')

        if not company_name:
            flash('El nombre de la empresa es obligatorio.', 'error')
            return redirect(url_for('main.new_campaign'))

        if not file or file.filename == '':
            flash('Debes subir una foto.', 'error')
            return redirect(url_for('main.new_campaign'))

        if not allowed_file(file.filename):
            flash('Formato de archivo no permitido. Usa: PNG, JPG, GIF o WebP.', 'error')
            return redirect(url_for('main.new_campaign'))

        # Guardar foto
        filename = secure_filename(file.filename)
        unique_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)

        # Crear campaña
        campaign = Campaign(
            company_name=company_name,
            description=description,
            original_photo=unique_name
        )
        db.session.add(campaign)
        db.session.commit()

        # Generar 3 guiones con IA
        scripts_data = generate_scripts(company_name)
        for s in scripts_data:
            script = Script(
                campaign_id=campaign.id,
                title=s['title'],
                content=s['content'],
                tone=s['tone']
            )
            db.session.add(script)
        db.session.commit()

        flash(f'✅ Campaña creada para "{company_name}". Se generaron 3 guiones.', 'success')
        return redirect(url_for('main.view_campaign', campaign_id=campaign.id))

    return render_template('new_campaign.html')


# ─── Paso 2: Ver campaña y seleccionar guion ────────────────────
@main_bp.route('/campaign/<int:campaign_id>')
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    scripts = Script.query.filter_by(campaign_id=campaign_id).all()
    generated = GeneratedContent.query.filter_by(campaign_id=campaign_id).all()
    selected_script = Script.query.filter_by(campaign_id=campaign_id, is_selected=True).first()
    return render_template(
        'campaign.html',
        campaign=campaign,
        scripts=scripts,
        generated=generated,
        selected_script=selected_script
    )


# ─── Paso 3: Seleccionar guion y generar contenido ──────────────
@main_bp.route('/campaign/<int:campaign_id>/select/<int:script_id>', methods=['POST'])
def select_script(campaign_id, script_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    script = Script.query.get_or_404(script_id)

    # Desmarcar todos los guiones de esta campaña
    Script.query.filter_by(campaign_id=campaign_id).update({'is_selected': False})
    script.is_selected = True

    # Eliminar contenido generado anterior
    GeneratedContent.query.filter_by(campaign_id=campaign_id).delete()

    output_dir = current_app.config['GENERATED_FOLDER']

    # Generar 3 fotos
    photo_files = generate_photos(campaign.company_name, script.content, output_dir)
    for pf in photo_files:
        content = GeneratedContent(
            campaign_id=campaign_id,
            script_id=script_id,
            content_type='photo',
            file_path=pf,
            caption=f"📸 Marketing content for {campaign.company_name}"
        )
        db.session.add(content)

    # Generar 1 video
    video_file = generate_video(campaign.company_name, script.content, output_dir)
    video_content = GeneratedContent(
        campaign_id=campaign_id,
        script_id=script_id,
        content_type='video',
        file_path=video_file,
        caption=f"🎬 Video marketing for {campaign.company_name}"
    )
    db.session.add(video_content)

    db.session.commit()
    flash('✅ ¡Contenido generado! 3 fotos y 1 video listos para publicar.', 'success')
    return redirect(url_for('main.view_campaign', campaign_id=campaign_id))


# ─── Paso 4: Publicar en red social (simulado) ──────────────────
@main_bp.route('/campaign/<int:campaign_id>/publish', methods=['POST'])
def publish(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    platform = request.form.get('platform', 'instagram')

    generated = GeneratedContent.query.filter_by(
        campaign_id=campaign_id,
        published=False
    ).all()

    if not generated:
        flash('⚠️ No hay contenido pendiente de publicar.', 'warning')
        return redirect(url_for('main.view_campaign', campaign_id=campaign_id))

    results = []
    for content in generated:
        result = simulate_publish(platform, campaign.company_name, content.content_type)
        content.published = True
        content.published_platform = platform
        content.published_at = datetime.utcnow()
        results.append(result)

    db.session.commit()

    flash(f'🎉 ¡{len(results)} piezas publicadas en {platform.capitalize()}!', 'success')
    return redirect(url_for('main.view_campaign', campaign_id=campaign_id))


# ─── API: Historial de campañas ─────────────────────────────────
@main_bp.route('/api/campaigns')
def api_campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'company_name': c.company_name,
        'description': c.description,
        'original_photo': c.original_photo,
        'created_at': c.created_at.isoformat(),
        'scripts_count': len(c.scripts),
        'content_count': len(c.generated_content),
    } for c in campaigns])


# ─── Eliminar campaña ───────────────────────────────────────────
@main_bp.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('🗑️ Campaña eliminada.', 'info')
    return redirect(url_for('main.index'))
