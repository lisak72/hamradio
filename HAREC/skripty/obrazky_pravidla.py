# -*- coding: utf-8 -*-
"""Obrázky k závěrečnému oddílu „Pravidla a souvislosti pro snadnější zapamatování“ (pravidla.py).

BAND_FIG – funkce s obrázkem pořadí úseků v KV pásmech (vkládá se za přehledovou tabulku pásem)
FIGS[název skupiny pravidel] -> [funkce] ; funkce vrací (svg_bytes, šířka, výška, popisek)
Vkládá se za tabulku příslušné skupiny. Barvy úseků pásem shodné s přílohou pasma_provoz (CAT).
Hodnoty podle odpovědí ČTÚ (provoz a), předpisy c), elektrotechnika j)) a vyhl. 156/2005 Sb.
Náhledy: python3 -I skripty/obrazky_pravidla.py VÝST_SLOŽKA
"""
import math
from obrazky_elek import F, BL, BLF, RED, GR, TX, GRN, ORA
from pasma_provoz import CAT

LIGHT = '#f4f6fa'


def col(k):
    return CAT[k][0], CAT[k][1]


def legend(f, x, y, items, size=12):
    for k, lab in items:
        fill, _ = col(k)
        f.rect(x, y - 11, 16, 14, fill=fill, stroke='#555555', sw=0.8)
        f.t(x + 21, y, lab, size=size, anchor='start')
        x += 40 + len(lab) * size * 0.6


# --------------------------------------------------------------- 1. pořadí úseků v KV pásmech
# (název, rozsah, [(kategorie, od, do, 'full'|'top'|'bot')], maják kHz | None)
HF = [
    ('160 m (1,8 MHz)', 1810, 2000,
     [('cw', 1810, 1838, 'full'), ('dig', 1838, 1840, 'full'), ('dig', 1840, 1843, 'top'),
      ('fone', 1840, 1843, 'bot'), ('fone', 1843, 2000, 'full')], None),
    ('80 m (3,5 MHz)', 3500, 3800,
     [('cw', 3500, 3580, 'full'), ('dig', 3580, 3600, 'full'), ('dig', 3600, 3620, 'top'),
      ('fone', 3600, 3620, 'bot'), ('fone', 3620, 3800, 'full')], None),
    ('40 m (7 MHz)', 7000, 7200,
     [('cw', 7000, 7040, 'full'), ('dig', 7040, 7050, 'full'), ('dig', 7050, 7060, 'top'),
      ('fone', 7050, 7060, 'bot'), ('fone', 7060, 7200, 'full')], None),
    ('30 m (10 MHz)', 10100, 10150, [('cw', 10100, 10140, 'full'), ('dig', 10140, 10150, 'full')], None),
    ('20 m (14 MHz)', 14000, 14350,
     [('cw', 14000, 14070, 'full'), ('dig', 14070, 14099, 'full'), ('bcn', 14099, 14101, 'full'),
      ('fone', 14101, 14350, 'full')], 14100),
    ('17 m (18 MHz)', 18068, 18168,
     [('cw', 18068, 18095, 'full'), ('dig', 18095, 18109, 'full'), ('bcn', 18109, 18111, 'full'),
      ('fone', 18111, 18168, 'full')], 18110),
    ('15 m (21 MHz)', 21000, 21450,
     [('cw', 21000, 21070, 'full'), ('dig', 21070, 21120, 'full'), ('gap', 21120, 21149, 'full'),
      ('bcn', 21149, 21151, 'full'), ('fone', 21151, 21450, 'full')], 21150),
    ('12 m (24 MHz)', 24890, 24990,
     [('cw', 24890, 24915, 'full'), ('dig', 24915, 24929, 'full'), ('bcn', 24929, 24931, 'full'),
      ('fone', 24931, 24990, 'full')], 24930),
    ('10 m (28 MHz)', 28000, 29700,
     [('cw', 28000, 28070, 'full'), ('dig', 28070, 28190, 'full'), ('bcn', 28190, 28225, 'full'),
      ('fone', 28225, 29300, 'full'), ('sat', 29300, 29510, 'full'), ('gap', 29510, 29700, 'full')], 28200),
]


def kfmt(v):
    s = f'{v:,}'.replace(',', ' ')
    return s


def band_order():
    rh, bh = 50, 22
    f = F(78 + rh * len(HF) + 20)
    f.t(380, 22, 'Každé KV pásmo zdola nahoru: CW → digi → (maják) → FONE', size=16, w='bold', c=BL)
    legend(f, 20, 50, [('cw', 'CW'), ('dig', 'digitální'), ('bcn', 'maják IBP'), ('fone', 'FONE'),
                       ('sat', 'družice'), ('gap', 'ČTÚ neurčuje')])
    x0, x1 = 150, 740
    for i, (name, lo, hi, segs, bcn) in enumerate(HF):
        y = 82 + i * rh
        X = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
        f.t(10, y + 10, name, size=13, w='bold', anchor='start')
        f.t(10, y + 26, f'{kfmt(lo)}–{kfmt(hi)} kHz', size=11, c=GR, anchor='start')
        for k, a, b, part in segs:
            xa, xb = X(a), X(b)
            if k == 'bcn' and xb - xa < 5:
                m = (xa + xb) / 2; xa, xb = m - 2.5, m + 2.5
            yy, hh = {'full': (y, bh), 'top': (y, bh / 2), 'bot': (y + bh / 2, bh / 2)}[part]
            fill, tc = col(k)
            f.rect(xa, yy, xb - xa, hh, fill=fill, stroke='none', sw=0)
            lab = {'cw': 'CW', 'dig': 'digi', 'fone': 'FONE', 'sat': 'druž.'}.get(k)
            if lab and part == 'full' and xb - xa >= 34:
                f.t((xa + xb) / 2, y + 15.5, lab, size=11, c=tc, w='bold')
        f.rect(x0, y, x1 - x0, bh, stroke='#555555', sw=0.8)
        cw_end = segs[0][2]
        f.l(X(cw_end), y + bh, X(cw_end), y + bh + 5, c=CAT['cw'][0], w=1.4)
        f.t(X(cw_end) - 2, y + bh + 15, kfmt(cw_end), size=11, c=CAT['cw'][0], anchor='end', w='bold')
        fone = [a for k, a, b, p in segs if k == 'fone']
        if fone:
            fa = min(fone)
            f.l(X(fa), y + bh, X(fa), y + bh + 5, c=CAT['fone'][0], w=1.4)
            f.t(X(fa) + 2, y + bh + 15, kfmt(fa), size=11, c=CAT['fone'][0], anchor='start', w='bold')
        else:
            f.t(x1, y + bh + 15, 'bez FONE', size=11, c=RED, anchor='end', w='bold')
        if bcn:
            xb = X(bcn)
            f.a(f'<path d="M{xb - 5:.1f},{y - 8:.1f} L{xb + 5:.1f},{y - 8:.1f} L{xb:.1f},{y - 1:.1f} Z" fill="{CAT["bcn"][0]}"/>')
            f.t(xb + 8, y - 2, kfmt(bcn), size=10, c=CAT['bcn'][0], anchor='start')
    return (f.done(), f.w, f.h,
            'Pásma jsou natažena na stejnou šířku, aby bylo vidět opakující se pořadí. Modře konec CW (= začátek digi), zeleně '
            'začátek FONE, hnědý trojúhelník = maják IBP. Na 160, 80 a 40 m (1,8, 3,5, 7 MHz) se digi a FONE překrývají '
            '(pruh rozdělený napůl); na 30 m (10 MHz) FONE není. Úseky podle odpovědí ČTÚ (P a) 2–29), majáky podle IARU R1.')


# --------------------------------------------------------------- 2. SSB u okraje úseku / pásma
def ssb_edges():
    f = F(330)
    f.t(380, 22, 'SSB zabírá asi 3 kHz vedle nastaveného kmitočtu – nesmí vyčnívat ven', size=16, w='bold', c=BL)

    def label(x, y, s, c, size=12, anchor='middle'):
        wd = len(s) * size * 0.56
        xa = {'middle': x - wd / 2, 'start': x, 'end': x - wd}[anchor]
        f.rect(xa - 3, y - size, wd + 6, size + 5, fill='#ffffff', stroke='none', sw=0)
        f.t(x, y, s, size=size, c=c, w='bold', anchor=anchor)

    def panel(x0, w, lo, hi, strip, rows, title, edge, edge_lab):
        X = lambda v: x0 + w * (v - lo) / (hi - lo)
        f.t(x0 + w / 2, 52, title, size=14, w='bold')
        y = 64
        for k, a, b, part in strip:
            yy, hh = {'full': (y, 18), 'top': (y, 9), 'bot': (y + 9, 9)}[part]
            f.rect(X(max(a, lo)), yy, X(min(b, hi)) - X(max(a, lo)), hh, fill=col(k)[0], stroke='none', sw=0)
        f.rect(x0, y, w, 18, stroke='#555555', sw=0.8)
        for v in range(int(lo), int(hi) + 1, 2):
            f.l(X(v), 82, X(v), 87, c=GR, w=1)
        f.t(x0, 100, kfmt(int(lo)), size=10, c=GR, anchor='start')
        f.t(x0 + w, 100, kfmt(int(hi)), size=10, c=GR, anchor='end')
        f.l(X(edge), 60, X(edge), 290, c=RED, w=1.6, dash='5,4')
        for j, (car, lsb, ok, lab) in enumerate(rows):
            yb = 170 + j * 92
            f.l(x0, yb, x0 + w, yb, c=GR, w=1)
            a, b = (car - 3, car - 0.3) if lsb else (car + 0.3, car + 3)
            c = GRN if ok else RED
            pts = [(X(a), yb), (X(a), yb - 44), (X(b), yb - 44), (X(b), yb)]
            f.path(pts, c=c, w=1.8, fill=c, op=0.35, close=True)
            f.l(X(car), yb + 4, X(car), yb - 56, c=TX, w=2)
            # popisek nosné na straně, kde není spektrum
            if lsb:
                f.t(X(car) + 5, yb - 46, f'nosná {kfmt(car)}', size=11, anchor='start')
            else:
                f.t(X(car) - 5, yb - 46, f'nosná {kfmt(car)}', size=11, anchor='end')
            label(x0 + w / 2, yb + 20, lab, c)
        label(X(edge), 312, edge_lab, RED)

    panel(30, 330, 1832, 1850,
          [('cw', 1810, 1838, 'full'), ('dig', 1838, 1840, 'full'), ('dig', 1840, 1843, 'top'),
           ('fone', 1840, 1843, 'bot'), ('fone', 1843, 1850, 'full')],
          [(1840, True, False, '✗ LSB na 1 840: zasahuje pod 1 840 (CW/digi)'),
           (1843, True, True, '✓ LSB na 1 843: celé ve FONE úseku')],
          '160 m (1,8 MHz) – LSB leží pod nosnou', 1840, 'začátek FONE 1 840 kHz')
    panel(400, 330, 14338, 14356,
          [('fone', 14338, 14350, 'full'), ('gap', 14350, 14356, 'full')],
          [(14350, False, False, '✗ USB na 14 350: přesahuje okraj pásma'),
           (14347, False, True, '✓ USB na 14 347: končí na 14 350')],
          '20 m (14 MHz) – USB leží nad nosnou', 14350, 'konec pásma 14 350 kHz')
    return (f.done(), f.w, f.h,
            'Svislá čára = nastavený (nosný) kmitočet, plocha = obsazené pásmo hovoru (asi 0,3–3 kHz od nosné). Pod 10 MHz se '
            'používá LSB, nad 10 MHz USB. Proto „SSB nelze na 1 840 kHz“ a „USB nelze na 14,35 MHz“ (Př c) 26, 35); IARU '
            'doporučuje nastavit LSB nejníže na 1 843, 3 603 a 7 053 kHz a USB nejvýše 3 kHz pod horním okrajem pásma.')


# --------------------------------------------------------------- 3. výkony podle pásem
def powers():
    f = F(380)
    f.t(380, 22, 'Třída A: 750 W všude – méně jen v pásmech NIB', size=16, w='bold', c=BL)
    bars = [('1 810–1 850\nkHz', 750, 'P'), ('1 850–1 890\nkHz', 75, 'NIB'), ('1 890–2 000\nkHz', 10, 'NIB'),
            ('3,5–29,7\nMHz', 750, 'P / S'), ('50–52\nMHz', 25, 'NIB'), ('144 a 430\nMHz', 750, 'P'),
            ('1,24–10,5\nGHz', 750, 'S'), ('3 400–3 410\nMHz', 25, 'NIB')]
    x0, y0, h = 110, 300, 240          # y0 = osa (5 W), log. stupnice 5 W … 5 000 W
    Y = lambda p: y0 - h * (math.log10(p) - math.log10(5)) / 3
    for p in (10, 100, 1000):
        f.l(x0 - 6, Y(p), 740, Y(p), c='#dddddd', w=1)
        f.t(x0 - 10, Y(p) + 4, f'{kfmt(p)} W', size=11, c=GR, anchor='end')
    for p, lab in ((1500, '1 500 W – mezinárodní závod / EME v intravilánu'), (3000, '3 000 W – totéž mimo intravilán')):
        f.l(x0, Y(p), 740, Y(p), c=ORA, w=1.6, dash='6,4')
        f.t(740, Y(p) - 5, lab, size=11, c=ORA, anchor='end')
    bw, gap = 58, 20
    for i, (lab, p, st) in enumerate(bars):
        x = x0 + 12 + i * (bw + gap)
        c = BL if st != 'NIB' else RED
        f.rect(x, Y(p), bw, y0 - Y(p), fill=c, stroke=c, op=0.8)
        f.t(x + bw / 2, Y(p) - 6, f'{p} W', size=12, w='bold', c=c)
        f.t(x + bw / 2, y0 + 16, lab, size=10.5)
        f.t(x + bw / 2, y0 + 44, st, size=10.5, c=c, w='bold')
    f.l(x0, y0, 740, y0, w=1.4)
    f.t(380, 372, 'P = přednostní, S = podružné (obojí 750 W), NIB = na neinterferenční bázi (snížený výkon)', size=12, c=GR)
    return (f.done(), f.w, f.h,
            'Výkon v logaritmickém měřítku podle vyhl. 156/2005 Sb. (§ 4, příloha 1). Stačí si pamatovat výjimky NIB: '
            '160 m (1,8 MHz) nad 1 850 kHz 75 W a nad 1 890 kHz 10 W, 6 m (50 MHz) 25 W. Ostatní výkony: neobsluhovaná '
            'stanice 50 W, třída N 10 W (Př c) 12, 16–20, 44, 47, 48).')


# --------------------------------------------------------------- 4. anatomie volací značky
def callsign():
    f = F(330)
    f.t(380, 22, 'Jak číst volací značku', size=16, w='bold', c=BL)

    def parts(y, items):
        x = 380 - sum(w for _, w, _, _ in items) / 2
        for txt, w, c, note in items:
            f.rect(x, y, w - 6, 46, fill=c, stroke=c, rx=6, op=0.18)
            f.rect(x, y, w - 6, 46, stroke=c, rx=6)
            f.t(x + (w - 6) / 2, y + 32, txt, size=24, w='bold', c=c)
            f.t(x + (w - 6) / 2, y + 66, note, size=11.5, c=c)
            x += w

    parts(50, [('OK', 120, BL, 'prefix ČR\n(OK nebo OL)'), ('1', 120, ORA, 'číslice\n1, 2 = klubová\n0 = neobsluhovaná'),
               ('K', 120, GRN, 'klubová: 1. písmeno\nsufixu K, O nebo R'), ('XX', 120, GRN, 'sufix celkem 3 písmena\n'
                                                                                     '(neobsl.: 1–3)')])
    f.t(380, 172, '3písmenný sufix nesmí začínat Q (zaměnil by se s Q kódy)', size=12, c=RED, w='bold')
    parts(196, [('FK', 150, ORA, 'KDE JSEM\nprefix navštívené země\n(T/R 61-01)'), ('/', 30, GR, ''),
                ('DL1YD', 170, BL, 'KDO JSEM\nvlastní značka'), ('/', 30, GR, ''),
                ('p', 150, GRN, 'JAK VYSÍLÁM\n/p, /m, /mm, /am\n(v závodech nepovinné)')])
    return (f.done(), f.w, f.h,
            'Nahoře stavba české klubové a neobsluhované značky (Př c) 45, 46), dole značka při vysílání v cizině – '
            'FK/DL1YD/p = DL1YD vysílá přechodně z Nové Kaledonie (P c) 10; Př b) 2, 6; Př c) 5–7). Cizinec v ČR používá '
            'OK/vlastní značka.')


# --------------------------------------------------------------- 5. azimuty z Prahy
AZ = [(45, 'Japonsko'), (85, 'Austrálie'), (175, 'JAR'), (240, 'Argentina'), (280, 'Karibik'), (315, 'USA'), (355, 'Havaj')]


def azimuths():
    f = F(400)
    cx, cy, R = 300, 205, 140
    f.circle(cx, cy, R, fill=LIGHT, stroke=GR)
    for a in range(0, 360, 15):
        r2 = R - (12 if a % 45 == 0 else 6)
        ra = math.radians(a)
        f.l(cx + R * math.sin(ra), cy - R * math.cos(ra), cx + r2 * math.sin(ra), cy - r2 * math.cos(ra), c=GR, w=1)
    for a, lab in ((0, 'S'), (90, 'V'), (180, 'J'), (270, 'Z')):
        ra = math.radians(a)
        f.t(cx + (R - 26) * math.sin(ra), cy - (R - 26) * math.cos(ra) + 5, lab, size=14, w='bold', c=GR)
    for i, (a, lab) in enumerate(AZ):
        ra = math.radians(a)
        c = BL if i % 2 == 0 else RED
        f.arrow([(cx, cy), (cx + (R - 4) * math.sin(ra), cy - (R - 4) * math.cos(ra))], c=c, w=2.2)
        rl = R + 12
        lx, ly = cx + rl * math.sin(ra), cy - rl * math.cos(ra)
        anc = 'start' if math.sin(ra) > 0.25 else ('end' if math.sin(ra) < -0.25 else 'middle')
        f.t(lx, ly + (4 if abs(math.cos(ra)) < 0.5 else (-2 if math.cos(ra) > 0 else 14)), f'{lab} {a}°', size=12.5, w='bold', c=c, anchor=anc)
    f.circle(cx, cy, 5, fill=TX)
    f.t(cx + 10, cy + 18, 'Praha', size=12, anchor='start')
    # pořadí po směru hodin
    x = 530
    f.t(x, 50, 'Po směru hodinových ručiček:', size=14, w='bold', anchor='start', c=BL)
    for i, (a, lab) in enumerate(AZ):
        f.t(x + 40, 82 + i * 28, f'{a}°', size=14, w='bold', anchor='end', c=BL if i % 2 == 0 else RED)
        f.t(x + 52, 82 + i * 28, lab, size=14, anchor='start')
    f.t(x, 290, 'Přes vysoké zeměpisné šířky:', size=12, c=GR, anchor='start')
    f.t(x, 308, 'Havaj téměř na sever,', size=12, c=GR, anchor='start')
    f.t(x, 326, 'USA na severozápad,', size=12, c=GR, anchor='start')
    f.t(x, 344, 'Austrálie téměř na východ.', size=12, c=GR, anchor='start')
    return (f.done(), f.w, f.h,
            'Výchozí azimuty nejkratší cesty (ortodromy) z Prahy podle odpovědí ČTÚ (P c) 1–7), 0° = sever. Skutečné trasy '
            'na mapě jsou za otázkou c) 7.')


# --------------------------------------------------------------- 6. ELI – ICE a reaktance
def eli_ice():
    f = F(270)

    def waves(x0, title, lead_u, sub):
        w, y = 220, 132
        f.t(x0 + w / 2, 28, title, size=15, w='bold', c=BL)
        f.t(x0 + w / 2, 48, sub, size=12, c=GR)
        f.l(x0, y, x0 + w, y, c=GR, w=1)
        for name, ph, c in (('U', 0 if lead_u else -90, RED), ('I', -90 if lead_u else 0, BL)):
            pts = [(x0 + w * k / 200, y - 55 * math.sin(math.radians(720 * k / 200 + ph + 90))) for k in range(201)]
            f.path(pts, c=c, w=2.4)
        f.l(x0 + 30, 222, x0 + 50, 222, c=RED, w=2.4); f.t(x0 + 55, 226, 'U napětí', size=12, c=RED, anchor='start', w='bold')
        f.l(x0 + 125, 222, x0 + 145, 222, c=BL, w=2.4); f.t(x0 + 150, 226, 'I proud', size=12, c=BL, anchor='start', w='bold')
        f.t(x0 + w / 2, 254, ('napětí předbíhá proud o 90°' if lead_u else 'proud předbíhá napětí o 90°'), size=12.5, w='bold')

    waves(20, 'cívka L:  E-L-I', True, 'E (napětí) před I (proudem)')
    waves(270, 'kondenzátor C:  I-C-E', False, 'I (proud) před E (napětím)')
    # reaktance
    x0, y0, w, h = 540, 220, 200, 160
    f.t(x0 + w / 2, 28, 'reaktance a kmitočet', size=15, w='bold', c=BL)
    f.arrow([(x0, y0), (x0 + w, y0)], c=TX, w=1.4); f.arrow([(x0, y0), (x0, y0 - h)], c=TX, w=1.4)
    f.t(x0 + w, y0 + 18, 'f', size=13, anchor='end'); f.t(x0 - 6, y0 - h + 8, 'X', size=13, anchor='end')
    f.path([(x0 + 5 + k, y0 - 5 - 0.75 * k) for k in range(0, 190, 5)], c=RED, w=2.4)
    f.path([(x0 + 5 + k, y0 - min(150, 2600 / (k + 12))) for k in range(0, 190, 3)], c=BL, w=2.4)
    f.t(x0 + 160, y0 - 140, 'XL roste', size=12, c=RED, w='bold')
    f.t(x0 + 160, y0 - 28, 'XC klesá', size=12, c=BL, w='bold')
    xr = x0 + 5 + 52
    f.l(xr, y0, xr, y0 - 45, c=GR, dash='3,3', w=1)
    f.t(xr, y0 + 16, 'f₀', size=12, c=GR)
    f.t(x0 + w / 2, 254, 'rovnají se při rezonanci f₀', size=12.5, w='bold')
    return (f.done(), f.w, f.h,
            'Pomůcka ELI–ICE (E = napětí, I = proud): u cívky (L) je E před I, u kondenzátoru (C) je I před E. Reaktance cívky '
            's kmitočtem roste, kondenzátoru klesá (E b) 8–11).')


# --------------------------------------------------------------- 7. filtry na stanici
def filters():
    f = F(390)
    f.t(380, 22, 'Filtr se dává tam, kde je problém – a zadrží to, co ruší', size=16, w='bold', c=BL)

    def ant(x, y, c=TX):
        f.l(x, y, x, y - 34, c=c, w=2)
        f.path([(x - 14, y - 34), (x, y - 20), (x + 14, y - 34)], c=c, w=2)

    def resp(x0, y0, low_pass, mark):
        w, h = 210, 70
        f.arrow([(x0, y0), (x0 + w, y0)], c=TX, w=1.2); f.arrow([(x0, y0), (x0, y0 - h - 10)], c=TX, w=1.2)
        f.t(x0 + w, y0 + 16, 'f', size=12, anchor='end')
        fc = x0 + 95
        if low_pass:
            pts = [(x0, y0 - h), (fc - 10, y0 - h), (fc + 25, y0 - 4), (x0 + w - 10, y0 - 4)]
        else:
            pts = [(x0, y0 - 4), (fc - 25, y0 - 4), (fc + 10, y0 - h), (x0 + w - 10, y0 - h)]
        f.path(pts, c=BL, w=2.6)
        for xx, lab, ok in mark:
            c = GRN if ok else RED
            f.l(x0 + xx, y0, x0 + xx, y0 - h + 15, c=c, w=3)
            f.t(x0 + xx, y0 + 16, lab, size=11, c=c, w='bold')

    # 1. vysílač
    y = 70
    f.box(20, y, 90, 44, 'KV\nvysílač', size=13)
    f.arrow([(110, y + 22), (150, y + 22)], c=TX, w=1.8)
    f.box(150, y, 170, 44, 'hornofrekvenční zádrž\n(= dolní propust)', fill='#fdecea', stroke=RED, size=12)
    f.arrow([(320, y + 22), (360, y + 22)], c=TX, w=1.8)
    ant(378, y + 30); f.l(360, y + 22, 378, y + 22, w=1.8); f.l(378, y + 22, 378, y + 30, w=1.8)
    resp(500, y + 80, True, [(40, 'f ✓', True), (125, '2f ✗', False), (170, '3f ✗', False)])
    f.t(500, y - 2, 'propustí signál, zadrží harmonické (vyšší kmitočty)', size=11.5, anchor='start', c=GR)
    f.t(20, y + 70, 'E i) 1: nežádoucí vyzařování KV vysílače', size=12, anchor='start', c=RED, w='bold')
    f.t(20, y + 88, 'E c) 5: π filtr (C–L–C) je dolní propust', size=12, anchor='start', c=GR)
    # 2. televize
    y = 240
    ant(38, y + 8); f.l(38, y + 8, 38, y + 22, w=1.8)
    f.t(60, y - 18, 'TV anténa (+ silný KV signál)', size=11, anchor='start', c=GR)
    f.arrow([(38, y + 22), (150, y + 22)], c=TX, w=1.8)
    f.box(150, y, 170, 44, 'dolnofrekvenční zádrž\n(= horní propust)', fill='#fdecea', stroke=RED, size=12)
    f.arrow([(320, y + 22), (360, y + 22)], c=TX, w=1.8)
    f.box(360, y, 90, 44, 'televizor', size=13)
    resp(500, y + 80, False, [(40, 'KV ✗', False), (165, 'TV ✓', True)])
    f.t(500, y - 2, 'zadrží KV (nižší kmitočet), propustí TV', size=11.5, anchor='start', c=GR)
    f.t(20, y + 70, 'E i) 3: rušení televize silným KV signálem', size=12, anchor='start', c=RED, w='bold')
    return (f.done(), f.w, f.h,
            '„Propust“ propouští, „zádrž“ zadržuje; „dolno-/horno-“ říká, které kmitočty. Hornofrekvenční zádrž je totéž co '
            'dolní propust a naopak – liší se jen název (E i) 1, 3; E c) 5).')


# --------------------------------------------------------------- 8. dekády LF … SHF
def decades():
    f = F(310)
    f.t(380, 22, 'Kmitočtová pásma po dekádách: λ [m] = 300 / f [MHz]', size=16, w='bold', c=BL)
    x0, dw = 50, 110
    X = lambda mhz: x0 + dw * (math.log10(mhz) - math.log10(0.03))
    names = [('LF', 'kilometrové\n(DV)'), ('MF', 'hektometrové\n(SV)'), ('HF', 'dekametrové\n(KV)'),
             ('VHF', 'metrové\n(VKV)'), ('UHF', 'decimetrové'), ('SHF', 'centimetrové')]
    fills = ['#eceff1', '#cfd8dc', BLF, '#c8e6c9', '#ffe0b2', '#f8bbd0']
    for i, ((n, cz), fl) in enumerate(zip(names, fills)):
        x = x0 + i * dw
        f.rect(x, 50, dw, 46, fill=fl, stroke='#777777', sw=1)
        f.t(x + dw / 2, 78, n, size=17, w='bold')
        f.t(x + dw / 2, 114, cz, size=11, c=GR)
    edges = [('30 kHz', '10 km'), ('300 kHz', '1 km'), ('3 MHz', '100 m'), ('30 MHz', '10 m'),
             ('300 MHz', '1 m'), ('3 GHz', '10 cm'), ('30 GHz', '1 cm')]
    for i, (fr, lam) in enumerate(edges):
        x = x0 + i * dw
        f.l(x, 46, x, 168, c='#777777', w=1)
        f.t(x, 160, fr, size=11, w='bold')
        f.t(x, 176, lam, size=11, c=GR)
    ham = [(0.1357, '137 kHz'), (1.81, '1,8'), (3.5, '3,5'), (7.0, '7'), (10.1, '10'), (14.0, '14'), (18.07, '18'),
           (21.0, '21'), (24.89, '24'), (28.0, '28'), (50, '50'), (144, '144'), (430, '432'), (1240, '1 296'),
           (2300, '2 320'), (5650, '5 760'), (10000, '10 GHz')]
    for mhz, lab in ham:
        x = X(mhz)
        f.l(x, 204, x, 218, c=BL, w=2.2)
        if lab in ('10', '18', '21', '24'):
            continue
        f.t(x + 4, 226, lab, size=10.5, c=BL, rot=60, anchor='start')
    xa, xb = X(10.1), X(24.89)
    f.path([(xa, 201), (xa, 196), (xb, 196), (xb, 201)], c=BL, w=1.2)
    f.t((xa + xb) / 2, 191, '10, 18, 21, 24', size=10, c=BL)
    f.t(x0, 298, 'modře amatérská pásma (MHz) – VHF = very, UHF = ultra, SHF = super high frequency', size=12,
        c=GR, anchor='start')
    return (f.done(), f.w, f.h,
            'Každé pásmo je o dekádu (10×) výš než předchozí a jeho vlnové délky jsou 10× kratší; české názvy podle vlnové '
            'délky. Zkratky LF, VHF, UHF, SHF jsou otázky P e) 32, 82, 75, 14.')


# --------------------------------------------------------------- 9. bezpečnost: ss × stř
def safety():
    f = F(260)
    f.t(380, 22, 'Střídavý proud je nebezpečnější → pro střídavý vždy nižší limit', size=16, w='bold', c=BL)

    def group(x0, title, vals, unit, vmax):
        f.t(x0 + 140, 52, title, size=14, w='bold')
        y0, h = 210, 130
        for i, (lab, v, c) in enumerate(vals):
            x = x0 + 40 + i * 130
            hh = h * v / vmax
            f.rect(x, y0 - hh, 80, hh, fill=c, stroke=c, op=0.8)
            f.t(x + 40, y0 - hh - 8, f'{v} {unit}'.replace('.', ','), size=15, w='bold', c=c)
            f.t(x + 40, y0 + 18, lab, size=12.5)
        f.l(x0 + 20, y0, x0 + 280, y0, w=1.4)

    group(40, 'bezpečné napětí (E j) 1)', [('stejnosměrné', 60, BL), ('střídavé', 25, RED)], 'V', 60)
    group(420, 'bezpečný proud (E j) 6)', [('stejnosměrný', 10, BL), ('střídavý', 3.5, RED)], 'mA', 10)
    return (f.done(), f.w, f.h,
            'Hodnoty přesně podle odpovědí ČTÚ (jiné příručky někdy uvádějí jiná čísla – u zkoušky platí ČTÚ).')


BAND_FIG = band_order
FIGS = {
    'Rozdělení KV pásem (provoz a)': [ssb_edges],
    'Výkony a nežádoucí vyzařování (předpisy c)': [powers],
    'Volací značky a provozní pravidla (předpisy, provoz c)': [callsign],
    'Provozní dovednosti (provoz c)': [azimuths],
    'Zkratky (provoz e)': [decades],
    'Elektrotechnika (a–f, h)': [eli_ice, filters],
    'Bezpečnost a rušení (elektrotechnika i, j)': [safety],
}

if __name__ == '__main__':
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    allf = [BAND_FIG] + [fn for v in FIGS.values() for fn in v]
    for fn in allf:
        data, w, h, _ = fn()
        open(os.path.join(out, fn.__name__ + '.svg'), 'wb').write(data)
    print(len(allf), 'obrázků')
