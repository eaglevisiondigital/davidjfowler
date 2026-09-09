#!/usr/bin/env python3
"""Connect the approved static thumbnail. Never draw or modify image pixels.

Scope: eaglevisiondigital/davidjfowler, homepage head metadata only.
Uses the Python standard library; no image-rendering or font dependencies.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import hashlib
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'eaglevisiondigital/davidjfowler'
NAME = 'david-j-fowler-social-approved-v19.jpg'
APPROVED_SHA256 = '3b528f4b914eb00da72b3c39cf6f783d637ad15c2c911a9bd1f0b6bf77146418'
SITE = 'https://davidjfowler.com/'
IMAGE_URL = SITE + 'assets/' + NAME
TITLE = 'David J. Fowler | Business, Ministry & Resources'
DESCRIPTION = ('Explore the businesses, ministries, books and resources of David J. Fowler. '
               'People. Purpose. Impact.')
ALT = ('David J. Fowler with the gold DJF monogram, People, Purpose, Impact, '
       'and Business, Ministry, Resources. DavidJFowler.com.')


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'meta':
            key = attrs.get('property') or attrs.get('name')
            if key:
                self.meta.setdefault(key, []).append(attrs.get('content', ''))


def connect_head(html):
    """Return the same page with only its social head metadata replaced."""
    match = re.search(r'<head\b[^>]*>(.*?)</head>', html, re.I | re.S)
    if match is None:
        raise ValueError('Homepage head missing. No files were changed.')
    head = match.group(1)
    head = re.sub(r'\s*<!-- SOCIAL PREVIEW V\d+ START -->.*?<!-- SOCIAL PREVIEW V\d+ END -->',
                  '', head, flags=re.S)
    head = re.sub(r'\s*<meta\b[^>]*(?:property|name)=["\'](?:og:|twitter:)[^>]*>',
                  '', head, flags=re.I)
    head = re.sub(r'\s*<link\b[^>]*rel=["\']canonical["\'][^>]*>', '', head, flags=re.I)
    values = [
        ('property', 'og:type', 'website'),
        ('property', 'og:site_name', 'David J. Fowler'),
        ('property', 'og:locale', 'en_US'),
        ('property', 'og:url', SITE),
        ('property', 'og:title', TITLE),
        ('property', 'og:description', DESCRIPTION),
        ('property', 'og:image', IMAGE_URL),
        ('property', 'og:image:secure_url', IMAGE_URL),
        ('property', 'og:image:type', 'image/jpeg'),
        ('property', 'og:image:width', '1200'),
        ('property', 'og:image:height', '630'),
        ('property', 'og:image:alt', ALT),
        ('name', 'twitter:card', 'summary_large_image'),
        ('name', 'twitter:title', TITLE),
        ('name', 'twitter:description', DESCRIPTION),
        ('name', 'twitter:image', IMAGE_URL),
        ('name', 'twitter:image:alt', ALT),
    ]
    lines = ['<!-- SOCIAL PREVIEW V20 START -->', f'<link rel="canonical" href="{SITE}">']
    lines.extend(f'<meta {kind}="{key}" content="{escape(value, quote=True)}">'
                 for kind, key, value in values)
    lines.append('<!-- SOCIAL PREVIEW V20 END -->')
    new_head = head.rstrip() + '\n\n  ' + '\n  '.join(lines) + '\n'
    updated = html[:match.start(1)] + new_head + html[match.end(1):]
    if updated.split('</head>', 1)[1] != html.split('</head>', 1)[1]:
        raise ValueError('Visible page content changed. No files were written.')
    parsed = MetaParser()
    parsed.feed(updated)
    for _, key, value in values:
        if parsed.meta.get(key) != [value]:
            raise ValueError('Missing or duplicate social metadata: ' + key)
    return updated


def main():
    context_repo = os.environ.get('GITHUB_REPOSITORY')
    if context_repo and context_repo != REPOSITORY:
        raise ValueError('This script is restricted to ' + REPOSITORY)
    asset = ROOT / 'assets' / NAME
    if not asset.is_file():
        raise FileNotFoundError(
            'Approved thumbnail not uploaded yet. Add ' + NAME + ' to the assets folder. '
            'The image will not be redrawn, and the homepage has not been changed.')
    original_image = asset.read_bytes()
    if hashlib.sha256(original_image).hexdigest() != APPROVED_SHA256:
        raise ValueError('Image differs from the approved file. Homepage metadata was not changed.')
    page = ROOT / 'index.html'
    original_page = page.read_text(encoding='utf-8')
    updated = connect_head(original_page)
    if '--check' in sys.argv:
        if updated != original_page:
            raise ValueError('Approved thumbnail is present but metadata still needs connecting.')
    elif updated != original_page:
        temp = page.with_name('.index-social-preview.tmp')
        temp.write_text(updated, encoding='utf-8')
        temp.replace(page)
    if asset.read_bytes() != original_image:
        raise ValueError('Approved image unexpectedly changed.')
    print(json.dumps({'status': 'approved_static_thumbnail_connected',
                      'scope': SITE, 'image': IMAGE_URL, 'size': [1200, 630],
                      'sha256': APPROVED_SHA256, 'image_modified': False,
                      'visible_page_modified': False}, indent=2))


if __name__ == '__main__':
    main()
