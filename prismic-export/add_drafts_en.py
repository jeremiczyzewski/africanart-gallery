"""EN tlumaczenia 9 szkicow + Lefem (brak EN w PDF KRS-3).

Tlumaczone z polskich oryginalow (szkice + Lefem-Prismic). Lefem ma faktyczny
opis klienta po polsku w EN markdown - tlumaczy sie tutaj.
Pozostale 9 szkicow oznaczone notą [DRAFT - subject to expert review].
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

EXHIBITS = Path(__file__).parent.parent / 'content' / 'exhibits'

DRAFT_NOTE = "*[DRAFT — preliminary description based on visual analysis of the object and its general cultural context. Subject to verification by an expert in African art; the full catalog entry will be prepared in separate KRS documentation.]*"

ENTRIES = {
    'lefem': {
        'title': 'Lefem',
        'metadata': [
            ('Origin', 'Cameroon, Bangwa Region'),
            ('People/Ethnic Group', 'Bangwa, Bamileke (Grasslands)'),
            ('Material', 'Wood, natural patina'),
            ('Technique', 'Sculptural'),
            ('Age', 'circa 1950'),
        ],
        'body': """Lefem figures are crafted as important testaments to dynastic lines of power. During the ceremonies accompanying the chief's funeral and the enthronement of his successor, his lefem is publicly displayed to maintain social and political continuity, and to strengthen belief in the power of the royal ancestral authority.""",
        'note': False,
    },
    'maska-ciala-gelede': {
        'title': 'Gelede Body Mask',
        'metadata': [
            ('Origin', 'Nigeria, Benin'),
            ('People/Ethnic Group', 'Yoruba'),
            ('Material', 'Wood, natural patina, kaolin, pigments'),
            ('Technique', 'Sculptural, polychromy'),
            ('Age', 'circa 1950'),
        ],
        'body': """This mask belongs to the Gelede costume-mask type of the Yoruba people of western Nigeria and adjacent regions of present-day Benin. Unlike classic Gelede masks worn on the head, this is a torso mask ("body mask") — a costume element fitted to the dancer's body during the Èfè/Gelede performance. The carving represents a stylised female torso: marked breasts, abdomen, and a central, circularly carved navel rosette with a cruciform motif — a symbol of life, fertility, and intergenerational continuity.

The Gelede spectacle honours Awọn Iya Wa — "our mothers": elder, venerable women and those endowed with spiritual power (àjẹ́), regarded as guardians of social balance. This mask, worn in the first part of the ceremony, embodies the very presence of that feminine power. Traces of kaolin (pemba), yellow, and red pigments testify to repeated ritual use. In 2001 the Gelede tradition was inscribed on the UNESCO Representative List of the Intangible Cultural Heritage of Humanity.""",
        'note': True,
    },
    'luba': {
        'title': 'Luba',
        'metadata': [
            ('Origin', 'Democratic Republic of the Congo'),
            ('People/Ethnic Group', 'Luba / Luba Shankadi'),
            ('Material', 'Wood, natural patina, cowrie shells'),
            ('Technique', 'Sculptural, inlay'),
            ('Age', 'circa 1950'),
        ],
        'body': """A female statuette in the canon of Luba art from south-eastern Congo (Katanga region). The figure displays the characteristic high, elaborate "cascading crown" hairstyle of the Luba Shankadi subgroup, an attribute of high-status women — wives and relatives of the mulopwe (sacred king). The eyes inlaid with cowrie shells underscore the figure's ritual function: cowries in Luba culture symbolise both femininity and the spiritual vision of the seer.

The figure performs the gesture of embracing the breasts — in Luba art interpreted as an expression of the nurture of royal knowledge (bumfumu) and of kinship with the ancestral spirits. The fine scarifications on the abdomen and hips record both bodily aesthetics and clan identification. Figures of this type served as mboko (memory vessels) or kabwelulu (supports for dignitaries), accompanying the initiations of the Mbudye fraternity — guardians of Luba historical and customary law.""",
        'note': True,
    },
    'lobala': {
        'title': 'Lobala',
        'metadata': [
            ('Origin', 'Democratic Republic of the Congo, Sud-Ubangi Region, Enyele village'),
            ('People/Ethnic Group', 'Lobala'),
            ('Material', 'Wood, natural patina'),
            ('Technique', 'Sculptural'),
            ('Age', 'before 1950'),
        ],
        'body': """A small male figure from the Lobala workshop — a small ethnic group of north-western Democratic Republic of the Congo (Sud-Ubangi region), inhabiting the basins of the Ubangi and Mongala rivers. Lobala art, sparsely documented in the literature, sits stylistically between the Ngombe, Ngbandi, and Ngbaka traditions — with strong simplification of mass, elongated proportions, and a pronounced vertical orientation.

The characteristic features of this figure — head with a stylised parted hairstyle, narrow, barely outlined eyes, arms held against the torso, slightly bent legs — point to a protective, most likely domestic function: such Lobala objects were placed in household compounds as protective figures of an ancestor of the lineage or founder of the village. The warm, uniform tone of the patina testifies to a long period of use.""",
        'note': True,
    },
    'maska': {
        'title': 'Lobala Face Mask',
        'metadata': [
            ('Origin', 'Democratic Republic of the Congo, Sud-Ubangi Region, Enyele village'),
            ('People/Ethnic Group', 'Lobala'),
            ('Material', 'Wood, kaolin, pigments'),
            ('Technique', 'Sculptural, polychromy'),
            ('Age', 'before 1950'),
        ],
        'body': """An oval face mask of the Lobala people of strongly expressive form. The dominant element is the great concentric circles framing the eye openings — a motif described in the literature as "frog eyes" or "spirit eyes" — shared by many traditions of the Ubangi basin (Ngbandi, Ngbaka, Lobala). The lofty, serrated crest running from the forehead to the back of the head schematises an initiation hairstyle; broad nostrils, an open mouth, and prominent ears complete the expression of ritual trance.

The mask's surface is covered with a dense pattern of white kaolin dots and lines — a trace of male initiation ceremonies (libwa) or of the funerary rite of a dignitary, in which kaolin (mpemba) represents the world of the ancestors, the white standing for spiritual presence and purity. The heavily worn polychromy and deep cracks in the wood should be interpreted as evidence of intensive, multigenerational use.""",
        'note': True,
    },
    'fetysz-gwozdziowy': {
        'title': 'Nail Fetish (Nkisi Nkondi)',
        'metadata': [
            ('Origin', 'Democratic Republic of the Congo, Sud-Ubangi Region, Enyele village'),
            ('People/Ethnic Group', 'Lobala (minkisi tradition)'),
            ('Material', 'Wood, iron nails and fittings, kaolin, pigments, ritual matter'),
            ('Technique', 'Sculptural, assemblage, "activation" with nails'),
            ('Age', 'before 1950'),
        ],
        'body': """A male figure of the nkisi nkondi type — a power fetish known from the traditions of the peoples of the Lower Congo (Yombe, Vili, Woyo, Kongo) and also adopted by neighbouring communities of the Ubangi basin. The face is covered with kaolin (mpemba) — the white of the ancestral world — with a strongly marked open mouth revealing the teeth (the gesture of pronouncing judgment). The raised right hand holds the remnant of a former attribute — most likely a knife, spear, or antelope horn — the symbol of the executor of the nganga's (priest's) decision.

The numerous nails, fittings, and iron fragments driven into the torso form a material record of successive "activations" of the figure: each nail is the sealing of an agreement, a curse, a healing, or a sworn oath, sealed by the priest in the presence of both parties to the dispute. The figure's abdomen (mooyo) contains traces of a capsule with bishimba — medicinal substances connecting the figure to the spirit world. The object combines the functions of judge, healer, and protector.""",
        'note': True,
    },
    'fetysz-gwozdziowy-2': {
        'title': 'Nail Fetish with Mirror (Nkisi Nkondi)',
        'metadata': [
            ('Origin', 'Democratic Republic of the Congo, Sud-Ubangi Region, Enyele village'),
            ('People/Ethnic Group', 'Lobala (minkisi tradition)'),
            ('Material', 'Wood, iron nails, fabric, cord, mirror, kaolin, ritual matter'),
            ('Technique', 'Sculptural, assemblage, reliquary mounting'),
            ('Age', 'before 1950'),
        ],
        'body': """The second nkisi figure in the collection — a "wrapped" variant in which the torso of the sculpture has been bound in fabric and cord, forming a ritual "skin" for the object. On the chest is a mirror window — a typical bilongo element: the mirror is meant to deflect the evil eye and allow the spirit inhabiting the figure to "see" the intentions of those who address it. Small bundles and packets attached to the torso contain medicinal substances (herbs, earth from a grave, hair) — personal carriers of the powers that the nganga managed on behalf of the community.

A clearly carved face with an open mouth and angular features, eyes accented with white — the expressive canon of "speaking" minkisi. The numerous forged nails and hooks driven into the torso record matters decided with the figure's participation. Objects of this kind, in full undeconstructed condition, are among the rarest evidence of minkisi ritual practice and are particularly prized in museum collections (comparable items at the British Museum, MRAC Tervuren, Quai Branly).""",
        'note': True,
    },
    'pochwa-na-miecz': {
        'title': 'Sword Sheath',
        'metadata': [
            ('Origin', 'Central Africa (probably the Congo basin)'),
            ('People/Ethnic Group', 'to be verified'),
            ('Material', 'Plant fibres, cowrie shells, glass beads, fabric, leather'),
            ('Technique', 'Plaitwork, beadwork, appliqué'),
            ('Age', 'first half of the 20th century'),
        ],
        'body': """A ceremonial sheath for a sword or prestige short knife, executed in the technique of plant-fibre plaitwork with rich finishing of cowrie shells, glass beads, and textile appliqué in vivid colours (red, ochre, black). A tripartite form: rectangular "head" with a figurative appliqué, a middle body with a regular geometric pattern, and a lower fringe of plaited braids tipped with cowries.

Objects of this kind served as insignia of authority or status — worn at the waist or slung over the shoulder during durbars, initiations, and dignitary funerals. Cowrie shells, the ancient medium of exchange in the African interior, combined economic value with the symbolism of female fertility and protection from the evil eye. The geometric triangles inscribed in the central field are often read as schematic representations of the female womb and eye.

**Regional identification required** — analogies point to the Yaka, Suku, Lulua or Pende traditions (Kasai/Kwango basin).""",
        'note': True,
    },
    'miecz': {
        'title': 'Mbele (Ceremonial Sword)',
        'metadata': [
            ('Origin', 'Central Africa (probably the Congo basin)'),
            ('People/Ethnic Group', 'to be verified'),
            ('Material', 'Forged iron, wood, plant fibres'),
            ('Technique', 'Smithing, sculptural, binding'),
            ('Age', 'first half of the 20th century'),
        ],
        'body': """A short ceremonial sword with a slender, single-edged forged blade decorated with geometric surface engraving. A multi-part hilt: a cylindrical lower section wound with plant fibre, a square central connector with embedded metal studs (a cruciform sign, perhaps liturgical or clan), terminating in a smooth polished knob. Between hilt and blade is a characteristic quadrangular knot ("biscuit") — at once a decorative and a structural element.

This type of short weapon — clearly not functional in combat — served as a dignitary's insignia or a ritual object (oath, offering, ceremonial beheading). The geometric incisions on the blade recall the traditions of the smith-sculptors of the Mangbetu, Ngbandi, Bua, or Songye; a precise identification requires comparison with atlases of Congolese weaponry (Westerdijk 1988, Felix 2003).

**Regional identification to be confirmed.**""",
        'note': True,
    },
    'miecz-2': {
        'title': 'Mbele a Lulendo (Long Ceremonial Sword)',
        'metadata': [
            ('Origin', 'Central Africa (probably the Congo basin)'),
            ('People/Ethnic Group', 'to be verified'),
            ('Material', 'Forged iron, wood, plant fibres'),
            ('Technique', 'Smithing, binding, engraving'),
            ('Age', 'first half of the 20th century'),
        ],
        'body': """A second ceremonial sword of the same typological family — with a longer, uniform blade and similar hilt construction (fibre binding, square connector with metal studs). The blade's surface is covered with a dense, herringbone-pattern decorative engraving — typical of the smithing traditions of central Congo. The pattern is both ornamental and a property considered to cool the sacrificial blood during offering rites.

Excellent state of preservation; the iron surface bears a natural dark patina. The sharp, regular incisions testify to the work of an experienced smith — in Congolese cultures the smith (mfumu ya muanga) held a position equal to that of the priest, combining the domain of technique with religion. The pair of swords (this one and the previous) suggests an origin in a single workshop or tradition — a pair of dignitary insignia was a ceremonial standard (one for the holder, the other for his son or deputy).

**Regional identification to be confirmed.**""",
        'note': True,
    },
}


def update_md(uid: str, data: dict) -> None:
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

    # Update title + imageAlt
    fm_text = re.sub(r'^title: ".*?"$', f'title: "{data["title"]}"', fm_text, count=1, flags=re.M)
    fm_text = re.sub(r'^imageAlt: ".*?"$', f'imageAlt: "{data["title"]}"', fm_text, count=1, flags=re.M)
    # Update pdfLabel
    fm_text = re.sub(r'pdfLabel: ".*?"', 'pdfLabel: "Download PDF documentation"', fm_text, count=1)

    # Update metadata block
    meta_lines = [f'{label}: {value}' for label, value in data['metadata']]
    new_metadata_block = '\n'.join(meta_lines)
    new_fm = re.sub(
        r'(metadata:\s*\|)(.*?)(?=\n[a-zA-Z_]+:|\Z)',
        lambda m: 'metadata: |\n' + '\n'.join(f'  {l}' for l in new_metadata_block.split('\n')) + '\n',
        fm_text, count=1, flags=re.DOTALL,
    )
    if not new_fm.endswith('\n'):
        new_fm += '\n'

    body = data['body']
    if data.get('note'):
        body += '\n\n' + DRAFT_NOTE

    out = f'---{new_fm}---\n\n{body}\n'
    md_path.write_text(out, encoding='utf-8')
    print(f'  OK {uid}: {len(body)} char body, {len(meta_lines)} meta fields')


for uid, data in ENTRIES.items():
    print(f'\n-- {uid}')
    update_md(uid, data)
