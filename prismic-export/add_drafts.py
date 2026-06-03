"""Dodaj szkice opisow do 9 eksponatow z generic PDF KRS-3.

Szkice na podstawie tytulu + analizy wizualnej zdjecia + obecnej metadata
Prismic. Kazdy oznaczony jako [SZKIC] - do weryfikacji przez dr Skonieczko
lub innego eksperta tribal art.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

EXHIBITS = Path(__file__).parent.parent / 'content' / 'exhibits'

NOTE = "*[SZKIC — opis wstępny, sporządzony na podstawie analizy wizualnej obiektu i jego ogólnego kontekstu kulturowego. Wymaga weryfikacji przez eksperta sztuki afrykańskiej; pełna karta katalogowa zostanie sporządzona w odrębnej dokumentacji KRS.]*"

DRAFTS = {
    'maska-ciala-gelede': {
        'metadata': [
            ('Pochodzenie', 'Nigeria, Benin'),
            ('Lud/ grupa etniczna', 'Joruba (Yoruba)'),
            ('Materiał', 'Drewno, patyna naturalna, kaolin, pigmenty'),
            ('Technika', 'Rzeźbiarska, polichromia'),
            ('Wiek', 'około 1950 r.'),
        ],
        'body': """Maska należy do typu masek-kostiumów Gelede ludu Joruba, zachodniej Nigerii i sąsiednich części dzisiejszego Beninu. Odmiennie niż klasyczne maski Gelede noszone na głowie, jest to maska torsowa (maska ciała) — element kostiumu tancerza, mocowany na korpusie podczas widowiska Èfè/Gelede. Rzeźba przedstawia stylizowany tors kobiecy: zaznaczone piersi, brzuch oraz centralna, koliście rzeźbiona pępkowa rozeta z motywem krzyżowym — symbol życia, płodności i więzi pokoleniowej.

Widowisko Gelede służy uhonorowaniu Awọn Iya Wa — „naszych matek”: kobiet starszych, czcigodnych i tych obdarzonych mocą duchową (àjẹ́), traktowanych jako strażniczki równowagi społecznej. Maska ta, noszona w pierwszej części ceremonii, ucieleśnia samą obecność tej żeńskiej mocy. Resztki kaolinu (pemba), żółtych i czerwonych pigmentów świadczą o wielokrotnym używaniu obiektu w obrzędach. Tradycja Gelede została w 2001 r. wpisana na Listę Reprezentatywną Niematerialnego Dziedzictwa Kulturowego UNESCO.""",
    },
    'luba': {
        'metadata': [
            ('Pochodzenie', 'Demokratyczna Republika Konga'),
            ('Lud/ grupa etniczna', 'Luba / Luba Shankadi'),
            ('Materiał', 'Drewno, patyna naturalna, muszle kauri'),
            ('Technika', 'Rzeźbiarska, inkrustacja'),
            ('Wiek', 'około 1950 r.'),
        ],
        'body': """Statuetka kobieca w kanonie sztuki Luba z południowo-wschodniego Konga (region Katanga). Rzeźba prezentuje charakterystyczny dla podgrupy Luba Shankadi typ wysokiej, kunsztownej fryzury („kaskadowa korona”), będącej atrybutem kobiet wysokiego statusu — żon i krewnych mulopwe (króla świętego). Oczy inkrustowane muszlami kauri (cowries) podkreślają funkcję rytualną figury: kauri w kulturze Luba symbolizują zarówno żeńskość, jak i duchowy wzrok wieszczki.

Postać wykonuje gest objęcia piersi — w sztuce Luba odczytywany jako wyraz pielęgnacji wiedzy królewskiej (bumfumu) oraz pokrewieństwa z duchami przodków. Drobne skaryfikacje na brzuchu i biodrach to zapis estetyki ciała oraz mapa identyfikacji klanowej. Tego typu figury pełniły funkcję mboko (naczyń pamięci) lub kabwelulu (podpórek dla dygnitarzy), towarzysząc inicjacjom bractwa Mbudye, strażników historii i prawa zwyczajowego Luba.""",
    },
    'lobala': {
        'metadata': [
            ('Pochodzenie', 'Demokratyczna Republika Konga, region Sud Ubangi, wioska Enyele'),
            ('Lud/ grupa etniczna', 'Lobala'),
            ('Materiał', 'Drewno, patyna naturalna'),
            ('Technika', 'Rzeźbiarska'),
            ('Wiek', 'przed 1950 r.'),
        ],
        'body': """Niewielka figura męska z warsztatu Lobala — niewielkiej grupy etnicznej z północno-zachodniej Demokratycznej Republiki Konga (region Sud-Ubangi), zamieszkującej dorzecze rzek Ubangi i Mongala. Sztuka Lobala, słabo opisana w literaturze, sytuuje się stylistycznie między tradycjami Ngombe, Ngbandi i Ngbaka — z silnym uproszczeniem brył, wydłużonymi proporcjami i zaakcentowanym układem pionowym.

Cechy charakterystyczne tej figury — głowa o stylizowanej fryzurze z przedziałkiem, podłużne, ledwie zarysowane oczy, ramiona przylegające do tułowia, lekko ugięte nogi — wskazują na funkcję ochronną, prawdopodobnie domową: tego typu obiekty Lobala stawiano w obejściach jako figurki opiekuńcze przodka rodu lub założyciela osady. Ciepły, jednolity ton patyny świadczy o długim okresie używania.""",
    },
    'maska': {
        'metadata': [
            ('Pochodzenie', 'Demokratyczna Republika Konga, region Sud Ubangi, wioska Enyele'),
            ('Lud/ grupa etniczna', 'Lobala'),
            ('Materiał', 'Drewno, kaolin, pigmenty'),
            ('Technika', 'Rzeźbiarska, polichromia'),
            ('Wiek', 'przed 1950 r.'),
        ],
        'body': """Owalna maska twarzowa ludu Lobala o silnie ekspresyjnej formie. Dominującym elementem są wielkie, koncentryczne okręgi otaczające otwory oczu — motyw określany w literaturze jako „oczy żaby” lub „oczy ducha” — wspólny dla wielu tradycji dorzecza Ubangi (Ngbandi, Ngbaka, Lobala). Wyniosły, ząbkowany grzebień biegnący od czoła ku tyłowi głowy stanowi schematyzację fryzury inicjacyjnej; szerokie nozdrza, otwarte usta i zaakcentowane uszy uzupełniają wyraz transu rytualnego.

Powierzchnia maski jest pokryta gęstym wzorem białych, kaolinowych kropek oraz linii — to ślad ceremonii inicjacyjnych młodzieńców (libwa) lub obrzędu pogrzebowego dygnitarza, w którym kaolin (mpemba) reprezentuje świat przodków, biel duchową obecność i czystość. Mocno startą polichromię i głębokie spękania drewna należy interpretować jako dowód intensywnego, wielopokoleniowego użytkowania.""",
    },
    'fetysz-gwozdziowy': {
        'metadata': [
            ('Pochodzenie', 'Demokratyczna Republika Konga, region Sud Ubangi, wioska Enyele'),
            ('Lud/ grupa etniczna', 'Lobala (tradycja minkisi)'),
            ('Materiał', 'Drewno, gwoździe i okucia żelazne, kaolin, pigmenty, materia rytualna'),
            ('Technika', 'Rzeźbiarska, asamblaż, „aktywacja” gwoździami'),
            ('Wiek', 'przed 1950 r.'),
        ],
        'body': """Figura męska typu nkisi nkondi — fetysza mocy znanego z tradycji ludów dolnego Konga (Yombe, Vili, Woyo, Kongo), a podejmowanego również przez sąsiednie społeczności dorzecza Ubangi. Twarz pokryta kaolinem (mpemba) — bielą świata przodków, z mocno zarysowanymi otwartymi ustami ukazującymi zęby (gest mowy wyroku). Uniesiona prawa ręka trzyma resztkę dawnego atrybutu — najprawdopodobniej noża, włóczni lub rogu antylopy — symbolu wykonującego decyzję nganga (kapłana).

Liczne gwoździe, okucia i fragmenty żelaza wbite w tors stanowią materialny zapis kolejnych „aktywacji” figury: każdy gwóźdź to pieczętowanie umowy, klątwy, leczenia lub zaprzysiężenia, pieczętowane przez kapłana w obecności obu stron sporu. Brzuch figury (mooyo) zawiera ślady kapsuły z bishimba — substancji medycznych łączących figurę ze światem duchowym. Obiekt łączy funkcję sędziowską, leczniczą i ochronną.""",
    },
    'fetysz-gwozdziowy-2': {
        'metadata': [
            ('Pochodzenie', 'Demokratyczna Republika Konga, region Sud Ubangi, wioska Enyele'),
            ('Lud/ grupa etniczna', 'Lobala (tradycja minkisi)'),
            ('Materiał', 'Drewno, gwoździe żelazne, tkanina, sznur, lusterko, kaolin, materia rytualna'),
            ('Technika', 'Rzeźbiarska, asamblaż, mocowanie reliquaire'),
            ('Wiek', 'przed 1950 r.'),
        ],
        'body': """Druga z figur typu nkisi w kolekcji — wariant „opakowany”, w którym tułów rzeźby został owinięty tkaniną i sznurem, tworząc rytualną „skórę” obiektu. Na piersi widnieje lustrzane okienko — typowy element bilongo: zwierciadło ma zatrzymywać zły wzrok i pozwalać duchowi zamieszkującemu figurę „widzieć” intencje zwracających się do niego ludzi. Małe woreczki i pakieciki przymocowane do korpusu zawierają substancje medyczne (zioła, ziemię z grobu, włosy) — personalne nośniki sił, którymi nganga zarządzał w imieniu wspólnoty.

Twarz wyraźnie wyrzeźbiona z otwartymi ustami i kanciastymi rysami, oczy podkreślone bielą — kanon ekspresji minkisi „mówiących”. Liczne kute gwoździe oraz haki wbite w korpus to zapis spraw rozstrzygniętych z udziałem tej figury. Tego typu obiekty w pełnym, niezdekonstruowanym stanie należą do najrzadszych świadectw rytualnej praktyki minkisi i są szczególnie cenione w kolekcjach muzealnych (porównywalne pozycje w British Museum, MRAC Tervuren, Quai Branly).""",
    },
    'pochwa-na-miecz': {
        'metadata': [
            ('Pochodzenie', 'Afryka Centralna (prawdopodobnie dorzecze Konga)'),
            ('Lud/ grupa etniczna', 'do weryfikacji'),
            ('Materiał', 'Włókna roślinne, muszelki kauri (cowries), paciorki szklane, tkanina, skóra'),
            ('Technika', 'Plecionkarska, koraliczna, aplikacja'),
            ('Wiek', '1. połowa XX w.'),
        ],
        'body': """Ceremonialna pochwa na miecz lub krótki nóż prestiżowy, wykonana w technice plecionki włókien roślinnych z bogatym wykończeniem z muszelek kauri (cowries), szklanych paciorków oraz aplikacji tekstylnych w żywych barwach (czerwień, ochra, czerń). Forma trójdzielna: prostokątna „głowa” z aplikacją figuralną, środkowy korpus o regularnym wzorze geometrycznym oraz dolna frędzla z plecionych warkoczy zwieńczonych kauri.

Tego rodzaju obiekty pełniły funkcję insygnium władzy lub statusu — noszone w pasie lub zawieszane na ramieniu podczas durbarów, ceremonii inicjacyjnych i pogrzebów dygnitarzy. Muszle kauri, dawne medium wymiany w głębi Afryki, łączyły wartość ekonomiczną z symboliką żeńskiej płodności i ochrony przed urokami. Geometryczne triangle wpisane w pole środkowe są często odczytywane jako schematyczne przedstawienia kobiecego łona oraz oka.

**Konieczna identyfikacja regionalna** — analogie wskazują na tradycje Yaka, Suku, Lulua lub Pende (dorzecze Kasai/Kwango).""",
    },
    'miecz': {
        'metadata': [
            ('Pochodzenie', 'Afryka Centralna (prawdopodobnie dorzecze Konga)'),
            ('Lud/ grupa etniczna', 'do weryfikacji'),
            ('Materiał', 'Żelazo kute, drewno, włókna roślinne'),
            ('Technika', 'Kowalska, rzeźbiarska, oplot'),
            ('Wiek', '1. połowa XX w.'),
        ],
        'body': """Ceremonialny miecz krótki o smukłej, jednosiecznej kutej klindze z geometrycznym rytem powierzchniowym. Rękojeść wieloczęściowa: dolna część walcowata, opleciona włóknem roślinnym, środkowy łącznik kwadratowy z wbitymi guzami metalowymi (krzyżowy znak być może liturgiczny lub klanowy), zakończenie gładkim, polerowanym grzybkiem. Pomiędzy rękojeścią a głownią charakterystyczny czworokątny węzeł („sucharek”) — element zdobniczy i konstrukcyjny zarazem.

Tego typu broń krótka — wyraźnie nie funkcjonalna bojowo — pełniła rolę insygnium dygnitarskiego lub przedmiotu obrzędowego (przysięga, ofiara, ścięcie ofiarne). Geometryczne nacięcia na klindze przypominają tradycje kowali-rzeźbiarzy Mangbetu, Ngbandi, Bua czy Songye; precyzyjna identyfikacja wymaga porównania z atlasami broni kongijskiej (Westerdijk 1988, Felix 2003).

**Identyfikacja regionalna do potwierdzenia.**""",
    },
    'miecz-2': {
        'metadata': [
            ('Pochodzenie', 'Afryka Centralna (prawdopodobnie dorzecze Konga)'),
            ('Lud/ grupa etniczna', 'do weryfikacji'),
            ('Materiał', 'Żelazo kute, drewno, włókna roślinne'),
            ('Technika', 'Kowalska, oplot, ryt'),
            ('Wiek', '1. połowa XX w.'),
        ],
        'body': """Drugi miecz ceremonialny z tej samej rodziny typologicznej — o dłuższej, jednorodnej klindze i podobnej budowie rękojeści (oplot włóknem, kwadratowy łącznik z metalowymi guzami). Powierzchnia głowni pokryta gęstym, rybokościowym („jodełkowym”) rytem dekoracyjnym, typowym dla tradycji kowalskich centralnego Konga — wzór jest zarówno ozdobą, jak i właściwością chłodzącą krew ofiarną podczas obrzędów ofiarniczych.

Stan zachowania bardzo dobry; powierzchnia żelaza z naturalną, ciemną patyną. Ostre, regularne nacięcia świadczą o pracy doświadczonego kowala — w kulturach kongijskich kowal (mfumu ya muanga) zajmował pozycję równorzędną z kapłanem, łącząc dziedzinę techniki z religią. Para mieczy (ten i poprzedni) sugeruje pochodzenie z jednego warsztatu lub jednej tradycji — para insygniów dygnitarskich była standardem ceremonialnym (jeden dla siebie, drugi dla syna lub zastępcy).

**Identyfikacja regionalna do potwierdzenia.**""",
    },
}


def update_md(uid: str, data: dict) -> None:
    md_path = EXHIBITS / f'{uid}_pl.md'
    if not md_path.exists():
        print(f'  ! brak {md_path.name}')
        return

    raw = md_path.read_text(encoding='utf-8')
    parts = raw.split('---', 2)
    if len(parts) < 3:
        print(f'  ! zly format {uid}')
        return

    fm_text = parts[1]
    meta_lines = [f'{label}: {value}' for label, value in data['metadata']]
    new_metadata_block = '\n'.join(meta_lines)

    new_fm = re.sub(
        r'(metadata:\s*\|)(.*?)(?=\n[a-zA-Z_]+:|\Z)',
        lambda m: 'metadata: |\n' + '\n'.join(f'  {l}' for l in new_metadata_block.split('\n')) + '\n',
        fm_text,
        count=1,
        flags=re.DOTALL,
    )
    if not new_fm.endswith('\n'):
        new_fm += '\n'

    body = data['body'] + '\n\n' + NOTE
    out = f'---{new_fm}---\n\n{body}\n'
    md_path.write_text(out, encoding='utf-8')
    print(f'  OK {uid}: {len(body)} char body, {len(meta_lines)} meta fields')


for uid, data in DRAFTS.items():
    print(f'\n-- {uid}')
    update_md(uid, data)
