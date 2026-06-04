"""Wyciag EN opisy z PDF KRS strona 2 (Eng), aplikuj do EN markdownow.

Dla eksponatow z unikalnym PDF KRS (12 sztuk: 3 oryginalne + 9 unikalne).
Generic KRS-3 PDF ma EN tylko dla Lefem; pozostale 8 generic eksponatow
dostana tlumaczenia przez add_drafts_en.py.
"""
import fitz
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
EXHIBITS = ROOT / 'content' / 'exhibits'
PDFS = ROOT / 'public' / 'uploads' / 'pdfs'

# 12 eksponatow z PDF ktore maja EN strone 2
WITH_EN_PDF = [
    ('lefem',                        'aM0f_2GNHVfTPdMV_KRS-3-opis-pelny-do-pobrania.pdf'),
    ('kogut-okukur',                 'aNppEZ5xUNkB1NyM_KRS9opispelnydopobraniaPL_ENG.pdf'),
    ('takangledeangle',              'aNppDp5xUNkB1NyK_KRS17opispelnydopobraniaPL_ENG.pdf'),
    ('beben-szczelinowy',            'aNppDZ5xUNkB1NyJ_KRS22opispelnydopobraniaPL_ENG.pdf'),
    ('chamba',                       'aNppCJ5xUNkB1NyE_KRS78opispelnydopobraniaPL_ENG.pdf'),
    ('meski-fetysz-mocy-bitekibuti', 'aNppDJ5xUNkB1NyI_KRS25opispelnydopobraniaPL_ENG.pdf'),
    ('mbulu-ngulu-relikwiarz-meski', 'aNppCZ5xUNkB1NyF_KRS68opispelnydopobraniaPL_ENG.pdf'),
    ('ngil',                         'aNppBp5xUNkB1NyC_KRS90opispelnydopobraniaPL_ENG.pdf'),
    ('nkishi-nkondi',                'aNppC55xUNkB1NyH_KRS27opispelnydopobraniaPL_ENG.pdf'),
    ('takangledeangle-2',            'aNppC55xUNkB1NyG_KRS33opispelnydopobraniaPL_ENG.pdf'),
    ('troh',                         'aNppB55xUNkB1NyD_KRS81opispelnydopobraniaPL_ENG.pdf'),
    ('troh-2',                       'aNppBZ5xUNkB1NyB_KRS94opispelnydopobraniaPL_ENG.pdf'),
]


def parse_pdf_page_en(pdf_path: Path) -> dict:
    """Wyciag z EN sekcji (wszystkie strony zaczynajace 'The Joanna...' i nastepne EN strony).

    PDF moga miec rozna strukture:
      3-stronicowe: p1 PL, p2 EN, p3 copyright
      4-stronicowe: p1 PL pt 1, p2 PL pt 2, p3 EN pt 1, p4 EN pt 2
      6-stronicowe: p1-3 PL, p4-6 EN
    """
    doc = fitz.open(pdf_path)
    # Znajdz ostatnia strone z PL naglowkiem, wez wszystko po niej (EN sekcja)
    pages_text = [doc[i].get_text("text") for i in range(doc.page_count)]
    doc.close()

    last_pl_idx = -1
    for i, t in enumerate(pages_text):
        if 'Kolekcja Joanny i Ryszarda Stolarskich' in t or 'Historia/Prowieniencja' in t:
            last_pl_idx = i

    en_pages = []
    for i in range(last_pl_idx + 1, len(pages_text)):
        t = pages_text[i]
        # Pomin tylko-copyright strony
        if t.strip().startswith('©') or ('All rights reserved' in t[:300] and len(t.strip()) < 600):
            continue
        # Pomin strony zawierajace polski naglowek (na wszelki wypadek)
        if 'Kolekcja Joanny i Ryszarda Stolarskich' in t:
            continue
        en_pages.append(t)
    if not en_pages:
        return {'fields': {}, 'description': '', 'provenance': ''}
    text = '\n'.join(en_pages)

    lines = [l.rstrip() for l in text.split('\n')]
    META_KEYS = ['Origin', 'People/Ethnic Group', 'People / Ethnic Group',
                 'Material', 'Technique', 'Height', 'Length', 'Width',
                 'Diameter', 'Dimensions', 'Age']
    fields = {}
    description_lines = []
    provenance_lines = []
    section = 'header'
    desc_buffer = []

    for line in lines:
        l = line.strip()
        if not l:
            if section == 'description' and desc_buffer:
                description_lines.append(' '.join(desc_buffer))
                desc_buffer = []
            continue

        if l.startswith('Prepared by') or l.startswith('Prepared:'):
            if desc_buffer:
                description_lines.append(' '.join(desc_buffer))
                desc_buffer = []
            section = 'opracowanie'
            continue
        if l.startswith('History') or l.startswith('Provenance'):
            section = 'provenance'
            continue
        if l.startswith('The Joanna') or l.startswith('Exhibit KSR') or l.startswith('Exhibit KRS') \
           or l.startswith('Name') or l.startswith('African Art') \
           or l.startswith('Kolekcja Joanny'):
            continue
        # Ignoruj PL pola metadata ktore klient zostawil mimo EN header
        is_pl_field = bool(re.match(
            r'^(Nazwa|Pochodzenie|Lud/grupa etniczna|Lud/ grupa etniczna|Materiał|Material'
            r'|Technika|Wysokość|Wysokosc|Wiek|Wymiary|Długość|Dlugosc|Szerokość|Szerokosc'
            r'|Średnica|Srednica)\s*[-–—]',
            l))
        if is_pl_field:
            continue
        # Pomin pojedyncze frazy PL ktore moga sie trafic
        if l in ('Kolekcja - Rudolf Steinmann', 'Historia/Prowieniencja:', 'Historia/Proweniencja:'):
            continue
        is_footer = (
            l.startswith('info@') or l.startswith('©')
            or 'No part of this publication' in l
            or 'All rights reserved' in l
            or 'Quoting short' in l
        )
        if is_footer:
            if section == 'description' and desc_buffer:
                description_lines.append(' '.join(desc_buffer))
                desc_buffer = []
            section = 'footer'
            continue
        if section == 'footer':
            continue

        is_meta_field = False
        for key in META_KEYS:
            m = re.match(rf'^{re.escape(key)}\s*[-–—]\s*(.+)$', l)
            if m:
                fields[key] = m.group(1).strip()
                is_meta_field = True
                break
        if is_meta_field:
            section = 'meta'
            continue

        if section in ('header', 'meta'):
            section = 'description'
        if section == 'description':
            desc_buffer.append(l)
        elif section == 'provenance':
            provenance_lines.append(l)

    if desc_buffer:
        description_lines.append(' '.join(desc_buffer))
    return {
        'fields': fields,
        'description': '\n\n'.join(description_lines).strip(),
        'provenance': '\n'.join(provenance_lines).strip(),
    }


def update_md(uid: str, parsed: dict) -> None:
    md_path = EXHIBITS / f'{uid}_en-us.md'
    if not md_path.exists():
        print(f'  ! brak {md_path.name}')
        return
    raw = md_path.read_text(encoding='utf-8')
    parts = raw.split('---', 2)
    if len(parts) < 3:
        print(f'  ! zly format {uid}')
        return

    fm_text = parts[1]
    fields = parsed['fields']
    canonical = [
        ('Origin',              fields.get('Origin')),
        ('People/Ethnic Group', fields.get('People/Ethnic Group') or fields.get('People / Ethnic Group')),
        ('Material',            fields.get('Material')),
        ('Technique',           fields.get('Technique')),
        ('Height',              fields.get('Height')),
        ('Length',              fields.get('Length')),
        ('Width',               fields.get('Width')),
        ('Diameter',            fields.get('Diameter')),
        ('Dimensions',          fields.get('Dimensions')),
        ('Age',                 fields.get('Age')),
    ]
    meta_lines = [f'{label}: {value}' for label, value in canonical if value]
    new_metadata_block = '\n'.join(meta_lines)

    new_fm = re.sub(
        r'(metadata:\s*\|)(.*?)(?=\n[a-zA-Z_]+:|\Z)',
        lambda m: 'metadata: |\n' + '\n'.join(f'  {l}' for l in new_metadata_block.split('\n')) + '\n',
        fm_text, count=1, flags=re.DOTALL,
    )
    if not new_fm.endswith('\n'):
        new_fm += '\n'

    body = parsed['description']
    if parsed.get('provenance'):
        body += '\n\n**History / Provenance:**\n\n' + parsed['provenance']

    # Update pdfLabel to English
    new_fm = re.sub(r'pdfLabel: ".*?"', 'pdfLabel: "Download PDF documentation"', new_fm, count=1)

    out = f'---{new_fm}---\n\n{body}\n'
    md_path.write_text(out, encoding='utf-8')
    print(f'  OK {uid}: {len(body)} char body, {len(meta_lines)} meta fields')


for uid, pdf_name in WITH_EN_PDF:
    pdf_path = PDFS / pdf_name
    if not pdf_path.exists():
        print(f'  ! brak PDF {pdf_name}')
        continue
    print(f'\n-- {uid}')
    parsed = parse_pdf_page_en(pdf_path)
    print(f'   metadata: {list(parsed["fields"].keys())}')
    print(f'   description: {parsed["description"][:100]}...')
    update_md(uid, parsed)
