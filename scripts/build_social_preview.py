#!/usr/bin/env python3
"""Build the homepage sharing image from approved original brand photos.
Requires Pillow and DejaVu fonts. No facial retouching or recoloring.
Only image sizing/cropping and homepage head metadata are changed.
"""
from pathlib import Path
from html import escape
import hashlib
import json
import re
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SCALE = 2
WIDTH, HEIGHT = 1200, 630
NAME = 'david-j-fowler-social-preview-v18.jpg'
URL = 'https://davidjfowler.com/'
TITLE = 'David J. Fowler | Ministry, Business & Global Impact'
DESCRIPTION = ('Explore the ministries, businesses, books and projects of David J. Fowler. '
               'One calling. Many expressions.')
ALT = ('David J. Fowler with his approved DJF monogram. One calling. Many expressions. '
       'Ministry, business, books and global impact. DavidJFowler.com.')


def font(size, bold=False, serif=False):
    family = 'DejaVuSerif' if serif else 'DejaVuSans'
    suffix = '-Bold' if bold else ''
    filename = family + suffix + '.ttf'
    for directory in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/dejavu'):
        path = Path(directory) / filename
        if path.exists():
            return ImageFont.truetype(str(path), round(size * SCALE))
    return ImageFont.truetype(filename, round(size * SCALE))


def rect(box):
    return tuple(round(v * SCALE) for v in box)


def text(draw, xy, value, size, color, bold=False, serif=False):
    f = font(size, bold, serif)
    draw.text(tuple(round(v * SCALE) for v in xy), value, font=f, fill=color, anchor='lt')
    return draw.textbbox((0, 0), value, font=f)[2] / SCALE


def tracking(draw, xy, value, size, color, spacing=2):
    x, y = xy
    f = font(size, True)
    for letter in value:
        draw.text((round(x * SCALE), round(y * SCALE)), letter, font=f, fill=color, anchor='lt')
        x += draw.textlength(letter, font=f) / SCALE + spacing
    return x


def make_image():
    gradient = Image.linear_gradient('L').resize((WIDTH * SCALE, HEIGHT * SCALE))
    canvas = ImageOps.colorize(gradient, '#07111e', '#102944').convert('RGBA')
    light = Image.new('RGBA', canvas.size)
    ld = ImageDraw.Draw(light)
    ld.ellipse(rect((-250, 255, 610, 1080)), fill=(21, 107, 198, 49))
    ld.ellipse(rect((695, -275, 1420, 445)), fill=(69, 111, 154, 45))
    light = light.filter(ImageFilter.GaussianBlur(105 * SCALE))
    canvas = Image.alpha_composite(canvas, light)
    draw = ImageDraw.Draw(canvas)
    draw.line(rect((48, 32, 1152, 32)), fill=(165, 138, 85, 125), width=SCALE)
    draw.line(rect((48, 597, 1152, 597)), fill=(68, 135, 196, 160), width=SCALE)
    draw.line(rect((810, 71, 810, 559)), fill=(198, 163, 93, 140), width=SCALE)

    # Original portrait: remove only the white mat and crop the sides.
    portrait = Image.open(ASSETS / 'dave-fowler-portrait.jpeg').convert('RGB')
    w, h = portrait.size
    portrait = portrait.crop((round(w * .040), round(h * .040), round(w * .960), round(h * .960)))
    portrait = ImageOps.fit(portrait, (328 * SCALE, 502 * SCALE),
                           Image.Resampling.LANCZOS, centering=(.5, .45))
    mask = Image.new('L', portrait.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, portrait.width - 1, portrait.height - 1),
                                           radius=22 * SCALE, fill=255)
    canvas.paste(portrait, (841 * SCALE, 63 * SCALE), mask)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(rect((841, 63, 1169, 565)), radius=22 * SCALE,
                           outline=(152, 169, 190, 105), width=SCALE)

    # Approved uploaded monogram, not a redrawn logo.
    logo = Image.open(ASSETS / 'djf-monogram.png').convert('RGBA')
    white = Image.new('RGBA', logo.size, 'white')
    white.alpha_composite(logo)
    logo = white.convert('RGB').resize((112 * SCALE, 112 * SCALE), Image.Resampling.LANCZOS)
    logo_mask = Image.new('L', logo.size)
    ImageDraw.Draw(logo_mask).rounded_rectangle((0, 0, logo.width - 1, logo.height - 1),
                                                radius=17 * SCALE, fill=255)
    canvas.paste(logo, (62 * SCALE, 65 * SCALE), logo_mask)
    draw = ImageDraw.Draw(canvas)
    text(draw, (198, 88), 'DAVID J. FOWLER', 32, '#f3d28d', True)
    tracking(draw, (200, 138), 'FAITH  /  FAMILY  /  PURPOSE', 12, '#a4c0db', 1.7)
    text(draw, (60, 218), 'One calling.', 63, '#f6f5f1', True, True)
    text(draw, (60, 298), 'Many expressions.', 56, '#f0c771', True)
    draw.line(rect((64, 389, 144, 389)), fill='#e5bb66', width=3 * SCALE)
    tracking(draw, (64, 418), 'MINISTRY  /  BUSINESS', 18, '#b9d7ef', 1.7)
    tracking(draw, (64, 451), 'BOOKS  /  GLOBAL IMPACT', 18, '#b9d7ef', 1.7)
    text(draw, (62, 525), 'DavidJFowler.com', 39, '#f3d28d', True)
    draw.line(rect((496, 548, 529, 548)), fill='#f3d28d', width=2 * SCALE)
    draw.line(rect((519, 538, 529, 548)), fill='#f3d28d', width=2 * SCALE)
    draw.line(rect((519, 558, 529, 548)), fill='#f3d28d', width=2 * SCALE)
    image = canvas.convert('RGB').resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    image.save(ASSETS / NAME, 'JPEG', quality=94, subsampling=0, optimize=True)
    image.save(ASSETS / NAME.replace('.jpg', '.png'), 'PNG', optimize=True)
    return image


def update_metadata():
    path = ROOT / 'index.html'
    html = path.read_text(encoding='utf-8')
    before_body = html.split('</head>', 1)[1]
    match = re.search(r'<head>(.*?)</head>', html, flags=re.S)
    if match is None:
        raise ValueError('Homepage head element missing; no changes made.')
    head = match.group(1)
    head = re.sub(r'\s*<!-- SOCIAL PREVIEW V18 START -->.*?<!-- SOCIAL PREVIEW V18 END -->', '', head, flags=re.S)
    head = re.sub(r'\s*<meta\b[^>]*(?:property|name)=["\'](?:og:|twitter:)[^>]*>', '', head, flags=re.I)
    head = re.sub(r'\s*<link\b[^>]*rel=["\']canonical["\'][^>]*>', '', head, flags=re.I)
    image_url = URL + 'assets/' + NAME
    tags = [
        '<!-- SOCIAL PREVIEW V18 START -->',
        f'<link rel="canonical" href="{URL}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="David J. Fowler">',
        '<meta property="og:locale" content="en_US">',
        f'<meta property="og:url" content="{URL}">',
        f'<meta property="og:title" content="{escape(TITLE, quote=True)}">',
        f'<meta property="og:description" content="{escape(DESCRIPTION, quote=True)}">',
        f'<meta property="og:image" content="{image_url}">',
        f'<meta property="og:image:secure_url" content="{image_url}">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{escape(ALT, quote=True)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{escape(TITLE, quote=True)}">',
        f'<meta name="twitter:description" content="{escape(DESCRIPTION, quote=True)}">',
        f'<meta name="twitter:image" content="{image_url}">',
        f'<meta name="twitter:image:alt" content="{escape(ALT, quote=True)}">',
        '<!-- SOCIAL PREVIEW V18 END -->'
    ]
    head = head.rstrip() + '\n\n  ' + '\n  '.join(tags) + '\n'
    html = html[:match.start(1)] + head + html[match.end(1):]
    assert before_body == html.split('</head>', 1)[1], 'Visible website was changed.'
    path.write_text(html, encoding='utf-8')


def main():
    ASSETS.mkdir(exist_ok=True)
    image = make_image()
    update_metadata()
    actual = Image.open(ASSETS / NAME)
    assert actual.size == (1200, 630)
    assert (ASSETS / NAME).stat().st_size < 1000000
    print(json.dumps({'thumbnail': str(ASSETS / NAME), 'size': image.size,
                      'bytes': (ASSETS / NAME).stat().st_size,
                      'sha256': hashlib.sha256((ASSETS / NAME).read_bytes()).hexdigest(),
                      'status': 'Created image and connected homepage sharing metadata; visible content unchanged.'}, indent=2))


if __name__ == '__main__':
    main()
