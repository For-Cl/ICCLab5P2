"""
Servicios de IA simulados (Mock) para generación de guiones, imágenes y video.
En producción, estos se reemplazarían por llamadas a APIs reales (OpenAI, Stability AI, etc.)
"""
import os
import random
import uuid
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


# ─── Colores de marca para las imágenes generadas ───
BRAND_PALETTES = [
    [(42, 47, 79), (78, 91, 166), (147, 157, 218)],      # Azul profundo
    [(79, 42, 42), (166, 78, 78), (218, 147, 147)],       # Rojo elegante
    [(42, 79, 55), (78, 166, 104), (147, 218, 170)],      # Verde natural
    [(79, 66, 42), (166, 138, 78), (218, 193, 147)],      # Dorado cálido
    [(66, 42, 79), (138, 78, 166), (193, 147, 218)],      # Púrpura creativo
]

SCRIPT_TEMPLATES = {
    'profesional': {
        'titles': [
            'Excelencia {company} – Campaña Corporativa',
            'Innovación y Liderazgo {company}',
            'La Calidad que Define a {company}',
        ],
        'contents': [
            (
                '🎯 GUION PROFESIONAL\n\n'
                'Escena 1: Plano aéreo de las instalaciones de {company}. '
                'Voz en off: "En un mundo que exige excelencia, {company} lidera el camino."\n\n'
                'Escena 2: Equipo trabajando con dedicación. '
                'Texto en pantalla: "Compromiso. Innovación. Resultados."\n\n'
                'Escena 3: Producto/servicio destacado con iluminación premium. '
                'CTA: "Descubre más en {company}.com"\n\n'
                '🎵 Música: Corporativa inspiradora\n'
                '⏱ Duración sugerida: 30 segundos'
            ),
        ],
    },
    'divertido': {
        'titles': [
            '¡Vive la experiencia {company}! 🎉',
            '{company} rompe esquemas 🚀',
            'Lo mejor de {company}, ¡sin filtro! ✨',
        ],
        'contents': [
            (
                '🎬 GUION DIVERTIDO\n\n'
                'Escena 1: Persona aburrida con el producto de la competencia. '
                'Efecto de sonido: "womp womp" 😴\n\n'
                'Escena 2: ¡BOOM! Aparece {company} con una entrada épica. '
                'Transición: Glitch colorido con música trap 🎵\n\n'
                'Escena 3: Montaje rápido mostrando la magia de {company}. '
                'Reacciones exageradas, emojis flotantes 🤩\n\n'
                'Escena 4: Logo de {company} con efecto neón. '
                'CTA: "¡Síguenos para más! @{company_lower}"\n\n'
                '🎵 Música: Beat viral de TikTok\n'
                '⏱ Duración sugerida: 15-20 segundos'
            ),
        ],
    },
    'emocional': {
        'titles': [
            'La historia detrás de {company} ❤️',
            '{company}: Más que una marca, una familia 🌟',
            'Tu momento con {company} 💫',
        ],
        'contents': [
            (
                '💝 GUION EMOCIONAL\n\n'
                'Escena 1: Amanecer. Plano detalle de manos trabajando con cariño. '
                'Voz en off susurrada: "Todo gran sueño empieza con un pequeño gesto..."\n\n'
                'Escena 2: Personas reales usando/disfrutando {company}. '
                'Sonrisas genuinas, momentos cotidianos. Música de piano suave 🎹\n\n'
                'Escena 3: Testimonios breves. "Gracias a {company}, mi vida cambió." '
                'Lágrimas de alegría, abrazos.\n\n'
                'Escena 4: Logo con fade lento. '
                'Texto: "{company} – Contigo en cada paso."\n\n'
                '🎵 Música: Piano + cuerdas emotivas\n'
                '⏱ Duración sugerida: 45 segundos'
            ),
        ],
    },
}


def generate_scripts(company_name: str) -> list[dict]:
    """Genera 3 guiones con diferentes tonos para la empresa dada."""
    scripts = []
    for tone, template in SCRIPT_TEMPLATES.items():
        title = random.choice(template['titles']).format(
            company=company_name
        )
        content = random.choice(template['contents']).format(
            company=company_name,
            company_lower=company_name.lower().replace(' ', '')
        )
        scripts.append({
            'title': title,
            'content': content,
            'tone': tone,
        })
    return scripts


def _create_marketing_image(
    output_path: str,
    text: str,
    company: str,
    palette: list[tuple],
    variant: int,
    size: tuple = (1080, 1080)
):
    """Genera una imagen de marketing simulada con gradientes y texto."""
    img = Image.new('RGB', size, palette[0])
    draw = ImageDraw.Draw(img)

    # Gradiente diagonal
    for y in range(size[1]):
        for x in range(size[0]):
            ratio_x = x / size[0]
            ratio_y = y / size[1]
            ratio = (ratio_x + ratio_y) / 2
            r = int(palette[0][0] * (1 - ratio) + palette[1][0] * ratio)
            g = int(palette[0][1] * (1 - ratio) + palette[1][1] * ratio)
            b = int(palette[0][2] * (1 - ratio) + palette[1][2] * ratio)
            img.putpixel((x, y), (r, g, b))

    # Formas decorativas
    accent = palette[2]
    if variant == 0:
        draw.ellipse([size[0]//4, size[1]//4, 3*size[0]//4, 3*size[1]//4],
                      outline=accent + (180,), width=3)
    elif variant == 1:
        draw.rectangle([100, 100, size[0]-100, size[1]-100],
                        outline=accent, width=4)
    else:
        for i in range(5):
            offset = i * 40
            draw.rounded_rectangle(
                [50+offset, 50+offset, size[0]-50-offset, size[1]-50-offset],
                radius=20, outline=accent, width=2
            )

    # Texto del nombre de empresa
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except (OSError, IOError):
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Nombre de empresa centrado
    bbox = draw.textbbox((0, 0), company, font=font_large)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - tw) // 2
    y = size[1] // 3
    # Sombra
    draw.text((x+2, y+2), company, fill=(0, 0, 0), font=font_large)
    draw.text((x, y), company, fill=(255, 255, 255), font=font_large)

    # Texto descriptivo
    lines = text.split('\n')
    y_offset = y + th + 40
    for line in lines[:3]:
        bbox = draw.textbbox((0, 0), line, font=font_small)
        tw2 = bbox[2] - bbox[0]
        x2 = (size[0] - tw2) // 2
        draw.text((x2, y_offset), line, fill=accent, font=font_small)
        y_offset += 40

    # Marca de agua "AI Generated"
    draw.text((20, size[1] - 40), "🤖 AI Generated - Marketing Suite", fill=(255, 255, 255, 128), font=font_small)

    img.save(output_path, 'JPEG', quality=90)


def generate_photos(company_name: str, script_content: str, output_dir: str) -> list[str]:
    """Genera 3 fotos de marketing basadas en el guion seleccionado."""
    palette = random.choice(BRAND_PALETTES)
    paths = []

    captions = [
        f"Presentamos {company_name}",
        f"{company_name} - Tu mejor elección",
        f"Vive la experiencia {company_name}",
    ]

    for i in range(3):
        filename = f"photo_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(output_dir, filename)
        _create_marketing_image(
            filepath, captions[i], company_name, palette, variant=i
        )
        paths.append(filename)

    return paths


def generate_video(company_name: str, script_content: str, output_dir: str) -> str:
    """
    Genera un 'video' simulado como una secuencia de frames guardada como GIF animado.
    En producción, esto usaría una API de generación de video (Runway, Pika, etc.)
    """
    palette = random.choice(BRAND_PALETTES)
    frames = []
    size = (1080, 1080)

    texts = [
        f"✨ {company_name} presenta...",
        f"🚀 Lo mejor está por venir",
        f"💫 {company_name}",
        f"👉 ¡Síguenos! @{company_name.lower().replace(' ', '')}",
    ]

    for i, text in enumerate(texts):
        img = Image.new('RGB', size, palette[0])
        draw = ImageDraw.Draw(img)

        # Gradiente con variación por frame
        shift = i * 30
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(palette[0][0] * (1 - ratio) + palette[1][0] * ratio) + shift
            g = int(palette[0][1] * (1 - ratio) + palette[1][1] * ratio)
            b = int(palette[0][2] * (1 - ratio) + palette[1][2] * ratio)
            r, g, b = min(r, 255), min(g, 255), min(b, 255)
            for x in range(size[0]):
                img.putpixel((x, y), (r, g, b))

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        except (OSError, IOError):
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (size[0] - tw) // 2
        y_pos = (size[1] - th) // 2
        draw.text((x+2, y_pos+2), text, fill=(0, 0, 0), font=font)
        draw.text((x, y_pos), text, fill=(255, 255, 255), font=font)

        frames.append(img)

    filename = f"video_{uuid.uuid4().hex[:8]}.gif"
    filepath = os.path.join(output_dir, filename)
    frames[0].save(
        filepath,
        save_all=True,
        append_images=frames[1:],
        duration=2000,
        loop=0
    )

    return filename


def simulate_publish(platform: str, company_name: str, content_type: str) -> dict:
    """Simula la publicación en una red social. Retorna datos del post simulado."""
    post_id = uuid.uuid4().hex[:12]
    now = datetime.utcnow()

    hashtags = [
        f"#{company_name.replace(' ', '')}",
        "#Marketing", "#IA", "#Publicidad",
        "#ContentCreator", "#DigitalMarketing"
    ]

    return {
        'success': True,
        'platform': platform,
        'post_id': post_id,
        'url': f"https://www.{platform}.com/p/{post_id}",
        'published_at': now.isoformat(),
        'hashtags': ' '.join(hashtags),
        'message': f'✅ Contenido publicado exitosamente en {platform.capitalize()}',
    }
