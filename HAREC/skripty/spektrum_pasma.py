# -*- coding: utf-8 -*-
"""Příloha: kmitočtové spektrum 0–6 GHz – radioamatérská pásma (barevně) a ostatní služby (šedě).

generate() -> [(název, popisek, svg_bytes, šířka, výška)]
Radioamatérská pásma: příloha 1 vyhl. č. 156/2005 Sb. (plně), pásma 630 m, 60 m a 4 m jsou čárkovaně –
ve vyhlášce nejsou, existují v RR / plánu IARU R1.
Ostatní služby: orientačně podle RR 2024 čl. 5 (Region 1) a běžného využití v Evropě; hranice KV a vybraných
VKV/UKV pásem ověřeny v zdroje/itu/RR2024_Vol1.txt (15. 11. 2026). Mobilní sítě, Wi-Fi, DVB-T2, DAB, PMR446,
DECT – podle obecně známého využití v ČR/EU.
"""
from obrazky_elek import F, TX, GR

HAM, HAM_F = '#1565c0', '#1e88e5'
G_FILL, G_TXT = '#c4c4c4', '#555555'

TITLE = 'Příloha: Kmitočtové spektrum 0–6 GHz a radioamatérská pásma'
INTRO = ('Grafy ukazují, kde v kmitočtovém spektru leží radioamatérská pásma a co je v jejich okolí. Barva '
         'radioamatérského pásma vyjadřuje převažující způsob šíření (viz první graf); šířka sloupce odpovídá šířce pásma. '
         'Plné sloupce jsou pásma podle přílohy 1 vyhl. č. 156/2005 Sb.; čárkovaně jsou pásma 630 m, 60 m a 4 m, která '
         've vyhlášce uvedena nejsou (existují v Radiokomunikačním řádu a v plánu IARU Region 1). Velmi úzká pásma jsou '
         'zakreslena s minimální šířkou. Šedě jsou ostatní služby s rozsahem kmitočtů (u úzkých svisle) – orientačně a '
         'zjednodušeně podle Radiokomunikačního řádu ITU (čl. 5, Region 1) a běžného využití v ČR; překrývající se služby '
         'jsou pod sebou. Každý graf (kromě prvního) má lineární osu, proto mají grafy různé měřítko.')

# (název, od, do [MHz], čárkovaně?)
HAM_BANDS = [
    ('2200 m', 0.1357, 0.1378, False), ('630 m', 0.472, 0.479, True), ('160 m', 1.810, 2.000, False),
    ('80 m', 3.500, 3.800, False), ('60 m', 5.3515, 5.3665, True), ('40 m', 7.000, 7.200, False),
    ('30 m', 10.100, 10.150, False), ('20 m', 14.000, 14.350, False), ('17 m', 18.068, 18.168, False),
    ('15 m', 21.000, 21.450, False), ('12 m', 24.890, 24.990, False), ('10 m', 28.000, 29.700, False),
    ('6 m', 50, 52, False), ('4 m', 70.0, 70.5, True), ('2 m', 144, 146, False), ('70 cm', 430, 440, False),
    ('23 cm', 1240, 1300, False), ('13 cm', 2300, 2450, False), ('9 cm', 3400, 3410, False), ('6 cm', 5650, 5850, False),
]

# (popis, zkratka, od, do [MHz])
OTHER = [
    ('časový signál DCF77', 'ČS', 0.0770, 0.0780), ('dlouhé vlny – rozhlas', 'R', 0.1485, 0.2835),
    ('letecké majáky NDB', 'LN', 0.2835, 0.4720), ('námořní', 'N', 0.4150, 0.5265), ('střední vlny – rozhlas', 'R', 0.5265, 1.6065),
    ('námořní', 'N', 1.6065, 1.8000),
    ('letecká', 'L', 2.850, 3.155), ('letecká', 'L', 3.400, 3.500), ('rozhlas', 'R', 3.950, 4.000), ('námořní', 'N', 4.063, 4.438),
    ('letecká', 'L', 4.650, 4.750), ('rozhlas (trop.)', 'R', 4.750, 5.060), ('letecká', 'L', 5.450, 5.730), ('rozhlas 49 m', 'R', 5.900, 6.200),
    ('námořní', 'N', 6.200, 6.525), ('letecká', 'L', 6.525, 6.765), ('rozhlas 41 m', 'R', 7.200, 7.450), ('námořní', 'N', 8.195, 8.815),
    ('letecká', 'L', 8.815, 9.040), ('rozhlas 31 m', 'R', 9.400, 9.900), ('letecká', 'L', 10.005, 10.100), ('letecká', 'L', 11.175, 11.400),
    ('rozhlas 25 m', 'R', 11.600, 12.100), ('námořní', 'N', 12.230, 13.200), ('letecká', 'L', 13.200, 13.360),
    ('rozhlas 22 m', 'R', 13.570, 13.870), ('časový signál', 'ČS', 2.495, 2.505), ('časový signál', 'ČS', 4.995, 5.005),
    ('časový signál', 'ČS', 9.995, 10.005), ('časový signál', 'ČS', 14.990, 15.010),
    ('letecká', 'L', 15.010, 15.100), ('rozhlas 19 m', 'R', 15.100, 15.800), ('námořní', 'N', 16.360, 17.410),
    ('rozhlas 16 m', 'R', 17.480, 17.900), ('letecká', 'L', 17.900, 18.030), ('námořní', 'N', 18.780, 18.900),
    ('rozhlas 15 m', 'R', 18.900, 19.020), ('námořní', 'N', 19.680, 19.800), ('rozhlas 13 m', 'R', 21.450, 21.850),
    ('letecká', 'L', 21.924, 22.000), ('námořní', 'N', 22.000, 22.855), ('letecká', 'L', 23.200, 23.350),
    ('námořní', 'N', 25.070, 25.210), ('rozhlas 11 m', 'R', 25.670, 26.100), ('námořní', 'N', 26.100, 26.175),
    ('CB 27 MHz', 'CB', 26.965, 27.405),
    ('ISM', 'ISM', 40.66, 40.70), ('VKV FM rozhlas', 'R', 87.5, 108), ('letecká navigace VOR/ILS', 'LN', 108, 117.975),
    ('letecká komunikace', 'L', 117.975, 137), ('meteo družice', 'D', 137, 138), ('námořní VKV', 'N', 156, 162.05),
    ('DAB+ rozhlas', 'R', 174, 230),
    ('ISM/SRD 433 MHz', 'SRD', 433.05, 434.79), ('PMR446', 'PMR', 446.0, 446.2), ('DVB-T2 televize', 'TV', 470, 694),
    ('LTE 700', 'M', 703, 788), ('LTE 800', 'M', 791, 862), ('SRD 868', 'SRD', 863, 870), ('GSM/LTE 900', 'M', 880, 960),
    ('letecká navigace DME/SSR', 'LN', 960, 1215), ('GNSS (Galileo, GPS L5/L2)', 'GNSS', 1164, 1300), ('radiolokace (radary)', 'RL', 1215, 1400),
    ('radioastronomie', 'RA', 1400, 1427), ('družicová (Inmarsat)', 'D', 1525, 1559), ('GNSS (GPS L1…)', 'GNSS', 1559, 1610),
    ('Iridium', 'D', 1616, 1626.5), ('družicová', 'D', 1626.5, 1660.5), ('LTE 1800', 'M', 1710, 1880), ('DECT', 'DECT', 1880, 1900),
    ('UMTS/LTE 2100', 'M', 1920, 2170), ('Wi-Fi / ISM 2,4 GHz', 'ISM', 2400, 2483.5), ('LTE 2600', 'M', 2500, 2690),
    ('radary (letiště, meteo)', 'RL', 2700, 3100),
    ('5G 3,5 GHz', 'M', 3400, 3800), ('družice pásmo C (příjem)', 'D', 3700, 4200), ('radiovýškoměry letadel', 'LN', 4200, 4400),
    ('Wi-Fi 5 GHz', 'ISM', 5150, 5350), ('Wi-Fi 5 GHz', 'ISM', 5470, 5725), ('meteoradary', 'RL', 5600, 5650),
    ('ISM/SRD 5,8 GHz', 'ISM', 5725, 5875),
]

CODES = {'R': 'rozhlas', 'L': 'letecká pohyblivá', 'LN': 'letecká radionavigace', 'N': 'námořní', 'ČS': 'časový signál',
         'CB': 'občanské pásmo', 'ISM': 'průmysl./věd./lék. (ISM)', 'D': 'družicová', 'M': 'mobilní sítě', 'TV': 'televize',
         'SRD': 'zařízení krátkého dosahu', 'PMR': 'PMR446', 'GNSS': 'družicová navigace', 'RL': 'radiolokace',
         'RA': 'radioastronomie', 'DECT': 'DECT'}

# (název grafu, od, do, jednotka zobrazení, dělitel, popisky osy)
CHARTS = [
    ('Dlouhé a střední vlny: 0–2 MHz', 0, 2.05, 'kHz', 0.001, [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]),
    ('Krátké vlny I: 2–15 MHz', 2, 15.2, 'MHz', 1, [2, 4, 6, 8, 10, 12, 14]),
    ('Krátké vlny II: 15–30 MHz', 15, 30, 'MHz', 1, [15, 18, 21, 24, 27, 30]),
    ('VKV: 30–300 MHz', 30, 300, 'MHz', 1, [30, 50, 70, 100, 150, 200, 250, 300]),
    ('UKV I: 300 MHz – 1 GHz', 300, 1000, 'MHz', 1, [300, 400, 500, 600, 700, 800, 900, 1000]),
    ('UKV II: 1–3 GHz', 1000, 3100, 'GHz', 1000, [1, 1.5, 2, 2.5, 3]),
    ('Mikrovlny: 3–6 GHz', 3100, 6000, 'GHz', 1000, [3.5, 4, 4.5, 5, 5.5, 6]),
]


def fmt(v):
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    if '.' in s and len(s.split('.')[0]) > 3:
        s = s.split('.')[0]
    a, _, b = s.partition('.')
    if len(a) > 3:
        a = a[:-3] + ' ' + a[-3:]
    return a + (',' + b if b else '')


def frng(a, b, unit, div, with_unit=False):
    """rozsah a–b [MHz] v jednotce grafu; v MHz grafu se hodnoty od 1 000 MHz píší v GHz"""
    if unit == 'MHz' and b >= 1000:
        return f'{fmt(a / 1000)}–{fmt(b / 1000)} GHz'
    return f'{fmt(a / div)}–{fmt(b / div)}' + (f' {unit}' if with_unit else '')


def tw(s, size):  # odhad šířky textu
    return len(s) * size * 0.56


# ---------------------------------------------------------------- druhy šíření (barvy amatérských pásem)
CAT = {   # klíč: (barva, popis do legendy)
    'gnd': ('#8d5a2b', 'přízemní vlna – šíří se podél zemského povrchu (DV, SV)'),
    'iono': ('#ff1a1a', 'odraz od ionosféry – dálková spojení (KV)'),
    'trans': ('#ef6c00', 'ionosférou většinou projdou – odraz jen výjimečně (Es, maximum slunečního cyklu)'),
    'los': ('#1565c0', 'přímá viditelnost, troposféra'),
    'aur': ('#8e24aa', 'použitelné pro odraz od polární záře (aurora)'),
}
BAND_CAT = {   # pásmo -> druhy šíření (sloupec se rozdělí na části), aurora se kreslí zvlášť jako pruh nahoře
    '2200 m': ['gnd'], '630 m': ['gnd'], '160 m': ['gnd', 'iono'], '80 m': ['iono'], '60 m': ['iono'], '40 m': ['iono'],
    '30 m': ['iono'], '20 m': ['iono'], '17 m': ['iono'], '15 m': ['iono'], '12 m': ['iono'], '10 m': ['iono', 'trans'],
    '6 m': ['trans', 'los'], '4 m': ['trans', 'los'], '2 m': ['los'], '70 cm': ['los'], '23 cm': ['los'], '13 cm': ['los'],
    '9 cm': ['los'], '6 cm': ['los'],
}
AURORA = {'10 m': 0.6, '6 m': 1, '4 m': 1, '2 m': 1, '70 cm': 0.45}   # síla (průhlednost) pruhu


def chart(title, fa, fb, unit, div, ticks):
    x0, x1 = 40, 725
    X = lambda v: x0 + (v - fa) / (fb - fa) * (x1 - x0)
    hams = [h for h in HAM_BANDS if h[2] > fa and h[1] < fb]
    oth = sorted([o for o in OTHER if o[3] > fa and o[2] < fb], key=lambda o: o[2])
    RH, LS = 64, 10.5
    # způsob popisu každé šedé služby a místo, které popisek zabere
    items = []
    for o in oth:
        nm, code, a, b = o
        xa, xb = X(max(a, fa)), X(min(b, fb))
        if xb - xa < 3: xa, xb = (xa + xb) / 2 - 1.5, (xa + xb) / 2 + 1.5
        rng = frng(a, b, unit, div)
        wpx = xb - xa
        if max(tw(nm, LS), tw(rng, LS)) + 6 <= wpx:
            mode, ext = 'h2', (xa, xb)
        elif max(tw(code, LS), tw(rng, LS)) + 6 <= wpx:
            mode, ext = 'h2c', (xa, xb)
        else:
            c = (xa + xb) / 2
            mode, ext = 'rot', (min(xa, c - 7), max(xb, c + 7))
        items.append((o, xa, xb, rng, mode, ext))
    rot = [tw(f'{it[0][1]} {it[3]}', 9.5) + 10 for it in items if it[4] == 'rot']
    RH = max([RH] + rot)
    rows = []
    for it in items:
        for r in rows:
            if r[-1][5][1] + 2 < it[5][0]:
                r.append(it); break
        else:
            rows.append([it])
    yb0, yb1 = 78, 128
    yg = 140
    ya = yg + len(rows) * (RH + 4) + 2
    used = set()
    f = F(ya + 92)
    f.t(x0, 22, title, size=16, w='bold', anchor='start')
    for nm, a, b, dash in hams:
        xa, xb = X(max(a, fa)), X(min(b, fb))
        if xb - xa < 4: xa, xb = (xa + xb) / 2 - 2, (xa + xb) / 2 + 2
        f.rect(xa, yb0, xb - xa, ya - yb0, fill=CAT[BAND_CAT[nm][-1]][0], stroke='none', op=0.07)
    for i, r in enumerate(rows):
        y = yg + i * (RH + 4)
        for (nm, code, a, b), xa, xb, rng, mode, ext in r:
            f.rect(xa, y, xb - xa, RH, fill=G_FILL, stroke='#a0a0a0', sw=0.6, op=0.75)
            cx = (xa + xb) / 2
            if mode == 'h2':
                f.t(cx, y + RH / 2 - 2, nm, size=LS, c=G_TXT, w='bold'); f.t(cx, y + RH / 2 + 12, rng, size=LS, c=G_TXT)
            elif mode == 'h2c':
                f.t(cx, y + RH / 2 - 2, code, size=LS, c=G_TXT, w='bold'); f.t(cx, y + RH / 2 + 12, rng, size=LS, c=G_TXT)
                used.add(code)
            else:
                f.t(cx + 3.6, y + RH - 3, f'{code} {rng}', size=9.5, c=G_TXT, rot=-90, anchor='start'); used.add(code)
    # amatérská pásma – barva podle druhu šíření
    for nm, a, b, dash in hams:
        xa, xb = X(max(a, fa)), X(min(b, fb))
        if xb - xa < 4: xa, xb = (xa + xb) / 2 - 2, (xa + xb) / 2 + 2
        cats = BAND_CAT[nm]
        hh = (yb1 - yb0) / len(cats)
        for k, cat in enumerate(cats):
            col = CAT[cat][0]
            f.rect(xa, yb0 + k * hh, xb - xa, hh, fill=col if not dash else '#ffffff', stroke='none', op=0.9 if not dash else 1)
            if dash:
                f.rect(xa, yb0 + k * hh, xb - xa, hh, fill=col, stroke='none', op=0.3)
        f.rect(xa, yb0, xb - xa, yb1 - yb0, fill='none', stroke=CAT[cats[0]][0], sw=1.6, dash='4,3' if dash else None)
        if nm in AURORA:
            f.rect(xa, yb0 - 8, xb - xa, 6, fill=CAT['aur'][0], stroke='none', op=AURORA[nm])
        cx = (xa + xb) / 2
        col = CAT[cats[0]][0]
        f.t(cx, 42, nm, size=14, w='bold', c=col)
        f.t(cx, 58, frng(a, b, unit, div, unit == 'kHz'), size=11, c=col)
    f.arrow([(x0, ya), (x1 + 18, ya)], c=TX, w=1.5)
    for v in ticks:
        xv = X(v * div)
        f.l(xv, ya - 4, xv, ya + 4, w=1.3); f.t(xv, ya + 19, f'{fmt(v / 1000)} GHz' if unit == 'MHz' and v >= 1000 else fmt(v), size=12)
    f.t(x1 + 18, ya - 9, f'f [{unit}]', size=12, anchor='end', w='bold')
    yl = ya + 42
    cats_here = []
    for h in hams:
        for c in BAND_CAT[h[0]] + (['aur'] if h[0] in AURORA else []):
            if c not in cats_here: cats_here.append(c)
    xx = x0
    for c in cats_here:
        lab = CAT[c][1].split(' – ')[0]
        f.rect(xx, yl - 10, 14, 10, fill=CAT[c][0], stroke='none', op=0.9); f.t(xx + 18, yl, lab, size=11, anchor='start', c=CAT[c][0])
        xx += 26 + tw(lab, 11)
    if used:
        parts, lines = [f'{c} = {CODES[c]}' for c in sorted(used)], ['Zkratky: ']
        for prt in parts:
            if tw(lines[-1] + prt, 11) > 690: lines.append('')
            lines[-1] += prt + ', '
        f.t(x0, yl + 20, '\n'.join(l.rstrip(', ') for l in lines), size=11, c=G_TXT, anchor='start')
    names = ', '.join(f'{h[0]} ({frng(h[1], h[2], unit, div, True)})' for h in hams)
    cap = f'Radioamatérská pásma v tomto úseku: {names}.' if hams else ''
    if any(h[3] for h in hams):
        cap += ' Čárkovaně: pásmo není uvedeno ve vyhl. č. 156/2005 Sb.'
    return f, cap


def overview():
    """přehled druhů šíření na logaritmické ose 0,1 MHz – 6 GHz"""
    import math
    x0, x1 = 40, 725
    la, lb = math.log10(0.1), math.log10(6000)
    X = lambda v: x0 + (math.log10(v) - la) / (lb - la) * (x1 - x0)
    rows = [('gnd', 0.1, 3, 'přízemní vlna (DV, SV, do ≈ 3 MHz)'),
            ('iono', 1.8, 30, 'odraz od ionosféry (≈ 1,8–30 MHz, horní mez = MUF)'),
            ('trans', 28, 150, 'odraz jen výjimečně (Es, max. cyklu)'),
            ('los', 50, 6000, 'přímá viditelnost, troposféra (VKV a výše)'),
            ('aur', 28, 450, 'aurora (28–450 MHz)')]
    f = F(64 + len(rows) * 34 + 60)
    f.t(x0, 22, 'Druhy šíření podle kmitočtu – význam barev v grafech', size=16, w='bold', anchor='start')
    yb = 40
    for nm, a, b, dash in HAM_BANDS:
        xc = (X(a) + X(b)) / 2
        f.l(xc, yb, xc, 64 + len(rows) * 34, '#cccccc', 0.8, '2,3')
    for i, (c, a, b, lab) in enumerate(rows):
        y = 52 + i * 34
        f.rect(X(a), y, X(b) - X(a), 24, fill=CAT[c][0], stroke='none', op=0.85, rx=4)
        tx = X(a) + 6 if tw(lab, 12) + 12 < X(b) - X(a) else X(b) + 6
        f.t(tx, y + 17, lab, size=12, c='#ffffff' if tx < X(b) else CAT[c][0], w='bold', anchor='start')
    ya = 56 + len(rows) * 34
    f.arrow([(x0, ya), (x1 + 18, ya)], c=TX, w=1.5)
    for v, lab in ((0.1, '0,1'), (1, '1'), (10, '10'), (100, '100'), (1000, '1 GHz'), (6000, '6 GHz')):
        f.l(X(v), ya - 4, X(v), ya + 4, w=1.3); f.t(X(v), ya + 19, lab, size=12)
    for nm, a, b, dash in HAM_BANDS:
        if nm in ('2200 m', '160 m', '80 m', '40 m', '20 m', '10 m', '6 m', '2 m', '70 cm', '23 cm', '13 cm', '6 cm'):
            f.t((X(a) + X(b)) / 2 + 4, ya + 34, nm, size=10, c=G_TXT, rot=-90, anchor='end')
    f.t(x1 + 18, ya - 9, 'f (log.)', size=12, anchor='end', w='bold')
    return f, ('Hranice jsou orientační – závisí na denní době, ročním období a sluneční činnosti. Svislé tečkované čáry '
               'označují radioamatérská pásma. V následujících grafech mají radioamatérská pásma barvu podle převažujícího '
               'způsobu šíření; pásma se dvěma způsoby jsou rozdělena na dvě části (např. 160 m: přízemní vlna i odraz v '
               'noci; 6 m: většinou přímá viditelnost, výjimečně odraz od Es), fialový pruh nad sloupcem = použitelné pro '
               'auroru.')


def generate():
    out = []
    fo, co = overview()
    out.append(('Druhy šíření', co, fo.done(), fo.w, fo.h))
    for title, fa, fb, unit, div, ticks in CHARTS:
        fg, cap = chart(title, fa, fb, unit, div, ticks)
        out.append((title, cap, fg.done(), fg.w, fg.h))
    return out
