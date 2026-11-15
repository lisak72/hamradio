# -*- coding: utf-8 -*-
"""Schematické grafy šíření rádiových vln (SVG bez externích knihoven).

generate() -> [(název, popis, svg_bytes, šířka_px, výška_px)]
Grafy jsou ilustrativní (typické hodnoty), nejde o měřená data. Odkazy [→ g) n] = otázky ČTÚ,
část Elektrotechnika, oddíl g) Šíření rádiových vln.
"""
import math
from xml.sax.saxutils import escape

W = 1000
FONT = 'font-family="Liberation Sans, Arial, sans-serif"'
C_BL, C_BLF, C_RED, C_GR, C_TX = '#2e5597', '#8fb0e0', '#c0392b', '#888888', '#222222'

INTRO = ('Schematické grafy znázorňují, jak se rádiové vlny šíří v závislosti na kmitočtu, denní době a sluneční '
         'činnosti. Hodnoty jsou typické a orientační – skutečné podmínky se mění podle ročního období, zeměpisné '
         'polohy a stavu ionosféry. Odkazy [→ g) n] vedou na otázky části 3, oddílu g) Šíření rádiových vln.')


class S:
    def __init__(self, h):
        self.h = h
        self.o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" {FONT} font-size="14">',
                  f'<rect x="0" y="0" width="{W}" height="{h}" fill="#ffffff"/>']

    def a(self, s): self.o.append(s)

    def t(self, x, y, s, c=C_TX, anchor='middle', size=14, w='normal', rot=None, italic=False):
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ''
        st = ' font-style="italic"' if italic else ''
        self.a(f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}"{st}{tr}>{escape(s)}</text>')

    def l(self, x1, y1, x2, y2, c=C_TX, w=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>')

    def path(self, pts, c=C_BL, w=2, fill='none', dash=None, op=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a('<path d="M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) +
               f'" stroke="{c}" stroke-width="{w}" fill="{fill}" fill-opacity="{op}"{d}/>')

    def arrow(self, pts, c=C_BL, w=2.5, dash=None):
        self.path(pts, c=c, w=w, dash=dash)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        a = math.atan2(y2 - y1, x2 - x1); L = 9 + w * 1.6; b = 0.42
        self.a(f'<polygon points="{x2:.1f},{y2:.1f} {x2 - L * math.cos(a - b):.1f},{y2 - L * math.sin(a - b):.1f} '
               f'{x2 - L * math.cos(a + b):.1f},{y2 - L * math.sin(a + b):.1f}" fill="{c}"/>')

    def mast(self, x, y, h=26, lab=None, anchor='middle'):
        self.l(x, y, x, y - h, C_TX, 3)
        self.l(x - 7, y - h, x + 7, y - h, C_TX, 2)
        if lab: self.t(x, y - h - 8, lab, size=12.5, w='bold', anchor=anchor)

    def rect(self, x, y, w, h, fill, op=1.0, stroke='none'):
        self.a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}"/>')

    def done(self):
        return '\n'.join(self.o + ['</svg>']).encode('utf-8')


BANDS = [('160 m', 1.85), ('80 m', 3.65), ('40 m', 7.1), ('30 m', 10.12), ('20 m', 14.2), ('17 m', 18.1), ('15 m', 21.2),
         ('12 m', 24.9), ('10 m', 28.5), ('6 m', 50.5), ('2 m', 145), ('70 cm', 435), ('23 cm', 1296), ('13 cm', 2320),
         ('6 cm', 5760), ('3 cm', 10368)]


# ---------------------------------------------------------------- 1. přehled druhů šíření podle kmitočtu
def g_overview():
    rows = [
        ('Přízemní vlna', [(1, 1), (3, .75), (10, .35), (30, .05)], C_BL, 'dosah klesá s kmitočtem'),
        ('Útlum ve vrstvě D (ve dne)', [(1, 1), (3, .8), (7, .45), (15, .12), (30, 0)], C_RED, 'pohlcuje nízká KV pásma'),
        ('Ionosférický odraz (F2)', [(1.8, .8), (7, 1), (21, 1), (30, .75), (50, .25), (60, 0)], C_BL, 'nad 30 MHz jen při max. slun. činnosti'),
        ('Sporadická vrstva Es (léto)', [(18, 0), (28, .7), (50, 1), (145, .55), (220, 0)], C_BL, ''),
        ('Meteorické stopy (MS)', [(25, 0), (28, .5), (50, 1), (145, .9), (435, .3), (500, 0)], C_BL, ''),
        ('Polární záře (aurora)', [(25, 0), (28, .4), (50, 1), (145, .9), (435, .3), (500, 0)], C_BL, ''),
        ('Troposféra (inverze, rozptyl)', [(40, 0), (50, .3), (145, .8), (435, 1), (10000, 1)], C_BL, ''),
        ('Přímá viditelnost', [(20, 0), (30, .5), (100, 1), (10000, 1)], C_BL, 'běžná spojení na VKV a UKV'),
        ('Odraz od Měsíce (EME)', [(45, 0), (50, .6), (145, 1), (10000, 1)], C_BL, 'pásma 6 m až 3 cm (50 MHz – 10 GHz)'),
    ]
    LX, X0, X1, top, rh = 245, 255, 975, 62, 32
    H = top + len(rows) * rh + 70
    s = S(H)
    fx = lambda f: X0 + math.log10(f) / 4 * (X1 - X0)
    # oblasti KV / VKV / UKV / SHF
    for (a, b, lab, c) in [(1, 3, 'SV', '#f2f2f2'), (3, 30, 'KV (HF)', '#e6eef9'), (30, 300, 'VKV (VHF)', '#f2f2f2'),
                           (300, 3000, 'UKV (UHF)', '#e6eef9'), (3000, 10000, 'SHF', '#f2f2f2')]:
        s.rect(fx(a), 6, fx(b) - fx(a), 22, c)
        s.t((fx(a) + fx(b)) / 2, 22, lab, size=12, w='bold')
    for f, lab in [(1, '1 MHz'), (3, '3'), (10, '10'), (30, '30'), (100, '100'), (300, '300'), (1000, '1 GHz'), (3000, '3'), (10000, '10 GHz')]:
        s.l(fx(f), 30, fx(f), 36)
        s.t(fx(f), 50, lab, size=12, anchor='start' if f == 1 else ('end' if f == 10000 else 'middle'))
    yb = top + len(rows) * rh
    for name, f in BANDS:
        s.l(fx(f), top - 4, fx(f), yb + 4, '#cccccc', 0.8, '2,3')
        s.t(fx(f) + 4, yb + 14, name, size=11, anchor='end', rot=-60)
    for i, (lab, pts, col, note) in enumerate(rows):
        y = top + i * rh
        s.t(LX, y + rh / 2 + 5, lab, anchor='end', size=13, w='bold')
        gid = f'g{i}'
        stops = ''.join(f'<stop offset="{(fx(f) - X0) / (X1 - X0):.4f}" stop-color="{col}" stop-opacity="{op:.2f}"/>' for f, op in pts)
        s.a(f'<defs><linearGradient id="{gid}" x1="{X0}" y1="0" x2="{X1}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="{pts[0][1] if pts[0][0] <= 1 else 0}"/>{stops}'
            f'<stop offset="1" stop-color="{col}" stop-opacity="{pts[-1][1]}"/></linearGradient></defs>')
        s.rect(X0, y + 5, X1 - X0, rh - 10, f'url(#{gid})')
        if note:
            fa = max(pts, key=lambda p: p[1])[0]
            xa = min(max(fx(fa), X0 + 120), X1 - 120)
            s.t(xa, y + rh / 2 + 4, note, c='#ffffff' if col == C_BL else '#ffffff', size=11.5, w='bold')
    return s.done(), H


# ---------------------------------------------------------------- 2. vrstvy ionosféry den / noc
def g_layers():
    H = 330
    s = S(H)
    y = lambda km: 300 - km * 0.62
    for km in range(0, 451, 50):
        s.l(95, y(km), 965, y(km), '#eeeeee', 0.8)
        s.t(85, y(km) + 5, f'{km} km', anchor='end', size=12)
    s.l(95, y(0), 965, y(0), C_TX, 1.5)
    s.rect(95, y(0), 870, 10, '#9c7b4f', 0.5)
    cols = [(115, 515, 'DEN', [('D', 60, 90, .9, '60–90 km – pohlcuje (tlumí) nízké kmitočty'),
                               ('E', 90, 140, .75, '≈ 100–120 km – odráží hlavně nižší KV pásma'),
                               ('F1', 160, 230, .6, '≈ 200 km – jen ve dne'),
                               ('F2', 250, 400, .9, '≈ 250–400 km – dálková spojení')]),
            (555, 955, 'NOC', [('E', 95, 130, .25, 'slabá zbytková ionizace'),
                               ('F', 250, 400, .7, 'F1 a F2 splývají v jednu vrstvu F')])]
    for x0, x1, lab, layers in cols:
        s.t((x0 + x1) / 2, 22, lab, size=16, w='bold', c='#7f4f00' if lab == 'DEN' else '#1f3864')
        for name, a, b, op, note in layers:
            s.rect(x0, y(b), x1 - x0, y(a) - y(b), C_BL if name != 'D' else C_RED, op * 0.55)
            s.t(x0 + 22, (y(a) + y(b)) / 2 + 6, name, size=17, w='bold', c='#ffffff' if op > .5 else C_TX)
            s.t(x0 + 55, (y(a) + y(b)) / 2 + 5, note, anchor='start', size=12)
    s.t(735, y(75) + 5, 'vrstva D v noci zaniká', size=12, italic=True, c=C_GR)
    return s.done(), H


# ---------------------------------------------------------------- 3. prostorová vlna, pásmo ticha
def g_skip():
    H = 330
    s = S(H)
    CX, CY, RE, RI1, RI2 = 500, 2620, 2420, 2520, 2565

    def pt(r, th): return CX + r * math.sin(th), CY - r * math.cos(th)

    def arc(r, a, b, n=80): return [pt(r, a + (b - a) * i / n) for i in range(n + 1)]

    A, B = -0.205, 0.205
    s.path(arc(RI2, A, B) + list(reversed(arc(RI1, A, B))), c='none', fill=C_BLF, op=.6, w=0)
    s.t(*pt(RI2 + 10, 0.13), 'ionosféra (vrstva F2)', size=13, w='bold', c=C_BL)
    ground = arc(RE, A, B) + [(1000, H), (0, H)]
    s.path(ground, c='#7a5c3a', w=2, fill='#d9c7a8', op=.8)
    t0 = -0.185
    tx = pt(RE, t0)
    s.l(tx[0], tx[1], tx[0], tx[1] - 28, C_TX, 3)
    s.t(tx[0] + 2, tx[1] - 34, 'vysílač', size=13, w='bold', anchor='start')
    # přízemní vlna
    s.path(arc(RE + 4, t0, t0 + 0.07, 20), c=C_RED, w=5)
    gx, gy = pt(RE - 40, t0 + 0.04)
    s.t(gx, gy, 'přízemní vlna', c=C_RED, size=13, w='bold')
    # paprsky: (bod odrazu, projde?)
    rays = [(-0.115, True), (-0.05, False), (0.0, False)]
    land = []
    for th, through in rays:
        r = pt(RI1 + (8 if not through else 0), th)
        if through:
            out = pt(RI2 + 30, th + 0.03)
            s.path([tx, r], c=C_GR, w=2, dash='7,5')
            s.path([r, out], c=C_GR, w=2, dash='7,5')
            s.t(out[0] - 10, out[1] + 4, 'f > MUF – vlna projde', c=C_GR, size=12.5, w='bold', anchor='end')
        else:
            l2 = pt(RE, 2 * th - t0)
            s.path([tx, r, l2], c=C_BL, w=2.5)
            land.append(2 * th - t0)
    # pásmo ticha
    s.path(arc(RE + 4, t0 + 0.07, land[0], 40), c='#e67e22', w=6)
    zx, zy = pt(RE - 40, (t0 + 0.07 + land[0]) / 2)
    s.t(zx, zy, 'pásmo ticha (mrtvé pásmo)', c='#b9580c', size=13, w='bold')
    s.path(arc(RE + 4, land[0], land[1], 40), c=C_BL, w=6)
    px, py = pt(RE - 40, (land[0] + land[1]) / 2)
    s.t(px, py, 'příjem prostorové vlny (1. skok)', c=C_BL, size=13, w='bold')
    mx, my = pt(RI1 - 45, 0.05)
    s.t(mx + 20, my, 'f < MUF – část energie se vrátí k Zemi', c=C_BL, size=12.5, w='bold', anchor='start')
    return s.done(), H


# ---------------------------------------------------------------- 4. MUF / LUF během dne
def g_muf():
    H = 340
    s = S(H)
    X0, X1, Y0, Y1 = 80, 900, 300, 25
    fx = lambda h: X0 + h / 24 * (X1 - X0)
    fy = lambda f: Y0 - f / 32 * (Y0 - Y1)

    def day(t):
        x = (t - 5.5) / 14.5
        return math.sin(math.pi * x) if 0 < x < 1 else 0.0
    muf = lambda t: 7.5 + 16.5 * day(t) ** 0.7
    luf = lambda t: 1.6 + 5.4 * day(t) ** 1.2
    s.rect(fx(0), Y1, fx(5.5) - fx(0), Y0 - Y1, '#e9ecf3')
    s.rect(fx(20), Y1, fx(24) - fx(20), Y0 - Y1, '#e9ecf3')
    s.t(fx(2.75), Y1 + 18, 'noc', c=C_GR, size=13, w='bold')
    s.t(fx(22), Y1 + 18, 'noc', c=C_GR, size=13, w='bold')
    s.t(fx(12.75), Y1 + 18, 'den', c='#7f4f00', size=13, w='bold')
    ts = [i / 10 for i in range(241)]
    s.path([(fx(t), fy(muf(t))) for t in ts] + [(fx(t), fy(luf(t))) for t in reversed(ts)], c='none', fill='#cfe3c8', op=.8, w=0)
    s.path([(fx(t), fy(muf(t))) for t in ts], c=C_RED, w=3)
    s.path([(fx(t), fy(0.85 * muf(t))) for t in ts], c=C_RED, w=1.5, dash='6,4')
    s.path([(fx(t), fy(luf(t))) for t in ts], c=C_BL, w=3)
    for name, f in BANDS[:9]:
        s.l(X0, fy(f), X1, fy(f), '#999999', 0.8, '3,3')
        s.t(X1 + 8, fy(f) + 4, f'{name} ({f:g} MHz)'.replace('.', ','), anchor='start', size=11.5)
    for h in range(0, 25, 3):
        s.l(fx(h), Y0, fx(h), Y0 + 6)
        s.t(fx(h), Y0 + 21, f'{h} h', size=12)
    for f in range(0, 33, 5):
        s.l(X0 - 6, fy(f), X0, fy(f))
        s.t(X0 - 10, fy(f) + 4, str(f), anchor='end', size=12)
    s.l(X0, Y0, X1, Y0, C_TX, 1.5)
    s.l(X0, Y0, X0, Y1, C_TX, 1.5)
    s.t(22, (Y0 + Y1) / 2, 'kmitočet (MHz)', rot=-90, size=12)
    s.t((X0 + X1) / 2, Y0 + 38, 'místní čas', size=12)
    s.t(fx(12.75), fy(muf(12.75)) - 8, 'MUF', c=C_RED, size=14, w='bold')
    s.t(fx(16.8), fy(0.85 * muf(16.8)) + 16, 'FOT ≈ 0,85 MUF', c=C_RED, size=12, w='bold')
    s.t(fx(12.75), fy(luf(12.75)) + 18, 'LUF', c=C_BL, size=14, w='bold')
    s.t(fx(10.5), fy(11.5), 'použitelné kmitočty', c='#2f6b22', size=13, w='bold')
    return s.done(), H


# ---------------------------------------------------------------- 5. sluneční cyklus
def g_cycle():
    H = 300
    s = S(H)
    X0, X1, Y0, Y1 = 80, 960, 255, 30
    T0, T1 = 1995, 2033
    fx = lambda t: X0 + (t - T0) / (T1 - T0) * (X1 - X0)
    fy = lambda v: Y0 - v / 200 * (Y0 - Y1)
    # (minimum, maximum, hodnota max, další minimum) – přibližné vyhlazené hodnoty
    cyc = [(1996.4, 2001.9, 180, 2008.9, '23'), (2008.9, 2014.3, 116, 2019.9, '24'), (2019.9, 2024.8, 161, 2030.8, '25')]
    pts = []
    for a, m, v, b, _ in cyc:
        for i in range(60):
            t = a + (m - a) * i / 60
            pts.append((t, 3 + (v - 3) * math.sin(math.pi / 2 * (t - a) / (m - a)) ** 2))
        for i in range(60):
            t = m + (b - m) * i / 60
            pts.append((t, 3 + (v - 3) * math.cos(math.pi / 2 * (t - m) / (b - m)) ** 2))
    pts = [(1995, 15)] + [p for p in pts if p[0] > 1995.2]
    now = 2026.9
    s.rect(fx(now), Y1, X1 - fx(now), Y0 - Y1, '#f3f3f3')
    s.t((fx(now) + X1) / 2, Y1 + 16, 'předpověď', c=C_GR, size=12, italic=True)
    past = [(fx(t), fy(v)) for t, v in pts if t <= now]
    fut = [(fx(t), fy(v)) for t, v in pts if t >= now - 0.1]
    s.path(past + [(past[-1][0], Y0), (past[0][0], Y0)], c='none', fill=C_BLF, op=.6, w=0)
    s.path(past, c=C_BL, w=2.5)
    s.path(fut, c=C_BL, w=2.5, dash='7,5')
    for a, m, v, b, n in cyc:
        s.t(fx(m), fy(v) - 10, f'cyklus {n} (max. {int(m)})', size=12.5, w='bold', c=C_BL)
    for yr in range(1995, 2034, 5):
        s.l(fx(yr), Y0, fx(yr), Y0 + 6)
        s.t(fx(yr), Y0 + 21, str(yr), size=12)
    for v in range(0, 201, 50):
        s.l(X0 - 6, fy(v), X0, fy(v))
        s.t(X0 - 10, fy(v) + 4, str(v), anchor='end', size=12)
    s.l(X0, Y0, X1, Y0, C_TX, 1.5)
    s.l(X0, Y0, X0, Y1, C_TX, 1.5)
    s.t(22, (Y0 + Y1) / 2, 'číslo slunečních skvrn', rot=-90, size=12)
    a, b = fx(2008.9), fx(2019.9)
    s.l(a, Y0 - 25, b, Y0 - 25, C_RED, 1.5)
    for x in (a, b): s.l(x, Y0 - 32, x, Y0 - 18, C_RED, 1.5)
    s.t((a + b) / 2, Y0 - 31, '≈ 11 let', c=C_RED, size=13, w='bold')
    return s.done(), H


# ---------------------------------------------------------------- 6. intenzita pole a vzdálenost
def g_distance():
    H = 280
    s = S(H)
    X0, X1, Y0, Y1 = 80, 940, 235, 25
    fx = lambda d: X0 + (d - 0.5) / 7.5 * (X1 - X0)
    fy = lambda v: Y0 - v / 1.05 * (Y0 - Y1)
    ds = [1 + i / 50 for i in range(351)]
    s.path([(fx(d), fy(1 / d)) for d in ds], c=C_BL, w=3)
    s.path([(fx(d), fy(1 / d ** 2)) for d in ds], c=C_RED, w=2.5, dash='7,5')
    for d in (1, 2, 4):
        s.a(f'<circle cx="{fx(d):.1f}" cy="{fy(1 / d):.1f}" r="4.5" fill="{C_BL}"/>')
        s.t(fx(d) + 8, fy(1 / d) - 8, {1: 'E', 2: 'E/2 (−6 dB)', 4: 'E/4 (−12 dB)'}[d], anchor='start', size=12.5, w='bold', c=C_BL)
    s.t(fx(6.2), fy(1 / 6.2) - 12, 'intenzita pole E ~ 1/d', c=C_BL, size=13, w='bold')
    s.t(fx(5.0), fy(0.075), 'hustota výkonu S ~ 1/d²', c=C_RED, size=13, w='bold', anchor='start')
    for d in range(1, 9):
        s.l(fx(d), Y0, fx(d), Y0 + 6)
        s.t(fx(d), Y0 + 21, f'{d}d' if d > 1 else 'd', size=12)
    s.l(X0, Y0, X1, Y0, C_TX, 1.5)
    s.l(X0, Y0, X0, Y1, C_TX, 1.5)
    s.t(22, (Y0 + Y1) / 2, 'relativní velikost', rot=-90, size=12)
    s.t((X0 + X1) / 2, Y0 + 40, 'vzdálenost od antény (ve vzdálené zóně, d > 10 λ)', size=12)
    return s.done(), H


# ---------------------------------------------------------------- názorné scény
def g_los():
    H = 270
    s = S(H)
    CX, CY, R = 500, 1010, 900

    def pt(r, th): return CX + r * math.sin(th), CY - r * math.cos(th)
    arc = [pt(R, -0.56 + 1.12 * i / 100) for i in range(101)]
    s.path(arc + [(1000, H), (0, H)], c='#7a5c3a', w=2, fill='#d9c7a8', op=.8)
    hA = 40
    a0, b0, c0 = -0.42, -0.25, 0.35
    A, B, C = pt(R + hA, a0), pt(R + 25, b0), pt(R + 25, c0)
    s.mast(*pt(R, a0), hA, 'A')
    s.mast(*pt(R, b0), 25, 'B')
    s.mast(*pt(R, c0), 25, 'C')
    s.arrow([A, B], c='#2f8a2f', w=3)
    s.t((A[0] + B[0]) / 2 + 6, (A[1] + B[1]) / 2 - 12, 'přímá viditelnost', c='#2f8a2f', size=13, w='bold')
    th = a0 + math.acos(R / (R + hA))
    T = pt(R, th)
    far = (A[0] + (T[0] - A[0]) * 2.4, A[1] + (T[1] - A[1]) * 2.4)
    s.path([A, far], c=C_GR, w=1.8, dash='7,5')
    s.a(f'<circle cx="{T[0]:.1f}" cy="{T[1]:.1f}" r="5" fill="#e67e22"/>')
    s.t(T[0], T[1] + 50, 'radiohorizont stanice A', c='#b9580c', size=12.5, w='bold')
    s.t(far[0] + 6, far[1] - 8, 'dál vlna pokračuje přímo do prostoru', c=C_GR, size=12, anchor='end')
    s.path([A, C], c=C_RED, w=2, dash='5,4')
    s.t(C[0] - 20, C[1] + 55, 'stanice C je za horizontem –', c=C_RED, size=12.5, w='bold')
    s.t(C[0] - 20, C[1] + 71, 'zakrývá ji zakřivení Země', c=C_RED, size=12.5, w='bold')
    return s.done(), H


def g_obstacles():
    H = 300
    s = S(H)
    G = 262
    titles = ['Odraz', 'Ohyb (difrakce)', 'Průchod překážkou']
    for k, tt in enumerate(titles):
        ox = 10 + k * 335
        s.t(ox + 158, 22, tt, size=15, w='bold', c='#1f3864')
        s.l(ox, G, ox + 315, G, '#7a5c3a', 2)
        if k < 2:
            s.l(ox + 325, 10, ox + 325, H - 10, '#dddddd', 1)
    # 1 odraz od budovy
    ox = 10
    s.rect(ox + 225, 85, 60, G - 85, '#b9b9b9', 1, '#777777')
    for yy in range(100, G - 20, 28):
        for xx in (ox + 235, ox + 260):
            s.rect(xx, yy, 14, 14, '#eef3fb')
    s.mast(ox + 30, G, 30, 'vysílač')
    s.arrow([(ox + 30, G - 30), (ox + 225, 150)], c=C_BL, w=3)
    s.arrow([(ox + 225, 150), (ox + 70, 98)], c=C_BL, w=2.5)
    s.t(ox + 100, 70, 'odražená vlna', c=C_BL, size=12.5, w='bold')
    s.t(ox + 120, G + 20, 'budovy a kopce odrážejí hlavně VKV/UKV;', size=11.5)
    s.t(ox + 120, G + 34, 'více cest → úniky, „flutter“', size=11.5)
    # 2 ohyb za hranou kopce
    ox = 345
    s.path([(ox + 95, G), (ox + 165, 95), (ox + 235, G)], c='#7a5c3a', w=2, fill='#d9c7a8', op=.9)
    s.mast(ox + 25, G, 30, 'vysílač')
    s.arrow([(ox + 25, G - 30), (ox + 165, 97)], c=C_BL, w=3)
    for (ex, ey, w, d) in [(ox + 312, 60, 2.5, None), (ox + 312, 140, 2.2, None), (ox + 300, 205, 1.6, '6,4'), (ox + 262, 245, 1.2, '4,4')]:
        s.arrow([(ox + 165, 97), (ex, ey)], c=C_BL, w=w, dash=d)
    s.t(ox + 268, 236, 'stín –', c=C_GR, size=12, w='bold')
    s.t(ox + 268, 250, 'slabší signál', c=C_GR, size=12, w='bold')
    s.t(ox + 158, G + 20, 'vlna se ohýbá za hranu překážky;', size=11.5)
    s.t(ox + 158, G + 34, 'čím nižší kmitočet, tím výraznější ohyb', size=11.5)
    # 3 průchod zdí
    ox = 680
    s.rect(ox + 150, 55, 30, G - 55, '#a0a0a0', 1, '#666666')
    s.t(ox + 165, 48, 'zeď', size=12, w='bold')
    s.arrow([(ox + 15, 110), (ox + 148, 110)], c=C_BL, w=6)
    s.arrow([(ox + 182, 110), (ox + 310, 110)], c=C_BL, w=5)
    s.t(ox + 80, 96, 'KV', c=C_BL, size=14, w='bold')
    s.t(ox + 245, 96, 'malý útlum', c=C_BL, size=12, w='bold')
    s.arrow([(ox + 15, 200), (ox + 148, 200)], c=C_RED, w=6)
    s.arrow([(ox + 182, 200), (ox + 290, 200)], c=C_RED, w=1.5, dash='5,4')
    s.arrow([(ox + 148, 205), (ox + 70, 238)], c=C_RED, w=2)
    s.t(ox + 80, 186, 'UKV / GHz', c=C_RED, size=14, w='bold')
    s.t(ox + 245, 186, 'velký útlum', c=C_RED, size=12, w='bold')
    s.t(ox + 52, 252, 'část se odrazí', c=C_RED, size=11.5, anchor='start')
    s.t(ox + 158, G + 20, 'útlum stěn, stromů a deště roste', size=11.5)
    s.t(ox + 158, G + 34, 's kmitočtem', size=11.5)
    return s.done(), H


def g_tropo():
    H = 270
    s = S(H)
    G, L = 235, 105
    s.rect(0, L - 32, W, 32, '#f6d7b0', .9)
    s.t(990, L - 12, 'teplotní inverze – teplý vzduch nad studeným', anchor='end', size=12.5, w='bold', c='#9a5a14')
    s.rect(0, G, W, H - G, '#d9c7a8', .8)
    s.l(0, G, W, G, '#7a5c3a', 2)
    s.mast(50, G, 28, 'vysílač')
    pts = []
    for i in range(0, 361):
        x = 50 + i * 2.45
        pts.append((x, G - 28 + (28 - (G - L)) * abs(math.sin(math.pi * (x - 50) / 250)) if x < 175 else
                    G - (G - L) * abs(math.sin(math.pi * (x - 50) / 250))))
    s.arrow(pts, c=C_BL, w=3)
    s.mast(930, G, 28, 'příjem')
    s.arrow([(50, G - 28), (330, 18)], c=C_GR, w=1.8, dash='7,5')
    s.t(340, 30, 'bez inverze vlna uniká do prostoru', c=C_GR, size=12, anchor='start')
    s.t(500, G + 22, 'troposférický kanál (dukt) – vlna se láme zpět k Zemi; VKV/UKV spojení na stovky až tisíce km', size=12.5, w='bold', c=C_BL)
    return s.done(), H


def g_special():
    H = 330
    s = S(H)
    G = 290
    s.rect(0, G, W, H - G, '#d9c7a8', .8)
    s.l(0, G, W, G, '#7a5c3a', 2)
    A, B = (300, G - 26), (720, G - 26)
    s.mast(300, G, 26, 'A')
    s.mast(720, G, 26, 'B')
    # Měsíc
    s.a('<circle cx="935" cy="52" r="34" fill="#dddddd" stroke="#999999" stroke-width="1.5"/>')
    s.t(935, 57, 'Měsíc', size=12.5, w='bold')
    s.arrow([A, (903, 66)], c=C_GR, w=1.6)
    s.arrow([(903, 66), B], c=C_GR, w=1.6)
    s.t(870, 110, 'EME', c='#555555', size=14, w='bold')
    # družice
    s.rect(590, 52, 26, 14, '#7d3c98')
    s.l(578, 59, 628, 59, '#7d3c98', 2)
    s.arrow([A, (595, 68)], c='#7d3c98', w=2)
    s.arrow([(603, 68), B], c='#7d3c98', w=2)
    s.t(603, 40, 'družice (Dopplerův jev)', c='#7d3c98', size=12.5, w='bold')
    # meteorická stopa
    s.l(470, 150, 530, 128, '#e67e22', 5)
    s.arrow([A, (495, 141)], c='#e67e22', w=2)
    s.arrow([(500, 139), B], c='#e67e22', w=2)
    s.t(540, 160, 'ionizovaná stopa meteoru (MS)', c='#b9580c', size=12.5, w='bold', anchor='start')
    # polární záře
    for k in range(5):
        x = 40 + k * 22
        s.path([(x + 10 * math.sin(j / 3), 50 + j * 6) for j in range(18)], c='#27ae60', w=4, op=.7)
    s.t(100, 40, 'polární záře (sever)', c='#1e8449', size=12.5, w='bold')
    s.arrow([A, (150, 130)], c='#27ae60', w=2, dash='6,4')
    s.arrow([(150, 130), (B[0] - 8, B[1] - 4)], c='#27ae60', w=2, dash='6,4')
    s.t(20, 215, 'aurora – signál zní chraptivě', anchor='start', c='#1e8449', size=12, w='bold')
    s.t(500, G + 26, 'Obvyklé na VKV/UKV: EME (6 m – 3 cm, tj. 50 MHz – 10 GHz), odrazy od meteorických stop a polární záře, spojení přes družice', size=12)
    return s.done(), H


PANELS = [
    ('Přímá viditelnost a radiohorizont', g_los,
     'Na VKV a UKV se vlny šíří přímočaře podobně jako světlo, ionosféra je neodráží. Běžná spojení v pásmech 2 m (144–146 MHz) a 70 cm (430–440 MHz) '
     'proto vyžadují přímou viditelnost obou antén [→ g) 4]. Dosah omezuje zakřivení Země – radiohorizont je díky '
     'mírnému ohybu v atmosféře asi o 15 % dál než optický, přibližně d ≈ 4,1·(√h₁ + √h₂) km (výšky antén v metrech). '
     'Proto se na VKV vysílá z kopců a antény se umisťují co nejvýš. Zakřivení Země je zveličeno.'),
    ('Odraz, ohyb a průchod překážkou', g_obstacles,
     'Odraz: rovné plochy (budovy, skály, kopce) vlnu odrážejí – přijímač pak dostává signál několika cestami a ty se '
     'sčítají nebo ruší (úniky, kolísání signálu za jízdy). Ohyb (difrakce): za hranou kopce vlna částečně zatáčí '
     'do stínu, takže i za překážkou bývá slabý signál; nižší kmitočty se ohýbají výrazněji. Průchod: zdi, stromy '
     'a déšť tlumí vlny tím víc, čím vyšší je kmitočet – KV projde budovou téměř bez útlumu, na UKV a v pásmech GHz '
     'je útlum velký a část energie se odrazí.'),
    ('Troposférický kanál (inverze)', g_tropo,
     'Při teplotní inverzi (teplejší a sušší vzduch nad studeným, typicky za klidného anticyklonálního počasí) se vlny '
     'VKV a UKV lámou zpět k Zemi a mohou se šířit vrstvou atmosféry jako vlnovodem na stovky až tisíce kilometrů. '
     'Bez inverze by vlna odešla nad horizont do prostoru.'),
    ('Zvláštní druhy šíření na VKV a UKV', g_special,
     'Odraz od Měsíce (EME) se zpravidla uskutečňuje v pásmech 6 m až 3 cm (50 MHz až 10 GHz) [→ g) 16] a vyžaduje velké antény a výkon. '
     'Odrazy od ionizovaných stop meteorů (meteor scatter) trvají zlomky sekundy až sekundy. Při polární záři se signál '
     'odráží od ionizace na severu – antény se směrují k severu a signál zní chraptivě. Při provozu přes družice se '
     'kvůli jejich pohybu mění přijímaný kmitočet – Dopplerův jev [→ g) 17].'),
    ('Druhy šíření podle kmitočtu', g_overview,
     'Sytost barvy vyjadřuje, jak výrazně se daný druh šíření v příslušné části spektra uplatňuje; svislé čárkované '
     'čáry jsou radioamatérská pásma. Na nízkých KV kmitočtech převládá přízemní vlna a ve dne silný útlum ve vrstvě D, '
     'proto jsou pásma 160, 80 a 40 m (1,8; 3,5 a 7 MHz) vhodná pro dálková spojení hlavně v noci [→ g) 3]. Na KV probíhají dálková spojení '
     'odrazem od ionosféry (vrstva F2); při velkém počtu slunečních skvrn jsou použitelné i kmitočty nad 40 MHz [→ g) 5]. '
     'Na VKV a UKV se běžně spojuje přímou viditelností [→ g) 4], dálková spojení umožňují troposférické podmínky, '
     'sporadická vrstva E, odrazy od meteorických stop a polární záře a odraz od Měsíce (EME, pásma 6 m až 3 cm, tj. 50 MHz až 10 GHz) [→ g) 16]. '
     'Mimo přízemní vlnu a přímý paprsek ovlivňuje šíření sluneční aktivita [→ g) 6].'),
    ('Vrstvy ionosféry ve dne a v noci', g_layers,
     'Ionosféra je ionizována slunečním zářením. Vrstvy se směrem od povrchu Země označují D, E, F1, F2 [→ g) 1]. '
     'Vrstva D (60–90 km) existuje jen ve dne a nízké kmitočty pohlcuje. Vrstva E leží průměrně ve výšce asi 100 km '
     '[→ g) 13]. Nejvyšší vrstva F2 umožňuje nejdelší skok, a je proto pro dálková spojení nejdůležitější [→ g) 14]. '
     'V noci vrstva D zaniká a F1 a F2 splývají, proto se nízká pásma v noci „otevírají“.'),
    ('Prostorová vlna, skok a pásmo ticha', g_skip,
     'Vlna o kmitočtu nižším než MUF se v ionosféře lomí a její část se vrací k Zemi [→ g) 7]. Strmě vyslaná vlna '
     'o kmitočtu vyšším než kritický ionosférou projde. Mezi koncem dosahu přízemní vlny a místem dopadu první '
     'prostorové vlny vzniká pásmo ticha, kde stanici neslyšíme. Rozptyl (scatter) umožňuje příjem i v této oblasti – '
     'tedy dál, než dosáhne přízemní vlna, a blíž, než dopadá vlna odražená od ionosféry [→ g) 12]. Rozptýlená energie '
     'přichází po různých drahách, proto signál zní zkresleně [→ g) 11]. Zakřivení Země a výšky vrstev jsou zveličeny.'),
    ('Denní průběh MUF a LUF', g_muf,
     'MUF (Maximum Usable Frequency) je nejvyšší kmitočet, který se na dané trase ještě odrazí od ionosféry. LUF (Lowest '
     'Usable Frequency) je nejnižší použitelný kmitočet – pod ním je útlum ve vrstvě D příliš velký. Spojení je možné '
     'v pásmu mezi LUF a MUF (zeleně). Nejvýhodnější je pracovní kmitočet FOT ≈ 0,85 MUF: je-li MUF pro trasu '
     'Praha–Tokio 17 MHz, nejlepší podmínky nabízí pásmo 20 m (14 MHz) [→ g) 10]. Ve dne MUF stoupá a otevírají se '
     'vyšší pásma (20–10 m, tj. 14–29,7 MHz), v noci klesá a použitelná jsou nízká pásma (160–40 m, tj. 1,8–7,2 MHz) [→ g) 3]. Průběh je pro střední '
     'zeměpisné šířky a střední sluneční činnost.'),
    ('Jedenáctiletý cyklus sluneční činnosti', g_cycle,
     'Počet slunečních skvrn (a s ním ionizace ionosféry a MUF) kolísá s periodou asi 11 let [→ g) 2]. V maximu cyklu '
     'bývají otevřena i pásma 10 m (28–29,7 MHz) a 6 m (50–52 MHz) a použitelné jsou kmitočty nad 40 MHz [→ g) 5]; v minimu jsou vyšší KV pásma '
     'často „mrtvá“. Maximum 25. cyklu nastalo v roce 2024, příští minimum se očekává kolem roku 2030. Geomagnetické '
     'bouře (po slunečních erupcích) šíření na KV zhoršují [→ g) 8]. Hodnoty jsou přibližné vyhlazené hodnoty.'),
    ('Pokles intenzity pole se vzdáleností', g_distance,
     'Ve volném prostoru ve vzdálenosti větší než asi 10 λ klesá intenzita elektromagnetického pole E nepřímo úměrně '
     'vzdálenosti (E ~ 1/d) – dvojnásobná vzdálenost znamená poloviční intenzitu, tj. pokles o 6 dB [→ g) 15; ČTÚ to '
     'formuluje jako lineární závislost na vzdálenosti]. Hustota výkonu S klesá se čtvercem vzdálenosti (S ~ 1/d²).'),
]


def generate():
    out = []
    for title, fn, desc in PANELS:
        data, h = fn()
        out.append((title, desc, data, W, h))
    return out
