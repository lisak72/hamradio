# -*- coding: utf-8 -*-
"""Příloha: radioamatérská pásma rozdělená podle druhů provozu (jen amatérská pásma, osa X = kmitočet).

generate() -> [(název, popisek, svg_bytes, šířka, výška)]
Každé pásmo má vlastní graf s lineární osou:
  • pruh „IARU R1“ – úseky podle plánů IARU Region 1: KV plán (platný od 16. 10. 2020, zdroje/iaru/IARU_R1_HF_bandplan.txt)
    a VHF Managers Handbook v10.03 (02/2026, zdroje/iaru/IARU_R1_VHF_Handbook_V10_03.txt); zjednodušeno do kategorií CAT,
    pásma jsou oříznuta na rozsah přílohy 1 vyhl. č. 156/2005 Sb. (6 m: 50–52 MHz, 9 cm: 3 400–3 410 MHz),
  • pruh „ČTÚ“ – úseky přesně podle odpovědí ČTÚ v otázkách provoz a) (odkaz a) n), mohou se lišit od plánu IARU,
  • značky nad pruhem = vybraná centra aktivity z plánu IARU,
  • u pásem s velmi úzkými úseky je pod grafem detail (ZOOM).
Hodnoty KV v kHz, ostatní v MHz.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obrazky_elek import F, TX
from spektrum_pasma import tw

TITLE = 'Příloha: Radioamatérská pásma podle druhů provozu'
INTRO = ('Grafy ukazují rozdělení každého radioamatérského pásma na úseky pro jednotlivé druhy provozu. Na ose X je '
         'kmitočet (každé pásmo má vlastní lineární měřítko; krátkovlnná pásma v kHz, ostatní v MHz). Horní pruh '
         '„IARU R1“ je zjednodušený plán pásem IARU Region 1 (KV plán platný od 16. 10. 2020, VKV a mikrovlny podle '
         'VHF Managers Handbook v10.03 z 02/2026), oříznutý na rozsah pásem podle přílohy 1 vyhl. č. 156/2005 Sb. '
         'Spodní pruh „ČTÚ“ ukazuje úseky přesně tak, jak je uvádějí odpovědi ČTÚ v otázkách Provoz a) – odkaz a) n '
         'je číslo otázky. Odpovědi ČTÚ se místy liší od aktuálního plánu IARU; pro zkoušku platí odpověď ČTÚ. Trojúhelníky '
         'nad pruhem označují vybraná centra aktivity (QRP = provoz malým výkonem, QRS = pomalá telegrafie, DV = digitální '
         'hlas, SSTV = přenos obrázků, nouzový = centrum aktivity pro nouzovou komunikaci). Pásma 630 m, 60 m a 4 m ve '
         'vyhlášce uvedena nejsou (čárkovaný rámeček). Plán IARU je doporučení – telegrafie (CW) je dovolena v celém '
         'pásmu kromě úseků pro majáky.')

# kategorie: (barva, barva textu, popis do legendy, krátké popisky do pruhu od nejdelšího)
CAT = {
    'cw':   ('#1565c0', '#ffffff', 'telegrafie (CW) – výhradně', ['CW']),
    'nb':   ('#f9a825', '#3e2a00', 'úzkopásmové provozy do 500 Hz – CW a digitální (RTTY, PSK, FT8…)',
             ['úzkopásmové', 'úzkopásm.', 'úzk.', 'Ú']),
    'dig':  ('#ffe082', '#3e2a00', 'všechny druhy, přednostně digitální provoz a data (na VKV např. APRS, paket)',
             ['digitální', 'digi', 'D']),
    'fone': ('#43a047', '#ffffff', 'všechny druhy do 2,7 kHz – FONE (SSB), CW, digitální', ['FONE (SSB)', 'FONE', 'F']),
    'fm':   ('#8e24aa', '#ffffff', 'FM a digitální hlas (DV) – simplex, převaděče', ['FM / DV', 'FM', 'FM']),
    'bcn':  ('#5d4037', '#ffffff', 'majáky (výhradně)', ['majáky', 'maj.', 'M']),
    'sat':  ('#00897b', '#ffffff', 'družicová služba', ['družice', 'druž.', 'S']),
    'atv':  ('#ef6c00', '#ffffff', 'televize ATV / DATV', ['ATV / DATV', 'ATV', 'TV']),
    'wide': ('#b0bec5', '#263238', 'všechny druhy provozu, i širokopásmové (bez omezení šířky)', ['všechny druhy', 'vše', 'V']),
    'gap':  ('#eeeeee', '#777777', 'ochranný úsek / nevyužito', ['']),
}
ORDER = ['cw', 'nb', 'dig', 'fone', 'fm', 'bcn', 'sat', 'atv', 'wide', 'gap']

# BANDS: (název, MHz pro titulek, jednotka, od, do, mimo vyhlášku?, [úseky IARU (od, do, kat)],
#         [úseky ČTÚ (od, do, kat, popisek, č. otázky provoz a)], [centra aktivity (kmitočet, popisek)], zoom (od, do) | [(od, do), …] | None,
#         poznámka do popisku)
BANDS = [
    ('2200 m', '0,136 MHz', 'kHz', 135.7, 137.8, False,
     [(135.7, 137.8, 'nb')], [], [], None,
     'Celé pásmo: CW, QRSS (velmi pomalá telegrafie) a úzkopásmové digitální provozy do 200 Hz.'),
    ('630 m', '0,47 MHz', 'kHz', 472, 479, True,
     [(472, 475, 'cw'), (475, 479, 'nb')], [], [], None,
     'Pásmo není ve vyhl. č. 156/2005 Sb.; rozdělení je podle IARU jen „navrhované využití“.'),
    ('160 m', '1,8 MHz', 'kHz', 1810, 2000, False,
     [(1810, 1838, 'cw'), (1838, 1840, 'nb'), (1840, 1843, 'dig'), (1843, 2000, 'fone')],
     [(1810, 1838, 'cw', 'CW', 3), (1838, 1843, 'nb', 'digi', 4), (1840, 2000, 'fone', 'FONE', 2)],
     [(1836, 'QRP CW')], None,
     'Nejnižší naladění pro LSB: 1 843 kHz. Podle vyhlášky je 1 850–2 000 kHz podružné pásmo s výkonem jen 10 W.'),
    ('80 m', '3,5 MHz', 'kHz', 3500, 3800, False,
     [(3500, 3570, 'cw'), (3570, 3600, 'nb'), (3600, 3620, 'dig'), (3620, 3800, 'fone')],
     [(3500, 3580, 'cw', 'CW', 7), (3500, 3510, 'cw', 'CW DX', 6), (3580, 3620, 'nb', 'digi', 8),
      (3600, 3800, 'fone', 'FONE', 5)],
     [(3510, 'CW DX'), (3555, 'QRS'), (3560, 'QRP CW'), (3630, 'DV'), (3690, 'QRP SSB'), (3735, 'SSTV'),
      (3760, 'nouzový')], None,
     'IARU: 3 500–3 510 kHz přednostně pro mezikontinentální provoz (DX); nejnižší naladění pro LSB 3 603 kHz.'),
    ('60 m', '5 MHz', 'kHz', 5351.5, 5366.5, True,
     [(5351.5, 5354, 'nb'), (5354, 5366, 'fone'), (5366, 5366.5, 'nb')], [], [], None,
     'Pásmo není ve vyhl. č. 156/2005 Sb. Pro fonii se zde doporučuje USB (nejvýše 5 363 kHz na stupnici). '
     '5 366–5 366,5 kHz: digitální provozy pro slabé signály do 20 Hz.'),
    ('40 m', '7 MHz', 'kHz', 7000, 7200, False,
     [(7000, 7040, 'cw'), (7040, 7050, 'nb'), (7050, 7060, 'dig'), (7060, 7200, 'fone')],
     [(7000, 7040, 'cw', 'CW', 10), (7040, 7060, 'nb', 'digi', 11), (7050, 7200, 'fone', 'FONE', 9)],
     [(7030, 'QRP CW'), (7070, 'DV'), (7090, 'QRP SSB'), (7110, 'nouzový'), (7165, 'SSTV')], None,
     'Nejnižší naladění pro LSB: 7 053 kHz.'),
    ('30 m', '10 MHz', 'kHz', 10100, 10150, False,
     [(10100, 10130, 'cw'), (10130, 10150, 'nb')],
     [(10140, 10150, 'nb', 'digi', 13)],
     [(10116, 'QRP CW')], None,
     'FONE provoz v pásmu 10 MHz není povolen [→ a) 12]. Pásmo WARC – nekonají se v něm závody.'),
    ('20 m', '14 MHz', 'kHz', 14000, 14350, False,
     [(14000, 14070, 'cw'), (14070, 14099, 'nb'), (14099, 14101, 'bcn'), (14101, 14112, 'dig'), (14112, 14350, 'fone')],
     [(14000, 14070, 'cw', 'CW', 14), (14070, 14099, 'nb', 'digi', 16), (14101, 14350, 'fone', 'FONE', 15)],
     [(14055, 'QRS'), (14060, 'QRP CW'), (14100, 'majáky NCDXF'), (14130, 'DV'), (14195, 'DX-expedice'),
      (14230, 'SSTV'), (14285, 'QRP SSB'), (14300, 'nouzový')], None,
     '14 099–14 101 kHz: mezinárodní síť majáků NCDXF/IARU. Nejvyšší naladění pro USB: 3 kHz pod horním okrajem pásma.'),
    ('17 m', '18 MHz', 'kHz', 18068, 18168, False,
     [(18068, 18095, 'cw'), (18095, 18109, 'nb'), (18109, 18111, 'bcn'), (18111, 18120, 'dig'), (18120, 18168, 'fone')],
     [(18068, 18095, 'cw', 'CW', 17), (18095, 18109, 'nb', 'digi', 19), (18111, 18168, 'fone', 'FONE', 18)],
     [(18086, 'QRP CW'), (18110, 'majáky'), (18130, 'QRP SSB'), (18150, 'DV'), (18160, 'nouzový')], None,
     'Pásmo WARC – nekonají se v něm závody.'),
    ('15 m', '21 MHz', 'kHz', 21000, 21450, False,
     [(21000, 21070, 'cw'), (21070, 21110, 'nb'), (21110, 21120, 'dig'), (21120, 21149, 'nb'), (21149, 21151, 'bcn'),
      (21151, 21450, 'fone')],
     [(21000, 21070, 'cw', 'CW', 20), (21070, 21120, 'nb', 'digi', 22), (21151, 21450, 'fone', 'FONE', 21)],
     [(21055, 'QRS'), (21060, 'QRP CW'), (21150, 'majáky'), (21180, 'DV'), (21285, 'QRP SSB'), (21340, 'SSTV'),
      (21360, 'nouzový')], None,
     'IARU: 21 125–21 450 kHz může využívat i družicová služba (přednostně nad 21 400 kHz).'),
    ('12 m', '24 MHz', 'kHz', 24890, 24990, False,
     [(24890, 24915, 'cw'), (24915, 24929, 'nb'), (24929, 24931, 'bcn'), (24931, 24940, 'dig'), (24940, 24990, 'fone')],
     [(24890, 24915, 'cw', 'CW', 24), (24915, 24929, 'nb', 'digi', 25), (24931, 24990, 'fone', 'FONE', 23)],
     [(24906, 'QRP CW'), (24930, 'majáky'), (24950, 'QRP SSB'), (24960, 'DV')], None,
     'Pásmo WARC – nekonají se v něm závody.'),
    ('10 m', '28 MHz', 'kHz', 28000, 29700, False,
     [(28000, 28070, 'cw'), (28070, 28190, 'nb'), (28190, 28225, 'bcn'), (28225, 28300, 'fone'), (28300, 28320, 'dig'),
      (28320, 29100, 'fone'), (29100, 29200, 'fm'), (29200, 29300, 'dig'), (29300, 29510, 'sat'), (29510, 29520, 'gap'),
      (29520, 29700, 'fm')],
     [(28000, 28070, 'cw', 'CW', 27), (28070, 28190, 'nb', 'digi', 28), (28225, 29300, 'fone', 'FONE', 26),
      (29300, 29510, 'sat', 'družice', 29)],
     [(28055, 'QRS'), (28060, 'QRP CW'), (28330, 'DV'), (28360, 'QRP SSB'), (28680, 'SSTV'), (29600, 'FM volací')], None,
     '28 190–28 225 kHz majáky; 29 100–29 200 kHz FM simplex (kanály po 10 kHz); 29 520–29 590 kHz vstupy a '
     '29 620–29 700 kHz výstupy FM převaděčů; 29 300–29 510 kHz družice.'),
    ('6 m', '50 MHz', 'MHz', 50, 52, False,
     [(50.0, 50.1, 'cw'), (50.1, 50.3, 'fone'), (50.3, 50.4, 'nb'), (50.4, 50.5, 'bcn'), (50.5, 50.7, 'dig'),
      (50.7, 50.9, 'fm'), (50.9, 51.2, 'wide'), (51.2, 51.4, 'fm'), (51.4, 51.6, 'fm'), (51.6, 51.8, 'wide'),
      (51.8, 52.0, 'fm')],
     [(50.0, 50.1, 'cw', 'CW', 32), (50.1, 52.0, 'fone', 'všechny úzkopásmové', 30), (51.41, 51.59, 'fm', 'FM', 31)],
     [(50.09, 'CW DX'), (50.11, 'DX volací'), (50.15, 'SSB'), (50.305, 'PSK'), (50.63, 'DV volací'),
      (51.51, 'FM volací')], None,
     'Třída A má pásmo 50–52 MHz jen na neinterferenční bázi; plán IARU pokračuje do 54 MHz. 50,0–50,1 MHz: IARU '
     'výhradně telegrafie; 50,4–50,5 MHz majáky; 50,7–50,9 MHz výstupy a 51,2–51,4 MHz vstupy FM/DV převaděčů; '
     '51,41–51,59 MHz FM simplex; 51,81–51,99 MHz další výstupy převaděčů.'),
    ('4 m', '70 MHz', 'MHz', 70.0, 70.5, True,
     [(70.0, 70.1, 'bcn'), (70.1, 70.25, 'fone'), (70.25, 70.5, 'fm')], [],
     [(70.2, 'CW/SSB'), (70.26, 'AM/FM volací'), (70.45, 'FM volací')], None,
     'Pásmo není ve vyhl. č. 156/2005 Sb. (v Evropě jej lze povolit podle poznámky ECA9).'),
    ('2 m', '144 MHz', 'MHz', 144, 146, False,
     [(144.0, 144.025, 'sat'), (144.025, 144.1, 'cw'), (144.1, 144.15, 'nb'), (144.15, 144.4, 'fone'),
      (144.4, 144.5, 'bcn'), (144.5, 144.794, 'wide'), (144.794, 144.9625, 'dig'), (144.9625, 144.975, 'gap'),
      (144.975, 145.194, 'fm'), (145.194, 145.206, 'fm'), (145.206, 145.5625, 'fm'), (145.5625, 145.575, 'gap'),
      (145.575, 145.794, 'fm'), (145.794, 145.806, 'fm'), (145.806, 146.0, 'sat')],
     [(144.0, 144.11, 'cw', 'CW', 33), (144.4, 144.49, 'bcn', 'majáky', 36), (145.806, 146.0, 'sat', 'družice', 35)],
     [(144.05, 'CW'), (144.3, 'SSB'), (144.5, 'SSTV'), (144.6, 'data'), (144.8, 'APRS'), (145.2, 'ISS'),
      (145.375, 'DV volací'), (145.5, 'FM volací')], None,
     'IARU: 144,000–144,025 MHz jen sestupné kanály družic; telegrafie výhradně do 144,110 MHz; 144,110–144,160 MHz CW '
     'a MGM EME – podle ČTÚ však úsek výhradně pro EME CW „není určen“ [→ a) 34]. 144,975–145,194 MHz vstupy a '
     '145,575–145,794 MHz výstupy FM převaděčů (posun 600 kHz); 145,206–145,5625 MHz FM simplex; 145,194–145,206 a '
     '145,794–145,806 MHz spojení s kosmickými stanicemi (ISS).'),
    ('70 cm', '430 MHz', 'MHz', 430, 440, False,
     [(430.0, 430.4, 'fm'), (430.4, 431.05, 'dig'), (431.05, 432.0, 'fm'), (432.0, 432.4, 'fone'), (432.4, 432.5, 'bcn'),
      (432.5, 433.0, 'wide'), (433.0, 433.4, 'fm'), (433.4, 433.6, 'fm'), (433.6, 434.6, 'wide'), (434.6, 435.0, 'fm'),
      (435.0, 438.0, 'sat'), (438.0, 438.65, 'dig'), (438.65, 439.6, 'fm'), (439.6, 439.8, 'wide'), (439.8, 440.0, 'dig')],
     [(432.025, 432.1, 'cw', 'CW', 39), (432.1, 432.4, 'fone', 'CW i SSB', 40), (432.4, 432.49, 'bcn', 'majáky', 37),
      (432.5, 432.975, 'wide', 'všechny druhy', 38)],
     [(432.05, 'CW'), (432.2, 'SSB'), (432.37, 'MS'), (432.5, 'APRS'), (433.4, 'SSTV'), (433.45, 'DV volací'),
      (433.5, 'FM volací'), (437.0, 'DATV/data')], (431.9, 433.7),
     'IARU: 430–432 MHz plánování podle zemí (převaděče, digitální spoje); 432,000–432,400 MHz úzkopásmový úsek pro '
     'všechny druhy do 2,7 kHz (CW 432,050, SSB 432,200 MHz); 433,0–433,4 MHz vstupy převaděčů; 433,4–433,6 MHz FM '
     'simplex; 434,6–435,0 a 438,65–439,6 MHz výstupy převaděčů; 435–438 MHz družice (436–438 MHz i DATV).'),
    ('23 cm', '1 240 MHz', 'MHz', 1240, 1300, False,
     [(1240.0, 1240.5, 'fone'), (1240.5, 1240.75, 'bcn'), (1240.75, 1241.0, 'fm'), (1241.0, 1243.25, 'dig'),
      (1243.25, 1260.0, 'atv'), (1260.0, 1270.0, 'sat'), (1270.0, 1272.0, 'dig'), (1272.0, 1291.0, 'atv'),
      (1291.0, 1291.5, 'fm'), (1291.5, 1296.0, 'wide'), (1296.0, 1296.15, 'nb'), (1296.15, 1296.8, 'fone'),
      (1296.8, 1297.0, 'bcn'), (1297.0, 1297.5, 'fm'), (1297.5, 1298.0, 'fm'), (1298.0, 1299.0, 'wide'),
      (1299.0, 1299.75, 'dig'), (1299.75, 1300.0, 'fm')],
     [],
     [(1296.0, 'EME'), (1296.2, 'úzkopásm.'), (1296.5, 'SSTV'), (1297.5, 'FM'), (1297.725, 'DV volací')],
     [(1240.0, 1243.6), (1295.8, 1300.0)],
     '1 243,25–1 260 a 1 272–1 291 MHz ATV/DATV; 1 260–1 270 MHz družice; 1 291,0–1 291,5 MHz vstupy a '
     '1 297,0–1 297,5 MHz výstupy převaděčů; 1 296,0–1 296,8 MHz úzkopásmový úsek (EME 1 296,000–1 296,025 MHz).'),
    ('13 cm', '2 300 MHz', 'MHz', 2300, 2450, False,
     [(2300.0, 2320.0, 'wide'), (2320.0, 2320.8, 'fone'), (2320.8, 2321.0, 'bcn'), (2321.0, 2322.0, 'fm'),
      (2322.0, 2355.0, 'atv'), (2355.0, 2365.0, 'dig'), (2365.0, 2370.0, 'fm'), (2370.0, 2392.0, 'atv'),
      (2392.0, 2400.0, 'dig'), (2400.0, 2450.0, 'sat')],
     [],
     [(2320.0, 'EME'), (2320.2, 'SSB')], (2319.8, 2322.2),
     '2 300–2 320 MHz plánování podle zemí; 2 320,0–2 320,8 MHz úzkopásmový úsek (EME, SSB 2 320,200 MHz); '
     '2 400–2 450 MHz družice (sdílí se s Wi-Fi/ISM).'),
    ('9 cm', '3 400 MHz', 'MHz', 3400, 3410, False,
     [(3400.0, 3400.8, 'fone'), (3400.8, 3401.0, 'bcn'), (3401.0, 3402.0, 'wide'), (3402.0, 3410.0, 'sat')],
     [],
     [(3400.1, 'úzkopásm. + EME')], None,
     'Vyhláška povoluje jen 3 400–3 410 MHz (plán IARU pokračuje do 3 475 MHz). 3 402–3 410 MHz družice (sestupné '
     'kanály).'),
    ('6 cm', '5 650 MHz', 'MHz', 5650, 5850, False,
     [(5650.0, 5670.0, 'sat'), (5670.0, 5700.0, 'dig'), (5700.0, 5760.0, 'wide'), (5760.0, 5760.8, 'fone'),
      (5760.8, 5761.0, 'bcn'), (5761.0, 5830.0, 'wide'), (5830.0, 5850.0, 'sat')],
     [],
     [(5668.2, 'úzkopásm.'), (5760.2, 'úzkopásm.')], (5759.8, 5761.4),
     '5 650–5 670 MHz vzestupné a 5 830–5 850 MHz sestupné kanály družic; úzkopásmová centra aktivity 5 668,2 a '
     '5 760,2 MHz; 5 670–5 700 MHz MGM (digitální).'),
]

X0, X1 = 92, 742
DARK = {'cw', 'fone', 'fm', 'bcn', 'sat', 'atv'}


def fnum(v):
    """kmitočet: mezera v tisících, desetinná čárka, bez zbytečných nul"""
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    a, _, b = s.partition('.')
    if len(a) > 3:
        a = a[:-3] + ' ' + a[-3:]
    return a + (',' + b if b else '')


def lanes(segs):
    """rozdělí překrývající se úseky ČTÚ do řádků"""
    rows = []
    for s in sorted(segs, key=lambda s: (s[0], -s[1])):
        for r in rows:
            if all(s[0] >= o[1] - 1e-9 or s[1] <= o[0] + 1e-9 for o in r):
                r.append(s); break
        else:
            rows.append([s])
    return rows


def seg_label(f, xa, xb, y, h, cat, texts, size=11):
    for t in texts:
        if t and tw(t, size) + 6 <= xb - xa:
            f.t((xa + xb) / 2, y + h / 2 + size * 0.36, t, size=size, c=CAT[cat][1], w='bold')
            return


def panel(f, y, fa, fb, unit, iaru, ctu, marks, dashed=False, skip=None, title=None):
    """nakreslí pruhy IARU a ČTÚ pro rozsah fa–fb od výšky y; vrátí (dolní y, X-funkce, y pruhů)"""
    X = lambda v: X0 + (v - fa) / (fb - fa) * (X1 - X0)
    inside = lambda v: fa - 1e-9 <= v <= fb + 1e-9
    if title:
        f.t(X0, y + 12, title, size=12, c='#555555', anchor='start', italic=True); y += 20
    # centra aktivity – hladiny popisků bez překryvu
    skip = skip or []
    mk = [m for m in marks if inside(m[0]) and not any(a < m[0] < b for a, b in skip)]
    placed, levels = [], 0
    for v, lab in sorted(mk):
        xm = X(v); w2 = tw(lab, 10.5) / 2 + 3
        lev = 0
        while any(p[2] == lev and not (xm - w2 > p[1] or xm + w2 < p[0]) for p in placed):
            lev += 1
        placed.append((xm - w2, xm + w2, lev, xm, lab)); levels = max(levels, lev + 1)
    ybar = y + (levels * 13 + 12 if levels else 4)
    for a, b, lev, xm, lab in placed:
        yl = ybar - 12 - lev * 13
        xt = min(max(xm, X0 + (b - a) / 2), X1 + 4 - (b - a) / 2)
        f.t(xt, yl, lab, size=10.5, c='#333333')
        f.l(xm, yl + 2, xm, ybar - 2, c='#999999', w=0.7)
        f.a(f'<polygon points="{xm - 4:.1f},{ybar - 6:.1f} {xm + 4:.1f},{ybar - 6:.1f} {xm:.1f},{ybar:.1f}" fill="#333333"/>')
    BH = 30
    ticks = {fa, fb}
    # IARU
    f.t(X0 - 8, ybar + BH / 2 + 4, 'IARU R1', size=11.5, w='bold', anchor='end')
    for a, b, cat in iaru:
        a, b = max(a, fa), min(b, fb)
        if b <= a: continue
        xa, xb = X(a), X(b)
        if xb - xa < 1.6: xa, xb = (xa + xb) / 2 - 0.8, (xa + xb) / 2 + 0.8
        f.rect(xa, ybar, xb - xa, BH, fill=CAT[cat][0], stroke='#ffffff', sw=0.6)
        seg_label(f, xa, xb, ybar, BH, cat, CAT[cat][3])
        ticks.update([a, b])
    f.rect(X0, ybar, X1 - X0, BH, fill='none', stroke='#444444', sw=1.4, dash='5,3' if dashed else None)
    yb = ybar + BH
    # ČTÚ
    vis = [s for s in ctu if s[1] > fa and s[0] < fb]
    if vis:
        rows = lanes(vis)
        LH = 17
        y0 = yb + 5
        f.t(X0 - 8, y0 + len(rows) * LH / 2 + 4, 'ČTÚ', size=11.5, w='bold', anchor='end', c='#b71c1c')
        f.rect(X0, y0, X1 - X0, len(rows) * LH, fill='#fafafa', stroke='#cccccc', sw=0.8)
        for k, r in enumerate(rows):
            for a, b, cat, lab, q in r:
                a2, b2 = max(a, fa), min(b, fb)
                xa, xb = X(a2), X(b2)
                if xb - xa < 1.6: xa, xb = (xa + xb) / 2 - 0.8, (xa + xb) / 2 + 0.8
                f.rect(xa, y0 + k * LH + 1, xb - xa, LH - 2, fill=CAT[cat][0], stroke='#ffffff', sw=0.6)
                seg_label(f, xa, xb, y0 + k * LH + 1, LH - 2, cat, [f'{lab} · a) {q}', lab, f'a) {q}'], size=10)
                ticks.update([a2, b2])
        yb = y0 + len(rows) * LH
    # osa a popisky hranic úseků (svisle, posunuté, aby se nepřekrývaly)
    f.l(X0, yb + 1, X1, yb + 1, c=TX, w=1.2)
    tk = sorted(v for v in ticks if not any(a < v < b for a, b in skip))
    xs, last = [], -1e9
    for v in tk:
        x = X(v)
        if xs and abs(x - X(xs[-1][0])) < 0.5:
            continue
        xl = max(x, last + 11.5)
        xs.append((v, xl)); last = xl
    over = xs[-1][1] - (X1 + 20) if xs else 0
    if over > 0:   # posunout zpět doleva, pokud popisky přetečou za okraj
        nx, nxt = [], X1 + 20
        for v, xl in reversed(xs):
            xl = min(xl, nxt); nx.append((v, xl)); nxt = xl - 11.5
        xs = list(reversed(nx))
    maxlen = max([tw(fnum(v), 10) for v, _ in xs] + [20])
    for v, xl in xs:
        x = X(v)
        f.l(x, yb - 3, x, yb + 5, c=TX, w=1)
        if abs(xl - x) > 0.5:
            f.l(x, yb + 5, xl, yb + 13, c='#888888', w=0.7)
        f.t(xl + 3.6, yb + 15, fnum(v), size=10, rot=-90, anchor='end')
    return yb + 15 + maxlen + 4, X, ybar


def resize(f, h):
    """změní výšku obrázku F po nakreslení (výška se zná až na konci)"""
    old, f.h = f.h, int(h)
    f.o[0] = f.o[0].replace(f'height="{old}"', f'height="{f.h}"').replace(f'0 0 {f.w} {old}', f'0 0 {f.w} {f.h}')
    f.o[1] = f.o[1].replace(f'height="{old}"', f'height="{f.h}"')


def band_fig(band):
    nm, mhz, unit, fa, fb, dashed, iaru, ctu, marks, zoom, note = band
    f = F(900)
    title = f'{nm} ({mhz}): {fnum(fa)}–{fnum(fb)} {unit}' + ('  – není ve vyhl. č. 156/2005 Sb.' if dashed else '')
    f.t(X0, 22, title, size=15, w='bold', anchor='start')
    f.t(X1, 22, f'osa: kmitočet [{unit}]', size=11, c='#555555', anchor='end')
    zooms = [] if not zoom else (zoom if isinstance(zoom, list) else [zoom])
    y, X, ybar = panel(f, 32 + (12 if len(zooms) > 1 else 0), fa, fb, unit, iaru, ctu, marks, dashed, skip=zooms)
    for k, (za, zb) in enumerate(zooms):
        xa, xb = X(za), X(zb)
        f.rect(xa - 1, ybar - 3, xb - xa + 2, 36, fill='none', stroke='#d32f2f', sw=1.6)
        yz = y + 10
        if len(zooms) == 1:
            f.path([(xa - 1, ybar + 33), (X0, yz)], c='#d32f2f', w=0.9, dash='3,3')
            f.path([(xb + 1, ybar + 33), (X1, yz)], c='#d32f2f', w=0.9, dash='3,3')
            ttl = f'Detail {fnum(za)}–{fnum(zb)} {unit} (červený rámeček)'
        else:
            f.t((xa + xb) / 2, ybar - 7, 'AB'[k], size=13, w='bold', c='#d32f2f')
            ttl = f'Detail {"AB"[k]}: {fnum(za)}–{fnum(zb)} {unit} (červený rámeček {"AB"[k]})'
        y, _, _ = panel(f, yz, za, zb, unit, iaru, ctu, marks, title=ttl)
    resize(f, y + 6)
    cap = ''
    if ctu:
        cap = 'Odpovědi ČTÚ: ' + '; '.join(
            f'{lab} {fnum(a)}–{fnum(b)} {unit} [→ a) {q}]' for a, b, c, lab, q in sorted(ctu, key=lambda s: s[0])) + '. '
    return f, cap + note


def legend():
    rowh = 24
    f = F(70 + len(ORDER) * rowh + 40)
    f.t(X0 - 52, 24, 'Barvy druhů provozu v následujících grafech', size=16, w='bold', anchor='start')
    for i, c in enumerate(ORDER):
        y = 44 + i * rowh
        f.rect(X0 - 52, y, 46, 18, fill=CAT[c][0], stroke='#999999', sw=0.6)
        f.t(X0 + 4, y + 14, CAT[c][2], size=12.5, anchor='start')
    y = 50 + len(ORDER) * rowh
    f.a(f'<polygon points="{X0 - 33:.1f},{y:.1f} {X0 - 25:.1f},{y:.1f} {X0 - 29:.1f},{y + 7:.1f}" fill="#333333"/>')
    f.t(X0 + 4, y + 8, 'centrum aktivity (doporučený kmitočet) podle plánu IARU', size=12.5, anchor='start')
    f.t(X0 - 52, y + 32, 'Pruh „IARU R1“ = plán IARU Region 1, pruh „ČTÚ“ = úseky z odpovědí ČTÚ „a) n“ = číslo otázky Provoz a).',
        size=12, anchor='start', c='#b71c1c')
    resize(f, y + 44)
    return f, ('Kategorie jsou zjednodušené: v plánu IARU má každý úsek předepsanou největší šířku pásma a „doporučený '
               'druh provozu“. Úseky „všechny druhy“ připouštějí i CW a digitální provozy, pokud nepřekročí šířku pásma.')


def generate():
    out = []
    fl, cl = legend()
    out.append(('Legenda', cl, fl.done(), fl.w, fl.h))
    for b in BANDS:
        fg, cap = band_fig(b)
        out.append((b[0], cap, fg.done(), fg.w, fg.h))
    return out


if __name__ == '__main__':   # náhledy: python3 -I skripty/pasma_provoz.py VÝST_SLOŽKA
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for i, (nm, cap, svg, w, h) in enumerate(generate()):
        open(os.path.join(od, f'pp{i:02d}.svg'), 'wb').write(svg)
    print('ok')
