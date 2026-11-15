# -*- coding: utf-8 -*-
"""Schematická spektra druhů provozu (tříd vysílání) – generuje SVG bez externích knihoven.

PANELS = [(název, popis, xmin, xmax, ticks, prvky)]; kmitočty jsou relativní k nosné f_n (jednotka podle panelu).
Prvky:
  ('car', f, h, štítek)        – nosná (červená spektrální čára)
  ('sup', f, štítek)           – potlačená / nevysílaná nosná (čárkovaně)
  ('band', [(f, h), ...], štít.) – postranní pásmo (vyplněný mnohoúhelník nad osou)
  ('ln', f, h, štítek|None)    – spektrální čára modulace (modrá)
  ('curve', fn, f1, f2, štít.) – spojité spektrum h = fn(f)
  ('filt', f1, f2, štítek)     – propustné pásmo filtru (tečkovaný obdélník)
  ('bw', f1, f2, text)         – šířka pásma (kóta nad grafem)
Výška h je 0–1 (relativní amplituda, schematicky).
"""
import math

W, H = 1000, 205
X0, X1 = 30, 950          # plocha grafu
YB, YT = 160, 48          # základní čára, výška h = 1
C_CAR, C_SB, C_SBF, C_GR = '#c0392b', '#2e5597', '#8fb0e0', '#888888'


def bessel(n, x):
    return sum((-1) ** k / (math.factorial(k) * math.factorial(n + k)) * (x / 2) ** (2 * k + n) for k in range(30))


def sinc2(u):
    return 1.0 if abs(u) < 1e-9 else (math.sin(math.pi * u) / (math.pi * u)) ** 2


def svg(xmin, xmax, ticks, items):
    sx = lambda f: X0 + (f - xmin) / (xmax - xmin) * (X1 - X0)
    sy = lambda h: YB - h * (YB - YT)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Liberation Sans, Arial, sans-serif" font-size="14">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>']
    txt = lambda x, y, t, c='#222222', a='middle', s=14, w='normal': o.append(
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" text-anchor="{a}" font-size="{s}" font-weight="{w}">{t}</text>')
    labels = []
    for it in items:
        k = it[0]
        if k == 'filt':
            _, f1, f2, lab = it
            o.append(f'<rect x="{sx(f1):.1f}" y="{sy(1.0):.1f}" width="{sx(f2) - sx(f1):.1f}" height="{YB - sy(1.0):.1f}" '
                     f'fill="none" stroke="{C_GR}" stroke-width="1.5" stroke-dasharray="2,4"/>')
            if lab: labels.append(((sx(f1) + sx(f2)) / 2, sy(1.0) + 16, lab, C_GR))
        elif k == 'band':
            _, pts, lab = it
            p = [(sx(pts[0][0]), YB)] + [(sx(f), sy(h)) for f, h in pts] + [(sx(pts[-1][0]), YB)]
            o.append('<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in p) +
                     f'" fill="{C_SBF}" fill-opacity="0.75" stroke="{C_SB}" stroke-width="1.5"/>')
            if lab:
                fm = sum(f for f, _ in pts) / len(pts)
                labels.append((sx(fm), sy(max(h for _, h in pts)) - 8, lab, C_SB))
        elif k == 'curve':
            _, fn, f1, f2, lab = it
            n = 300
            p = [(sx(f1), YB)] + [(sx(f1 + (f2 - f1) * i / n), sy(fn(f1 + (f2 - f1) * i / n))) for i in range(n + 1)] + [(sx(f2), YB)]
            o.append('<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in p) +
                     f'" fill="{C_SBF}" fill-opacity="0.75" stroke="{C_SB}" stroke-width="1.5"/>')
            if lab: labels.append(lab)
        elif k == 'sup':
            _, f, lab = it
            o.append(f'<line x1="{sx(f):.1f}" y1="{YB}" x2="{sx(f):.1f}" y2="{sy(1.0):.1f}" stroke="{C_GR}" stroke-width="2" stroke-dasharray="6,4"/>')
            if lab: labels.append((sx(f), sy(1.0) - 8, lab, C_GR))
        elif k in ('car', 'ln'):
            _, f, h, lab = it
            c, w = (C_CAR, 3.5) if k == 'car' else (C_SB, 3)
            x, y = sx(f), sy(h)
            o.append(f'<line x1="{x:.1f}" y1="{YB}" x2="{x:.1f}" y2="{y + 6:.1f}" stroke="{c}" stroke-width="{w}"/>')
            o.append(f'<polygon points="{x - 5:.1f},{y + 8:.1f} {x + 5:.1f},{y + 8:.1f} {x:.1f},{y:.1f}" fill="{c}"/>')
            if lab: labels.append((x, y - 8, lab, c))
        elif k == 'bw':
            _, f1, f2, t = it
            a, b, y = sx(f1), sx(f2), 22
            o.append(f'<line x1="{a:.1f}" y1="{y}" x2="{b:.1f}" y2="{y}" stroke="#555555" stroke-width="1.2"/>')
            for x in (a, b):
                o.append(f'<line x1="{x:.1f}" y1="{y - 6}" x2="{x:.1f}" y2="{y + 6}" stroke="#555555" stroke-width="1.2"/>')
                o.append(f'<line x1="{x:.1f}" y1="{y + 6}" x2="{x:.1f}" y2="{YB}" stroke="#bbbbbb" stroke-width="0.8" stroke-dasharray="3,3"/>')
            txt((a + b) / 2, y - 7, t, '#333333', s=13)
    # osa kmitočtu a značky
    o.append(f'<line x1="{X0 - 10}" y1="{YB}" x2="{X1 + 25}" y2="{YB}" stroke="#222222" stroke-width="1.5"/>')
    o.append(f'<polygon points="{X1 + 35},{YB} {X1 + 23},{YB - 5} {X1 + 23},{YB + 5}" fill="#222222"/>')
    txt(X1 + 38, YB + 22, 'f', a='end', s=16, w='bold')
    for f, lab in ticks:
        o.append(f'<line x1="{sx(f):.1f}" y1="{YB}" x2="{sx(f):.1f}" y2="{YB + 6}" stroke="#222222" stroke-width="1.2"/>')
        txt(sx(f), YB + 22, lab, s=13)
    for x, y, t, c in labels:
        txt(x, y, t, c, s=13, w='bold')
    o.append('</svg>')
    return '\n'.join(o)


# ---------------------------------------------------------------- tvary
def speech(f1, f2, side=1):
    """Typický tvar spektra řeči v postranním pásmu (300 Hz – 3 kHz), side=-1 zrcadlí pod nosnou."""
    pts = [(0.30, 0.0), (0.45, 0.62), (0.8, 0.85), (1.3, 0.72), (2.0, 0.48), (2.6, 0.30), (2.95, 0.0)]
    s = (f2 - f1) / (2.95 - 0.30)
    pts = [(f1 + (f - 0.30) * s, h) for f, h in pts]
    return pts if side > 0 else [(-f, h) for f, h in reversed(pts)]


def fm_lines(beta, fm, nmax, k=1.0):
    out = []
    for n in range(-nmax, nmax + 1):
        a = abs(bessel(abs(n), beta)) * k
        if a < 0.015: continue
        out.append(('car' if n == 0 else 'ln', n * fm, a, None))
    return out


KHZ = lambda v: (f'fₙ{v:+g} kHz'.replace('-', '−').replace('.', ',') if v else 'fₙ')
MHZ = lambda v: (f'fₙ{v:+g} MHz'.replace('-', '−').replace('.', ',') if v else 'fₙ')
HZ = lambda v: (f'fₙ{v:+g} Hz'.replace('-', '−') if v else 'fₙ')

PANELS = [
    ('N0N – nemodulovaná nosná',
     'Vysílá se jen nosná vlna na jediném kmitočtu fₙ. Nepřenáší žádnou informaci (zkušební vysílání, ladění).',
     -3, 3, [(v, KHZ(v)) for v in (-3, -2, -1, 0, 1, 2, 3)],
     [('car', 0, 1.0, 'nosná')]),
    ('A1A – telegrafie CW (klíčování nosné)',
     'Nosná se zapíná a vypíná v rytmu Morseovy abecedy (amplitudová modulace, 2 stavy). Spektrum je velmi úzké '
     '– jen nosná a úzká „klíčovací“ postranní pásma (řádově 100 Hz podle rychlosti klíčování). Příliš strmé hrany '
     'značek rozšiřují spektrum (kliksy).',
     -500, 500, [(v, HZ(v)) for v in (-500, -250, 0, 250, 500)],
     [('curve', lambda f: 0.55 * sinc2(f / 60) if abs(f) < 240 else 0, -240, 240, None),
      ('car', 0, 1.0, 'nosná'), ('bw', -60, 60, '≈ 100 Hz')]),
    ('A2A – tónová telegrafie MCW',
     'Nosná je amplitudově modulována klíčovaným nízkofrekvenčním tónem (např. 1 kHz). Ve spektru je nosná a dvě '
     'postranní čáry ve vzdálenosti kmitočtu tónu (fₙ ± 1 kHz). Přijímá se i obyčejným AM nebo FM přijímačem (ROB).',
     -3, 3, [(v, KHZ(v)) for v in (-3, -2, -1, 0, 1, 2, 3)],
     [('car', 0, 1.0, 'nosná'), ('ln', -1, 0.45, 'fₙ − tón'), ('ln', 1, 0.45, 'fₙ + tón'), ('bw', -1, 1, '2 × kmitočet tónu')]),
    ('A3E – telefonie AM (dvě postranní pásma, plná nosná)',
     'Nosná zůstává, informace je ve dvou zrcadlově souměrných postranních pásmech – dolním (LSB) a horním (USB). '
     'Šířka pásma = 2 × nejvyšší modulační kmitočet, tj. asi 6 kHz. Většina výkonu připadá na nosnou, která informaci nenese.',
     -4, 4, [(v, KHZ(v)) for v in (-4, -3, -2, -1, 0, 1, 2, 3, 4)],
     [('band', speech(0.3, 3.0, -1), 'LSB'),
      ('band', speech(0.3, 3.0), 'USB'), ('car', 0, 1.0, 'nosná'), ('bw', -3, 3, '≈ 6 kHz')]),
    ('J3E – telefonie SSB, horní postranní pásmo (USB)',
     'Nosná i dolní postranní pásmo jsou potlačeny, vysílá se jen horní postranní pásmo (300 Hz – 2,7 kHz nad fₙ). '
     'Šířka pásma asi 2,4–2,7 kHz. Podle zvyklosti se USB používá v pásmech nad 10 MHz. Transceiver ukazuje kmitočet '
     'potlačené nosné.',
     -1.5, 4, [(v, KHZ(v)) for v in (-1, 0, 1, 2, 3, 4)],
     [('sup', 0, 'potlačená nosná'), ('band', speech(0.3, 2.7), 'USB'), ('bw', 0.3, 2.7, '≈ 2,4 kHz')]),
    ('J3E – telefonie SSB, dolní postranní pásmo (LSB)',
     'Zrcadlový případ: vysílá se jen dolní postranní pásmo (300 Hz – 2,7 kHz pod fₙ). Podle zvyklosti se LSB '
     'používá v pásmech pod 10 MHz (160, 80, 40 m, tj. 1,8; 3,5 a 7 MHz). Spektrum řeči je oproti USB převrácené: nízké tóny leží '
     'těsně pod nosnou, vyšší tóny dále od ní směrem dolů.',
     -4, 1.5, [(v, KHZ(v)) for v in (-4, -3, -2, -1, 0, 1)],
     [('sup', 0, 'potlačená nosná'), ('band', [(-f, h) for f, h in reversed(speech(0.3, 2.7))], 'LSB'), ('bw', -2.7, -0.3, '≈ 2,4 kHz')]),
    ('J2A – telegrafie tónem přes SSB vysílač',
     'Do mikrofonního vstupu SSB vysílače (USB) se přivádí klíčovaný tón např. 700 Hz. Vyzařuje se jediná čára '
     'fₙ + 700 Hz – ve vzduchu je to totéž jako A1A, jen posunuté od zobrazeného kmitočtu.',
     -1.5, 4, [(v, KHZ(v)) for v in (-1, 0, 1, 2, 3, 4)],
     [('filt', 0.3, 2.7, 'propust SSB filtru'), ('sup', 0, 'potlačená nosná'), ('ln', 0.7, 0.8, 'tón 700 Hz')]),
    ('J2B – RTTY / PSK31 přes SSB vysílač (AFSK)',
     'Zvuková karta nebo modem generuje dva tóny (RTTY: posun 170 Hz, např. 2 125 a 2 295 Hz), které SSB vysílač '
     'přenese do vf pásma. Výsledné spektrum je stejné jako u F1B. Obdobně PSK31 – jediný úzký signál (asi 60 Hz) '
     'kdekoli v propustném pásmu.',
     -1.5, 4, [(v, KHZ(v)) for v in (-1, 0, 1, 2, 3, 4)],
     [('filt', 0.3, 2.7, 'propust SSB filtru'), ('sup', 0, 'potlačená nosná'),
      ('ln', 2.125, 0.8, None), ('ln', 2.295, 0.8, 'mark / space'), ('bw', 2.125, 2.295, '170 Hz')]),
    ('J2D – digitální provozy přes SSB (např. FT8)',
     'Digitální signály ze zvukové karty zabírají jen malou část propustného pásma SSB. U FT8 má jeden signál šířku '
     'asi 50 Hz a v pásmu 0,2–3 kHz nad fₙ jich současně vysílá mnoho stanic (každá na jiném zvukovém kmitočtu).',
     -1.5, 4, [(v, KHZ(v)) for v in (-1, 0, 1, 2, 3, 4)],
     [('filt', 0.2, 3.0, 'propust SSB filtru'), ('sup', 0, 'potlačená nosná')] +
     [('band', [(c - 0.025, 0.55), (c + 0.025, 0.55)], None) for c in (0.45, 0.8, 1.05, 1.5, 1.62, 2.0, 2.35, 2.7)] +
     [('bw', 1.475, 1.525, '1 signál ≈ 50 Hz')]),
    ('F1B – dálnopis RTTY kmitočtovým klíčováním (FSK)',
     'Nosná se přeskakuje mezi dvěma kmitočty – značka (mark) a mezera (space) – posunutými o 170 Hz. Na nominálním '
     'kmitočtu fₙ (uprostřed) se nevysílá. Stejně F1A (telegrafie) a F1D (data). Amplituda je stálá.',
     -400, 400, [(v, HZ(v)) for v in (-400, -200, -85, 0, 85, 200, 400)],
     [('sup', 0, 'nominální kmitočet'), ('ln', -85, 0.85, 'mezera'), ('ln', 85, 0.85, 'značka'), ('bw', -85, 85, 'posun 170 Hz')]),
    ('F3E / G3E – telefonie FM (úzkopásmová, kanál 12,5 kHz)',
     'Modulace mění okamžitý kmitočet nosné (zdvih Δf ≈ 2,5–3 kHz). Ve spektru vzniká nosná a teoreticky nekonečně '
     'mnoho postranních čar vzdálených o modulační kmitočet fₘ; jejich velikost určuje index modulace β = Δf / fₘ '
     '(zde β = 1,5, tón 2 kHz). Šířka pásma podle Carsonova pravidla B ≈ 2·(Δf + fₘ) ≈ 11–12 kHz. Nosná zůstává, '
     'ale její amplituda se mění (při β ≈ 2,4 zmizí). G3E (fázová modulace) má obdobné spektrum; F2A a F2D (AFSK '
     '1 200/2 200 Hz pro paket rádio a APRS) jsou FM modulace tóny se stejným tvarem spektra.',
     -10, 10, [(v, KHZ(v)) for v in (-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10)],
     fm_lines(1.5, 2, 5) + [('bw', -6, 6, '≈ 12 kHz')]),
    ('G1D / G1B – fázové klíčování PSK (BPSK)',
     'Fáze nosné se přepíná mezi 0° a 180° podle přenášených bitů. U BPSK je nosná potlačena; energie leží v hlavním '
     'laloku šířky 2 × modulační rychlost (R) kolem fₙ a v menších postranních lalocích. Filtrací (tvarováním) '
     'se postranní laloky omezí.',
     -3, 3, [(-3, 'fₙ−3R'), (-2, 'fₙ−2R'), (-1, 'fₙ−R'), (0, 'fₙ'), (1, 'fₙ+R'), (2, 'fₙ+2R'), (3, 'fₙ+3R')],
     [('curve', lambda f: 0.9 * sinc2(f), -2.98, 2.98, None), ('sup', 0, 'potlačená nosná'), ('bw', -1, 1, 'hlavní lalok 2R')]),
    ('C3F – amatérská televize s amplitudovou modulací (ATV)',
     'Obrazová nosná je amplitudově modulována obrazovým signálem (asi 5 MHz). Horní postranní pásmo se vysílá celé, '
     'dolní jen zčásti (částečně potlačené postranní pásmo – „vestigial sideband“, odtud písmeno C). Nad obrazem je '
     'zvuková nosná (podle normy +5,5 nebo +6,5 MHz). Šířka pásma asi 7–8 MHz – proto jen v pásmech 70 cm (430–440 MHz) a výše.',
     -2, 7.5, [(v, MHZ(v)) for v in (-2, -1, 0, 1, 2, 3, 4, 5, 6, 7)],
     [('band', [(-1.25, 0.0), (-0.75, 0.55), (0, 0.6), (4.2, 0.45), (5.0, 0.0)], 'obraz'),
      ('car', 0, 1.0, 'obrazová nosná'), ('ln', 5.5, 0.35, 'zvuk'), ('bw', -1.25, 6.0, '≈ 7 MHz')]),
    ('F3F – amatérská televize s kmitočtovou modulací (FM ATV)',
     'Obrazový signál moduluje kmitočet nosné s velkým zdvihem. Spektrum je široké (typicky 16–20 MHz) a souvislé, '
     'zvuk se přenáší na pomocné nosné v základním pásmu. Používá se v pásmech 23 cm (1 240–1 300 MHz) a výše.',
     -12, 12, [(v, MHZ(v)) for v in (-12, -8, -4, 0, 4, 8, 12)],
     [('curve', lambda f: 0.7 * math.exp(-(f / 6.0) ** 4), -11.5, 11.5, None), ('sup', 0, 'nominální kmitočet'), ('bw', -9, 9, '≈ 18 MHz')]),
]

INTRO = ('Schematická spektra (amplituda v závislosti na kmitočtu) ukazují, kde se při jednotlivých druzích '
         'provozu nachází vyzařovaná energie vzhledem ke kmitočtu nosné fₙ. Červeně je nosná, čárkovaně potlačená '
         'nebo nevysílaná nosná, modře postranní pásma a modulační složky, tečkovaně propustné pásmo SSB filtru; kóta '
         'nahoře udává přibližnou šířku pásma. Měřítko svislé osy je jen orientační.')


def generate():
    """Vrátí [(název, popis, svg_bytes)]."""
    return [(t, d, svg(a, b, tk, it).encode('utf-8')) for t, d, a, b, tk, it in PANELS]
