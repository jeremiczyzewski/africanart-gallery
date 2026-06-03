"""Wyciag opisy z PDF KRS dla 18 eksponatow z duplicatem 'Wolnostojacy...' (bug Lefem).

Parsuje pierwsza strone (PL) kazdego unikalnego PDF i podstawia tresc do markdownow.
Eksponaty ktore maja generic PDF KRS-3 (Lefem default) zostawia z nota - nie da sie
poprawic bez nowych zrodel.
"""
import fitz  # PyMuPDF
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
EXHIBITS = ROOT / 'content' / 'exhibits'
PDFS = ROOT / 'public' / 'uploads' / 'pdfs'

# Lista eksponatow z bugiem: (uid, pdf_filename)
# 9 z unikalnym PDF (KRS22/25/27/33/68/78/81/90/94)
# 9 z generic KRS-3 (wspolny z Lefem) -> nie da sie
BUG_EXHIBITS = [
    ('beben-szczelinowy',           'aNppDZ5xUNkB1NyJ_KRS22opispelnydopobraniaPL_ENG.pdf'),
    ('chamba',                       'aNppCJ5xUNkB1NyE_KRS78opispelnydopobraniaPL_ENG.pdf'),
    ('meski-fetysz-mocy-bitekibuti', 'aNppDJ5xUNkB1NyI_KRS25opispelnydopobraniaPL_ENG.pdf'),
    ('mbulu-ngulu-relikwiarz-meski', 'aNppCZ5xUNkB1NyF_KRS68opispelnydopobraniaPL_ENG.pdf'),
    ('ngil',                         'aNppBp5xUNkB1NyC_KRS90opispelnydopobraniaPL_ENG.pdf'),
    ('nkishi-nkondi',                'aNppC55xUNkB1NyH_KRS27opispelnydopobraniaPL_ENG.pdf'),
    ('takangledeangle-2',            'aNppC55xUNkB1NyG_KRS33opispelnydopobraniaPL_ENG.pdf'),
    ('troh',                         'aNppB55xUNkB1NyD_KRS81opispelnydopobraniaPL_ENG.pdf'),
    ('troh-2',                       'aNppBZ5xUNkB1NyB_KRS94opispelnydopobraniaPL_ENG.pdf'),
]
# Z generic KRS-3 PDF (wspolny z Lefem)
GENERIC_PDF_EXHIBITS = [
    'maska-ciala-gelede', 'fetysz-gwozdziowy-2', 'pochwa-na-miecz',
    'luba', 'fetysz-gwozdziowy', 'miecz', 'lobala', 'maska', 'miecz-2',
]


def parse_pdf_page1(pdf_path: Path) -> dict:
    """Wyciag z 1. strony (PL): metadata fields + opis + provenance."""
    doc = fitz.open(pdf_path)
    text = doc[0].get_text("text")
    doc.close()

    lines = [l.rstrip() for l in text.split('\n')]
    # Pomin header (Kolekcja..., Eksponat KSR..., Nazwa - ...)
    # Pola metadata format: "Pole - wartosc" lub "Pole – wartosc"
    # Konczy sie pierwsza pusta linia LUB pierwszym dlugim akapitem opisu

    META_KEYS = ['Pochodzenie', 'Lud/grupa etniczna', 'Lud / grupa etniczna',
                 'Materiał', 'Material', 'Technika',
                 'Wysokość', 'Wysokosc', 'Wiek', 'Wymiary', 'Średnica', 'Srednica',
                 'Długość', 'Dlugosc', 'Szerokość', 'Szerokosc']

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

        # Wykryj zmiane sekcji
        if l.startswith('Opracowanie'):
            if desc_buffer:
                description_lines.append(' '.join(desc_buffer))
                desc_buffer = []
            section = 'opracowanie'
            continue
        if l.startswith('Historia') or l.startswith('Prowieniencja') or l.startswith('Proweniencja'):
            section = 'provenance'
            continue
        # Linie naglowkowe (skip, ale NIE zmieniaj section)
        if l.startswith('Kolekcja Joanny') \
           or l.startswith('Eksponat KSR') or l.startswith('Eksponat KRS') \
           or l.startswith('Nazwa') or l.startswith('African Art'):
            continue
        # Linie copyright/stopka -> koniec parsowania, reszta linii skip
        is_footer = (
            l.startswith('info@') or l.startswith('©')
            or 'przechowywana w systemach' in l
            or l.startswith('Cytowanie kr')
            or 'wszelkie prawa zastrzeżone' in l.lower()
        )
        if is_footer:
            if section == 'description' and desc_buffer:
                description_lines.append(' '.join(desc_buffer))
                desc_buffer = []
            section = 'footer'
            continue
        if section == 'footer':
            continue

        # Sprawdz czy to pole metadata
        is_meta_field = False
        for key in META_KEYS:
            # Format: "Pole - wartosc" lub "Pole – wartosc" (rozne mysliniki)
            m = re.match(rf'^{re.escape(key)}\s*[-–—]\s*(.+)$', l)
            if m:
                fields[key] = m.group(1).strip()
                is_meta_field = True
                break
        if is_meta_field:
            section = 'meta'
            continue

        # Inaczej: opis lub provenance
        if section in ('header', 'meta'):
            section = 'description'
        if section == 'description':
            desc_buffer.append(l)
        elif section == 'provenance':
            provenance_lines.append(l)

    # Flush
    if desc_buffer:
        description_lines.append(' '.join(desc_buffer))

    description = '\n\n'.join(description_lines).strip()
    provenance = '\n'.join(provenance_lines).strip()

    return {
        'fields': fields,
        'description': description,
        'provenance': provenance,
    }


def yaml_escape(s: str) -> str:
    if s is None:
        return ''
    return str(s).replace('\\', '\\\\').replace('"', '\\"')


def update_markdown(uid: str, parsed: dict) -> None:
    """Zaktualizuj markdown dla danego eksponata: metadata fields + body."""
    md_path = EXHIBITS / f'{uid}_pl.md'
    if not md_path.exists():
        print(f'  ! brak {md_path.name}')
        return

    raw = md_path.read_text(encoding='utf-8')
    # Parse frontmatter manualnie (bo gray-matter nie mam w Pythonie)
    parts = raw.split('---', 2)
    if len(parts) < 3:
        print(f'  ! zly format frontmatter {uid}')
        return

    fm_text = parts[1]
    fields = parsed['fields']

    # Buduj nowe metadata jako multi-line string YAML
    meta_lines = []
    # Kanoniczne pola w stalej kolejnosci
    canonical = [
        ('Pochodzenie',         fields.get('Pochodzenie')),
        ('Lud/ grupa etniczna', fields.get('Lud/grupa etniczna') or fields.get('Lud / grupa etniczna')),
        ('Materiał',            fields.get('Materiał') or fields.get('Material')),
        ('Technika',            fields.get('Technika')),
        ('Wysokość',            fields.get('Wysokość') or fields.get('Wysokosc')),
        ('Wymiary',             fields.get('Wymiary')),
        ('Średnica',            fields.get('Średnica') or fields.get('Srednica')),
        ('Długość',             fields.get('Długość') or fields.get('Dlugosc')),
        ('Szerokość',           fields.get('Szerokość') or fields.get('Szerokosc')),
        ('Wiek',                fields.get('Wiek')),
    ]
    for label, value in canonical:
        if value:
            meta_lines.append(f'{label}: {value}')
    new_metadata_block = '\n'.join(meta_lines)

    # Zaktualizuj frontmatter — zamien stary `metadata: |` blok na nowy
    # Stary format: `metadata: |` + linie ze spacja na poczatku do konca frontmatter
    # WAZNE: konczy sie newline'em (zeby nie skleic z ---)
    new_fm = re.sub(
        r'(metadata:\s*\|)(.*?)(?=\n[a-zA-Z_]+:|\Z)',
        lambda m: 'metadata: |\n' + '\n'.join(f'  {l}' for l in new_metadata_block.split('\n')) + '\n',
        fm_text,
        count=1,
        flags=re.DOTALL,
    )
    # Zapewnij ze frontmatter konczy sie newline'em zanim zostanie zamkniety
    if not new_fm.endswith('\n'):
        new_fm += '\n'

    # Build nowy plik
    body = parsed['description']
    if parsed.get('provenance'):
        body += '\n\n**Historia / Proweniencja:**\n\n' + parsed['provenance']

    out = f'---{new_fm}---\n\n{body}\n'
    md_path.write_text(out, encoding='utf-8')
    print(f'  OK {uid}: {len(body)} char body, {len(meta_lines)} meta fields')


def main():
    print('=== UNIKALNE PDF (9 eksponatow) ===')
    for uid, pdf_name in BUG_EXHIBITS:
        pdf_path = PDFS / pdf_name
        if not pdf_path.exists():
            print(f'  ! brak PDF {pdf_name}')
            continue
        print(f'\n-- {uid} ({pdf_name[:50]})')
        parsed = parse_pdf_page1(pdf_path)
        print(f'   metadata: {list(parsed["fields"].keys())}')
        print(f'   description: {parsed["description"][:100]}...')
        update_markdown(uid, parsed)

    print(f'\n=== GENERIC PDF KRS-3 ({len(GENERIC_PDF_EXHIBITS)} eksponatow) ===')
    print('Te eksponaty maja wspolny PDF KRS-3 (default Lefem) — nie da sie poprawic z PDF.')
    print('Wymagaja recznych poprawek przez Sveltia CMS lub innego zrodla.')
    for uid in GENERIC_PDF_EXHIBITS:
        # Zostawmy bez zmian — nic nie ma do zaoferowania
        print(f'  - {uid}')


if __name__ == '__main__':
    main()
