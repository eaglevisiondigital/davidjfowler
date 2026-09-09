#!/usr/bin/env python3
"""Build the approved David J. Fowler social sharing image.
Uses the original approved portrait and DJF monogram without retouching the face.
Only layout, cropping, scaling, typography, and social metadata are changed.
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
NAME = 'david-j-fowler-social-preview-v19.jpg'
URL = 'https://davidjfowler.com/'
TITLE = 'David J. Fowler | Business • Ministry • Resources'
DESCRIPTION = ('Explore all things related to David J. Fowler — business, ministry, books, '
               'resources and global impact.')
ALT = ('David J. Fowler with the DJF monogram and the words People, Purpose, Impact. '
       'Business, Ministry, Resources. DavidJFowler.com.')


def font(size, bold=False, serif=False, italic=False):
    if serif:
        family = 'DejaVuSerif'
    else:
        family = 'DejaVuSans'
    suffix = ''
    if bold and italic:
        suffix = '-BoldOblique'
    elif bold:
        suffix = '-Bold'
    elif italic:
        suffix = '-Oblique'
    filename = family + suffix + '.ttf'
    for directory in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/dejavu'):
        path = Path(directory) / filename
        if path.exists():
            return ImageFont.truetype(str(path), round(size * SCALE))
    return ImageFont.truetype(filename, round(size * SCALE))


def rect(box):
    return tuple(round(v * SCALE) for v in box)


def put_text(draw, xy, value, size, color, bold=False, serif=False, italic=False, anchor='la'):
    f = font(size, bold, serif, italic)
    draw.text((round(xy[0] * SCALE), round(xy[1] * SCALE)), value,
              font=f, fill=color, anchor=anchor)


def make_image():
    canvas = Image.new('RGBA', (WIDTH * SCALE, HEIGHT * SCALE), '#071423')

    # Premium navy atmosphere with restrained blue/gold depth.
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse(rect((-250, 40, 620, 800)), fill=(22, 84, 149, 90))
    gd.ellipse(rect((760, -180, 1480, 520)), fill=(22, 78, 136, 70))
    gd.ellipse(rect((920, 440, 1450, 850)), fill=(225, 170, 72, 34))
    glow = glow.filter(ImageFilter.GaussianBlur(95 * SCALE))
    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)

    # Subtle horizon/mountain silhouettes, keeping the share image elegant rather than busy.
    draw.polygon([rect((0, 455, 0, 455))[:2], rect((155, 390, 155, 390))[:2],
                  rect((305, 455, 305, 455))[:2], rect((470, 355, 470, 355))[:2],
                  rect((655, 470, 655, 470))[:2], rect((835, 405, 835, 405))[:2],
                  rect((1010, 475, 1010, 475))[:2], rect((1200, 375, 1200, 375))[:2],
                  rect((1200, 630, 1200, 630))[:2], rect((0, 630, 0, 630))[:2]],
                 fill=(4, 17, 30, 205))

    # Approved portrait. Remove only the surrounding white mat and fit it into the left panel.
    # No facial retouching, smoothing, recoloring, or generative alteration.
    portrait = Image.open(ASSETS / 'dave-fowler-portrait.jpeg').convert('RGB')
    w, h = portrait.size
    portrait = portrait.crop((round(w * .040), round(h * .040), round(w * .960), round(h * .960)))
    portrait = ImageOps.fit(portrait, (445 * SCALE, 610 * SCALE),
                           Image.Resampling.LANCZOS, centering=(.50, .42))
    fade = Image.new('L', portrait.size, 255)
    fd = ImageDraw.Draw(fade)
    # Soft fade only on the far right edge of the portrait, never altering the face itself.
    for x in range(round(350 * SCALE), portrait.width):
        alpha = max(0, 255 - int((x - 350 * SCALE) / max(1, portrait.width - 350 * SCALE) * 255))
        fd.line((x, 0, x, portrait.height), fill=alpha)
    canvas.paste(portrait, (0, 20 * SCALE), fade)
    draw = ImageDraw.Draw(canvas)

    # People / Purpose / Impact — intentionally visible, matching the approved revision.
    put_text(draw, (470, 112), 'People', 32, '#f0cc81', serif=True, italic=True)
    put_text(draw, (486, 161), 'Purpose', 32, '#f0cc81', serif=True, italic=True)
    put_text(draw, (498, 210), 'Impact', 32, '#f0cc81', serif=True, italic=True)
    draw.line(rect((492, 263, 565, 263)), fill='#e6bd68', width=2 * SCALE)

    # Approved DJF monogram at upper right. Preserve its original appearance.
    logo = Image.open(ASSETS / 'djf-monogram.png').convert('RGBA')
    # Trim surrounding whitespace while retaining all monogram pixels.
    bg = Image.new('RGBA', logo.size, (255, 255, 255, 255))
    comp = Image.alpha_composite(bg, logo)
    rgb = comp.convert('RGB')
    bbox = ImageOps.invert(ImageOps.grayscale(rgb)).getbbox()
    if bbox:
        rgb = rgb.crop(bbox)
    rgb.thumbnail((285 * SCALE, 245 * SCALE), Image.Resampling.LANCZOS)
    # White pixels from the source tile become transparent against the dark background.
    rgba = rgb.convert('RGBA')
    pix = rgba.load()
    for yy in range(rgba.height):
        for xx in range(rgba.width):
            r, g, b, a = pix[xx, yy]
            if r > 242 and g > 242 and b > 242:
                pix[xx, yy] = (r, g, b, 0)
    canvas.alpha_composite(rgba, (780 * SCALE, 28 * SCALE))
    draw = ImageDraw.Draw(canvas)

    # Main identity and supporting message.
    put_text(draw, (620, 286), 'David J. Fowler', 57, '#f5f5f2', serif=True)
    draw.line(rect((616, 367, 1146, 367)), fill='#e8c06c', width=2 * SCALE)
    put_text(draw, (650, 388), 'Business  •  Ministry  •  Resources', 25, '#f0f1f3', serif=True)
    put_text(draw, (678, 432), 'Explore all things related to David J. Fowler', 18,
             '#e3e6e9', serif=True, italic=True)

    # URL CTA box.
    draw.rounded_rectangle(rect((700, 477, 1103, 536)), radius=29 * SCALE,
                           fill=(7, 27, 47, 245), outline='#e9bd63', width=2 * SCALE)
    put_text(draw, (900, 507), 'DAVIDJFOWLER.COM', 25, '#f7f7f6', bold=True, anchor='mm')
    draw.line(rect((1065, 496, 1078, 507)), fill='#e9bd63', width=3 * SCALE)
    draw.line(rect((1065, 518, 1078, 507)), fill='#e9bd63', width=3 * SCALE)

    # Three concise pillars at the bottom.
    put_text(draw, (715, 575), 'BUSINESS', 14, '#f3f4f5', bold=True, anchor='mm')
    put_text(draw, (890, 575), 'MINISTRY', 14, '#f3f4f5', bold=True, anchor='mm')
    put_text(draw, (1062, 575), 'RESOURCES', 14, '#f3f4f5', bold=True, anchor='mm')
    draw.line(rect((798, 555, 798, 590)), fill=(211, 174, 95, 160), width=SCALE)
    draw.line(rect((974, 555, 974, 590)), fill=(211, 174, 95, 160), width=SCALE)

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
    head = re.sub(r'\s*<!-- SOCIAL PREVIEW V\d+ START -->.*?<!-- SOCIAL PREVIEW V\d+ END -->', '', head, flags=re.S)
    head = re.sub(r'\s*<meta\b[^>]*(?:property|name)=["\'](?:og:|twitter:)[^>]*>', '', head, flags=re.I)
    head = re.sub(r'\s*<link\b[^>]*rel=["\']canonical["\'][^>]*>', '', head, flags=re.I)
    image_url = URL + 'assets/' + NAME
    tags = [
        '<!-- SOCIAL PREVIEW V19 START -->',
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
        '<!-- SOCIAL PREVIEW V19 END -->'
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
                      'status': 'Approved-style social preview created and connected; visible page content unchanged.'}, indent=2))


if __name__ == '__main__':
    main()
