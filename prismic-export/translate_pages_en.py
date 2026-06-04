"""Tlumaczenia stron statycznych EN (o-galerii, tworcy-galerii, kontakt)."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PAGES = Path(__file__).parent.parent / 'content' / 'pages'

# o-galerii: slice 2 (text oneColumnCentered) ma 1 heading1 + 4 paragraphs
O_GALERII_TEXT = [
    {"type": "heading1", "text": "African Art Gallery", "spans": [], "direction": "ltr"},
    {"type": "paragraph", "text":
        "African Art Gallery — the collection of Joanna and Ryszard Stolarski — is a space created out of "
        "passion, knowledge, and deep respect for African cultural heritage. Its beginnings trace back to the "
        "meeting of Ryszard Stolarski, a collector and art enthusiast, with the distinguished tribal art dealer "
        "Rudi Steinemann, who ran a tribal art gallery in Wiesbaden. That was the start of a journey that today "
        "leads to one of the most fascinating private collections of African art in Poland.",
        "spans": [], "direction": "ltr"},
    {"type": "paragraph", "text":
        "The collection currently comprises more than 200 carefully selected objects originating primarily from "
        "West and Central Africa. Each piece was acquired with attention not only to provenance and aesthetic "
        "merit, but also to its state of preservation and research potential. The exhibits include sculptures, "
        "masks, and ritual artefacts — drawn from both historic private collections and museum holdings from "
        "around the world.",
        "spans": [], "direction": "ltr"},
    {"type": "paragraph", "text":
        "The uniqueness of the gallery's holdings lies not only in their diversity but also in their meticulous "
        "documentation. Every object has its own inventory card, history, name, and attribution — often "
        "established through field research. All objects have been professionally described, photographed, and "
        "conserved. The collection is under the continuous care of distinguished specialists in art history "
        "and conservation, as well as experienced museum curators, ensuring the highest scholarly and ethical "
        "standards.",
        "spans": [], "direction": "ltr"},
    {"type": "paragraph", "text":
        "African Art Gallery is more than a collection — it is a living testimony to history, culture, and "
        "spirituality. It is a space that inspires, educates, and provokes reflection on the significance of "
        "African art within the context of universal cultural values.",
        "spans": [], "direction": "ltr"},
]


def update_text_slice(file_name: str, slice_idx: int, new_text: list) -> None:
    fp = PAGES / file_name
    with open(fp, 'r', encoding='utf-8') as f:
        d = json.load(f)
    d['slices'][slice_idx]['primary']['text'] = new_text
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f'  OK {file_name} slice {slice_idx}: {len(new_text)} blocks')


print('=== o-galerii_en-us.json ===')
update_text_slice('o-galerii_en-us.json', 2, O_GALERII_TEXT)


# Sprawdz tworcy-galerii i kontakt EN — ile slice'ow + co tam
for fn in ('tworcy-galerii_en-us.json', 'kontakt_en-us.json'):
    print(f'\n=== Inspect: {fn} ===')
    with open(PAGES / fn, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for i, sl in enumerate(d.get('slices', [])):
        p = sl.get('primary', {})
        for k, v in p.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and 'text' in v[0]:
                txt = '\n'.join(b.get('text','')[:80] for b in v)
                print(f' slice {i} ({sl.get("slice_type")}) {k}: \"{txt[:120]}...\"')
            elif isinstance(v, str) and v:
                print(f' slice {i} ({sl.get("slice_type")}) {k}: \"{v[:80]}\"')
