#!/usr/bin/env python3
"""Eksport Prismic -> markdowny + pobranie zdjec/PDFow."""
import json
import os
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / 'public'
IMG_DIR = PUBLIC / 'uploads' / 'images'
PDF_DIR = PUBLIC / 'uploads' / 'pdfs'
CONTENT = ROOT / 'content'
EXHIBITS = CONTENT / 'exhibits'
PAGES = CONTENT / 'pages'
SETTINGS = CONTENT / 'settings'

for d in (IMG_DIR, PDF_DIR, EXHIBITS, PAGES, SETTINGS):
    d.mkdir(parents=True, exist_ok=True)


def download(url, dest):
    """Pobierz plik jesli nie istnieje."""
    if dest.exists():
        return False
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f'  ERR {url}: {e}')
        return False


def safe_filename(url):
    """Zamien URL na bezpieczna nazwe pliku."""
    parsed = urllib.parse.urlparse(url)
    name = os.path.basename(parsed.path)
    return re.sub(r'[^a-zA-Z0-9._-]', '_', name)


def rt_to_plain(rt):
    """Rich text -> plain text z zachowaniem \\n."""
    if not rt:
        return ''
    return '\n'.join(b.get('text', '') for b in rt if b.get('type') in ('paragraph', 'heading1', 'heading2', 'heading3'))


def yaml_escape(s):
    """Escape stringu do YAML frontmatter."""
    if s is None:
        return ''
    s = str(s).replace('\\', '\\\\').replace('"', '\\"')
    return s


with open(ROOT / 'prismic-export' / 'all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

stats = {'imgs': 0, 'pdfs': 0, 'exhibits': 0, 'pages': 0, 'settings': 0}

for doc in data['results']:
    typ = doc['type']
    uid = doc.get('uid') or doc['id']
    lang = doc['lang']
    d = doc['data']

    # ====== EKSPONAT ======
    if typ == 'gallery':
        slices = d.get('slices', [])
        if not slices:
            continue
        p = slices[0].get('primary', {})

        title = rt_to_plain(d.get('title', [])) or rt_to_plain(p.get('heading', []))
        description = rt_to_plain(p.get('description', []))
        text = rt_to_plain(p.get('text', []))

        # Image
        img_url = ''
        img_alt = ''
        img = p.get('image', {})
        if img and img.get('url'):
            img_url_full = img['url']
            fname = safe_filename(img_url_full)
            if download(img_url_full, IMG_DIR / fname):
                stats['imgs'] += 1
            img_url = f'/uploads/images/{fname}'
            img_alt = img.get('alt') or title

        # PDF
        pdf_url = ''
        pdf_label = ''
        pdf = p.get('pdfLink', {})
        if pdf and pdf.get('url'):
            fname = safe_filename(pdf['url'])
            if download(pdf['url'], PDF_DIR / fname):
                stats['pdfs'] += 1
            pdf_url = f'/uploads/pdfs/{fname}'
            pdf_label = pdf.get('text', 'Pobierz dokumentacje PDF')

        # Sasiednie eksponaty (nawigacja)
        prev_uid = (p.get('leftArrow') or {}).get('uid', '')
        next_uid = (p.get('rightArrow') or {}).get('uid', '')

        # Zapis MD
        out = EXHIBITS / f'{uid}_{lang}.md'
        fm = [
            '---',
            f'title: "{yaml_escape(title)}"',
            f'lang: {lang}',
            f'slug: {uid}',
            f'image: "{img_url}"',
            f'imageAlt: "{yaml_escape(img_alt)}"',
            f'pdfUrl: "{pdf_url}"',
            f'pdfLabel: "{yaml_escape(pdf_label)}"',
            f'prevSlug: "{prev_uid}"',
            f'nextSlug: "{next_uid}"',
            f'firstPublished: "{doc["first_publication_date"]}"',
            f'lastPublished: "{doc["last_publication_date"]}"',
            'metadata: |',
        ]
        for line in (description or '').split('\n'):
            fm.append(f'  {line}')
        fm.append('---')
        fm.append('')
        fm.append(text)
        out.write_text('\n'.join(fm), encoding='utf-8')
        stats['exhibits'] += 1

    # ====== STRONA STATYCZNA ======
    elif typ == 'page':
        out = PAGES / f'{uid}_{lang}.json'
        out.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
        stats['pages'] += 1
        # Pobierz zdjecia ze stron statycznych
        for slice_ in d.get('slices', []):
            for k, v in (slice_.get('primary') or {}).items():
                if isinstance(v, dict) and v.get('url') and 'images.prismic.io' in str(v.get('url', '')):
                    fname = safe_filename(v['url'])
                    if download(v['url'], IMG_DIR / fname):
                        stats['imgs'] += 1
            for item in (slice_.get('items') or []):
                for k, v in (item or {}).items():
                    if isinstance(v, dict) and v.get('url') and 'images.prismic.io' in str(v.get('url', '')):
                        fname = safe_filename(v['url'])
                        if download(v['url'], IMG_DIR / fname):
                            stats['imgs'] += 1

    # ====== SETTINGS / FOOTER / NAVIGATION / SOCIAL ======
    else:
        out = SETTINGS / f'{typ}_{lang}.json'
        out.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
        stats['settings'] += 1

print('=== STATS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
print(f'\n=== Pliki w content/ ===')
for d in (EXHIBITS, PAGES, SETTINGS):
    print(f'  {d.name}: {len(list(d.iterdir()))}')
print(f'\n=== Pliki binarne ===')
print(f'  images: {len(list(IMG_DIR.iterdir()))}')
print(f'  pdfs:   {len(list(PDF_DIR.iterdir()))}')
