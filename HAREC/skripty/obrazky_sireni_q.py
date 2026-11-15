# -*- coding: utf-8 -*-
"""Názorné obrázky k otázkám Elektrotechnika g) Šíření rádiových vln (SVG, kreslicí pomůcky z obrazky_elek).

FIGS_G[('g', pořadí)] -> funkce vracející (F, popisek); pořadí = 0-based pozice otázky v oddílu g).
Hodnoty jsou typické a orientační (výšky vrstev, počty slunečních skvrn, MUF), nejde o měřená data.
"""
import math
from obrazky_elek import F, BL, BLF, RED, GR, TX, GRN, ORA, freqaxis

SKY, GROUND, SUN = '#eaf2fb', '#b08d5b', '#f5c518'


def mast(f, x, y, h=34, lab=None, c=TX, anchor='middle'):
    f.l(x, y, x, y - h, c, 3); f.l(x - 8, y - h, x + 8, y - h, c, 2)
    if lab: f.t(x, y - h - 8, lab, size=13, w='bold', c=c, anchor=anchor)


def ground(f, y, x0=0, x1=760):
    f.rect(x0, y, x1 - x0, 14, fill=GROUND, stroke='none', op=0.55)
    f.l(x0, y, x1, y, '#7a5a2e', 2)


def sun(f, x, y, r=34):
    for k in range(12):
        a = k * math.pi / 6
        f.l(x + (r + 5) * math.cos(a), y + (r + 5) * math.sin(a), x + (r + 16) * math.cos(a), y + (r + 16) * math.sin(a), ORA, 2.5)
    f.circle(x, y, r, fill=SUN, stroke=ORA, sw=2)


def quad(p0, p1, p2, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def layer(f, x0, x1, y0, y1, lab, c=BL, op=0.25, size=14, tx=None):
    f.rect(x0, y0, x1 - x0, y1 - y0, fill=c, stroke='none', op=op)
    if lab: f.t(tx if tx is not None else x0 + 10, (y0 + y1) / 2 + 5, lab, size=size, w='bold', c=c, anchor='start')


# ---------------------------------------------------------------- g) 1 vrstvy D, E, F1, F2
def g_layers():
    f = F(330)
    y = lambda km: 300 - km * 0.6
    for km in range(0, 451, 100):
        f.l(80, y(km), 560, y(km), '#eeeeee', 1)
        f.t(72, y(km) + 5, f'{km} km', anchor='end', size=12)
    ground(f, 300, 80, 560)
    for nm, a, b, c, op in (('D', 60, 90, RED, 0.35), ('E', 95, 130, BL, 0.3), ('F1', 160, 220, BL, 0.4), ('F2', 250, 400, BL, 0.55)):
        layer(f, 90, 550, y(b), y(a), None, c=c, op=op)
        f.t(110, (y(a) + y(b)) / 2 + 7, nm, size=20, w='bold', c=c, anchor='start')
        f.t(160, (y(a) + y(b)) / 2 + 5, f'{a}–{b} km', size=13, anchor='start')
    f.t(350, y(75) + 5, 'pohlcuje nízké kmitočty, v noci zaniká', size=12, c=RED, anchor='start')
    f.t(350, y(112) + 5, 'průměrně ≈ 100 km', size=12, anchor='start')
    f.t(350, y(190) + 5, 'jen ve dne', size=12, anchor='start')
    f.t(350, y(330) + 5, 'nejvyšší, dálková spojení', size=12, anchor='start', c='#ffffff', w='bold')
    f.arrow([(620, 295), (620, 50)], c=GRN, w=3)
    f.t(640, 70, 'směrem\nod Země:', size=13, anchor='start', w='bold')
    for k, (nm, km) in enumerate((('1. D', 75), ('2. E', 112), ('3. F1', 190), ('4. F2', 325))):
        f.t(640, y(km) + 5, nm, size=15, anchor='start', w='bold', c=RED if nm.endswith('D') else BL)
    f.t(320, 322, 'povrch Země', size=12, c='#7a5a2e')
    return f, ('Ionosféra má několik vrstev, od Země nahoru: D, E, F1 a F2 (abecedně podle výšky). Vrstva D existuje jen '
               've dne a nízké kmitočty pohlcuje; v noci F1 a F2 splývají v jednu vrstvu F.')


# ---------------------------------------------------------------- g) 2 jedenáctiletý cyklus
def g_cycle():
    f = F(300)
    x0, y0, w, h = 70, 255, 650, 190
    f.axes(x0, y0, w, h, 'rok', '')
    f.t(x0 - 10, y0 - h - 6, 'počet slunečních skvrn', size=13, anchor='start')
    X = lambda yr: x0 + (yr - 1985) / 47 * (w - 20)
    Y = lambda n: y0 - n / 250 * (h - 10)
    ext = [(1986.7, 13), (1989.9, 214), (1996.4, 11), (2001.9, 180), (2008.9, 2), (2014.3, 116), (2019.9, 2), (2024.8, 160), (2030.5, 10)]
    pts = []
    for (a, na), (b, nb) in zip(ext, ext[1:]):
        for i in range(30):
            t = i / 30
            pts.append((X(a + (b - a) * t), Y(na + (nb - na) * (1 - math.cos(math.pi * t)) / 2)))
    pts.append((X(ext[-1][0]), Y(ext[-1][1])))
    f.path([(X(1986.7), y0)] + pts + [(X(2030.5), y0)], c=ORA, fill=SUN, op=0.35, w=2.4)
    for yr in (1990, 2000, 2010, 2020, 2030):
        f.l(X(yr), y0 - 4, X(yr), y0 + 4, w=1.3); f.t(X(yr), y0 + 20, str(yr), size=12)
    for n in (100, 200):
        f.t(x0 - 6, Y(n) + 4, str(n), size=12, anchor='end')
    for yr, n, cyc in ((1989.9, 214, '22'), (2001.9, 180, '23'), (2014.3, 116, '24'), (2024.8, 160, '25')):
        f.t(X(yr), Y(n) - 8, f'cyklus {cyc}', size=12, w='bold')
    for a, b in ((1986.7, 1996.4), (1996.4, 2008.9), (2008.9, 2019.9)):
        f.arrow([(X(a), y0 - 12), (X(b), y0 - 12)], c=RED, w=1.5, both=True)
        f.t((X(a) + X(b)) / 2, y0 - 18, '≈ 11 let', size=12, c=RED, w='bold')
    f.t(x0 + w - 20, 30, 'orientační vyhlazené hodnoty', size=12, c=GR, anchor='end')
    return f, ('Počet slunečních skvrn (a s ním ultrafialové záření, které ionizuje ionosféru) kolísá s periodou asi '
               '11 let. V maximu cyklu jsou otevřena i vyšší KV pásma a 6 m (50–52 MHz), v minimu jsou použitelná hlavně '
               'nižší pásma.')


# ---------------------------------------------------------------- g) 3 noc – nízká pásma
def g_night():
    f = F(300)
    for k, (x0, title, day) in enumerate(((10, 'DEN', True), (395, 'NOC', False))):
        xs, gy = x0 + 355, 250
        f.rect(x0, 20, 355, 230, fill='#fff8e1' if day else '#e8ecf6', stroke='none')
        f.t(x0 + 20, 45, title, size=17, w='bold', c='#7f4f00' if day else '#1f3864', anchor='start')
        if day: sun(f, x0 + 310, 55, 18)
        else: f.circle(x0 + 310, 55, 16, fill='#fffbe0', stroke=GR, sw=1.2)
        layer(f, x0, xs, 70, 100, 'F', c=BL, op=0.35)
        if day:
            layer(f, x0, xs, 160, 185, 'D', c=RED, op=0.35)
        ground(f, gy, x0, xs)
        mast(f, x0 + 40, gy, lab='TX')
        if day:
            f.arrow([(x0 + 40, gy - 34), (x0 + 130, 172)], c=BL, w=2.5)
            f.t(x0 + 140, 160, '✗', size=26, c=RED, w='bold')
            f.t(x0 + 175, 215, 'vrstva D vlnu\npohltí', size=13, c=RED, anchor='start')
        else:
            f.path(quad((x0 + 40, gy - 34), (x0 + 180, 20), (x0 + 320, gy)), c=GRN, w=2.8)
            f.arrow([(x0 + 315, gy - 12), (x0 + 320, gy)], c=GRN, w=2.8)
            mast(f, x0 + 320, gy, lab='RX')
            f.t(x0 + 180, 150, 'odraz od vrstvy F\n→ dálkové spojení', size=13, c=GRN)
    f.t(380, 286, 'pásma 160, 80 a 40 m (1,8–2,0 · 3,5–3,8 · 7,0–7,2 MHz)', size=14, w='bold')
    return f, ('Ve dne vrstva D silně tlumí nízké kmitočty, takže pásma 160, 80 a 40 m slouží jen pro bližší spojení. '
               'V noci vrstva D zanikne a vlny se odrážejí od vrstvy F – nízká pásma se otevřou pro dálková spojení.')


# ---------------------------------------------------------------- g) 4 70 cm přímá viditelnost
def g_los():
    f = F(330)
    cx, cy, R = 380, 1880, 1700
    gy = lambda x: cy - math.sqrt(R * R - (x - cx) ** 2)
    f.a(f'<path d="M 0,{gy(0):.1f} A {R} {R} 0 0 1 760,{gy(760):.1f} L 760,280 L 0,280 Z" fill="{GROUND}" fill-opacity="0.45" stroke="#7a5a2e" stroke-width="2"/>')
    layer(f, 0, 760, 25, 55, 'ionosféra', c=BL, op=0.2)
    a, b = 120, 640
    mast(f, a, gy(a), 45, 'stanice A'); mast(f, b, gy(b), 45, 'stanice B')
    f.arrow([(a, gy(a) - 45), (b, gy(b) - 45)], c=GRN, w=2.8, both=True)
    f.t(380, gy(a) - 55, 'přímá viditelnost – „vidí“ se anténami', size=14, c=GRN, w='bold')
    f.arrow([(a, gy(a) - 45), (330, 5)], c=BL, w=2, dash='6,4')
    f.t(345, 75, 'ionosféra 70 cm neodráží –\nvlna odejde do vesmíru', size=12, c=BL, anchor='start')
    f.t(380, 300, 'dosah ≈ radiohorizont:  d [km] ≈ 4,1 · (√h₁ + √h₂),  h v metrech', size=14, w='bold')
    f.t(380, 322, 'pásmo 70 cm = 430–440 MHz', size=12, c=GR)
    return f, ('Na UKV (pásmo 70 cm, 430–440 MHz) se vlny šíří přímočaře jako světlo a ionosférou procházejí. Běžná '
               'spojení jsou proto možná jen mezi stanicemi, které na sebe „vidí“; dosah zvětší vyšší umístění antén nebo '
               'převáděč na kopci.')


# ---------------------------------------------------------------- g) 5 mnoho skvrn → MUF > 40 MHz
def g_muf_max():
    f = F(290)
    x0, y0, w, h = 80, 240, 620, 200
    f.axes(x0, y0, w, h, 'hodina (místní čas)', 'MUF [MHz]')
    X = lambda hr: x0 + hr / 24 * (w - 20)
    Y = lambda m: y0 - m / 60 * (h - 15)
    bump = lambda hr: max(0.0, math.sin(math.pi * (hr - 5) / 16)) ** 1.2 if 5 <= hr <= 21 else 0.0
    for lo, hi, c, lab in ((6, 10, BL, 'minimum cyklu (málo skvrn)'), (12, 36, RED, 'maximum cyklu (mnoho skvrn)')):
        pts = [(X(i / 10), Y(lo + hi * bump(i / 10))) for i in range(241)]
        f.path(pts, c=c, w=2.6)
        f.t(X(12.5), Y(lo + hi) - 9, lab, size=13, c=c, w='bold')
    for m, lab in ((40, '40 MHz'), (50, '6 m (50 MHz)')):
        f.l(x0, Y(m), x0 + w - 20, Y(m), GRN if m == 50 else GR, 1.4, '6,4')
        f.t(x0 + w - 20, Y(m) - 5, lab, size=12, c=GRN if m == 50 else GR, anchor='end')
    for m in (10, 20, 30, 40, 50):
        f.t(x0 - 6, Y(m) + 4, str(m), size=12, anchor='end')
    for hr in (0, 6, 12, 18):
        f.t(X(hr), y0 + 20, str(hr), size=12)
    return f, ('Maximální použitelný kmitočet (MUF) závisí na ionizaci ionosféry, tedy na sluneční činnosti. Při velkém '
               'počtu slunečních skvrn vystoupí MUF přes 40 MHz – otevírá se pásmo 10 m (28–29,7 MHz) i 6 m (50–52 MHz).')


# ---------------------------------------------------------------- g) 6 sluneční aktivita
def g_sun():
    f = F(300)
    gy = 260
    sun(f, 60, 60, 32)
    layer(f, 130, 760, 50, 85, 'ionosféra (ionizuje ji UV a RTG záření Slunce)', c=BL, op=0.25, size=13, tx=300)
    for k in range(4):
        x = 125 + k * 6
        pts = [(x + i * 4.5, 70 + 10 * k - 6 * math.sin(i / 1.7) - 2 * i / 3) for i in range(22)]
        f.path(pts, c=ORA, w=1.8)
    ground(f, gy, 0, 760)
    mast(f, 90, gy, 40, 'TX')
    f.arrow([(110, gy - 6), (330, gy - 6)], c=GRN, w=3); f.t(220, gy - 16, 'přízemní vlna', size=13, c=GRN, w='bold')
    mast(f, 360, gy, 40, 'RX 1')
    f.arrow([(90, gy - 40), (352, gy - 42)], c=GRN, w=2.2, dash='7,4'); f.t(220, gy - 52, 'přímý paprsek', size=13, c=GRN, w='bold')
    f.path(quad((90, gy - 40), (440, -40), (700, gy)), c=RED, w=2.8)
    f.arrow([(695, gy - 14), (700, gy)], c=RED, w=2.8)
    mast(f, 700, gy, 40, 'RX 2')
    f.t(500, 175, 'prostorová vlna přes ionosféru\n→ závisí na sluneční aktivitě', size=13, c=RED, w='bold')
    f.t(220, 290, 'nezávisí na Slunci', size=13, c=GRN)
    return f, ('Přízemní vlna a přímý paprsek ionosféru nevyužívají, takže sluneční činnost je téměř neovlivňuje. Všechna '
               'ostatní spojení přes ionosféru závisí na tom, jak silně ji Slunce ionizuje (denní doba, roční období, '
               '11letý cyklus, sluneční erupce).')


# ---------------------------------------------------------------- g) 7 kmitočet pod MUF
def g_below_muf():
    f = F(290)
    gy = 250
    layer(f, 0, 760, 55, 105, 'ionosféra', c=BL, op=0.25)
    ground(f, gy)
    mast(f, 100, gy, 36, 'TX')
    f.path(quad((100, gy - 36), (330, -10), (560, gy)), c=GRN, w=3); f.arrow([(555, gy - 14), (560, gy)], c=GRN, w=3)
    mast(f, 560, gy, 36, 'RX')
    f.t(578, 150, 'f < MUF: lom zpět\n→ část energie se\nvrátí k Zemi', size=13, c=GRN, w='bold', anchor='start')
    f.path([(100, gy - 36), (250, 70), (300, 5)], c=RED, w=2.6); f.arrow([(296, 12), (300, 5)], c=RED, w=2.6)
    f.t(310, 22, 'f > MUF: projde ionosférou do vesmíru', size=13, c=RED, w='bold', anchor='start')
    f.path([(330, 52), (360, 30)], c=GRN, w=1.4, dash='3,3')
    f.t(370, 40, 'malá část projde / pohltí se', size=11, c=GR, anchor='start')
    return f, ('Vlna s kmitočtem nižším než MUF se v ionosféře postupně lomí, až se stočí zpět k Zemi – vrátí se (část '
               'energie se ztratí pohlcením). Vlna nad MUF už se nestočí dost a odejde do vesmíru.')


# ---------------------------------------------------------------- g) 8 geomagnetická bouře
def g_storm():
    f = F(290)
    sun(f, 50, 125, 32)
    ex, ey = 330, 125
    for k in range(3):
        f.ellipse(ex + 15, ey, 50 + k * 22, 30 + k * 16, stroke='#8e44ad', sw=1.2, dash='4,3')
    f.circle(ex, ey, 34, fill='#5dade2', stroke=BL, sw=2); f.t(ex, ey + 5, 'Země', size=12, c='#ffffff', w='bold')
    import random
    rnd = random.Random(5)
    for i in range(45):
        x = 100 + rnd.random() * 150
        y = ey + (rnd.random() - 0.5) * (30 + (x - 100) * 0.5)
        f.circle(x, y, 2.2, fill=ORA, stroke=ORA, sw=0.5)
    f.arrow([(110, 60), (240, 85)], c=ORA, w=2); f.t(150, 50, 'proud částic (CME)', size=12, c=ORA, w='bold')
    f.t(ex, 230, 'magnetické pole Země\nse rozkmitá', size=12, c='#8e44ad')
    x0, y0, w, h = 450, 220, 290, 170
    f.axes(x0, y0, w, h, 'dny', '')
    X = lambda d: x0 + d / 3 * (w - 20)
    kp = [2, 2, 3, 5, 7, 8, 7, 6, 5, 4, 3, 2]
    for i, k in enumerate(kp):
        c = GRN if k < 5 else (ORA if k < 7 else RED)
        f.rect(X(i / 4) + 2, y0 - k * 7, (w - 20) / 12 - 4, k * 7, fill=c, stroke='none', op=0.75)
    sig = [(X(i / 40), y0 - 150 + (55 * math.exp(-((i / 40 - 1.4) / 0.45) ** 2))) for i in range(121)]
    f.path(sig, c=BL, w=2.4)
    f.t(x0 + 6, y0 - h + 5, 'síla KV signálů', size=12, c=BL, anchor='start', w='bold')
    f.t(x0, y0 + 40, 'sloupce: index Kp (geomagnetická aktivita)', size=12, c=RED, anchor='start')
    f.t(X(1.4) + 30, y0 - 72, 'bouře', size=12, c=RED, w='bold', anchor='start')
    return f, ('Při geomagnetické bouři (po sluneční erupci dorazí k Zemi oblak nabitých částic) se rozruší ionosféra. '
               'KV signály slábnou nebo úplně zmizí (hlavně na trasách přes polární oblasti), MUF klesá. Na VKV se naopak '
               'může objevit šíření polární září (aurora).')


# ---------------------------------------------------------------- g) 9 co ovlivňuje intenzitu signálu
def g_factors():
    f = F(270)
    items = [('vysílač', 'výkon'), ('napáječ', 'útlum'), ('anténa TX', 'zisk, výška'), ('šíření', 'vzdálenost,\npodmínky'),
             ('anténa RX', 'zisk, výška'), ('přijímač', '')]
    for i, (nm, fc) in enumerate(items):
        x = 15 + i * 125
        f.box(x, 50, 108, 46, nm, size=13, wt='bold')
        if fc: f.t(x + 54, 118, fc, size=12, c=GRN)
        if i: f.arrow([(x - 17, 73), (x, 73)], c=TX, w=1.8)
    f.t(380, 30, 'na intenzitu přijímaného signálu mají vliv (zeleně):', size=14, w='bold', c=GRN)
    f.box(30, 175, 200, 50, 'napájecí napětí zdroje', size=13, fill='#f2f2f2', stroke=GR)
    f.l(30, 175, 230, 225, RED, 3); f.l(30, 225, 230, 175, RED, 3)
    f.arrow([(130, 175), (69, 98)], c=GR, w=1.5, dash='4,3')
    f.t(250, 195, 'jen napájí vysílač – je-li v pořádku (např. 13,8 V),', size=13, anchor='start')
    f.t(250, 217, 'výkon vysílače ani signál u protistanice nemění', size=13, anchor='start')
    return f, ('Sílu signálu u protistanice určuje vyzářený výkon (výkon vysílače, ztráty v napáječi, zisk antény) a '
               'útlum na trase (vzdálenost, podmínky šíření) a také přijímací anténa. Napájecí napětí zdroje mezi tyto '
               'činitele nepatří – pokud je v toleranci, vysílač dává stále stejný výkon.')


# ---------------------------------------------------------------- g) 10 MUF 17 MHz → 20 m
def _muf17_rays(f):
    """odrazy Praha–Tokio v souřadnicích 760×400 (volající je zmenší)"""
    cx, cy, R, ex = 380, 1290, 1000, 2.3
    k = 0.157 * ex
    P = lambda a, h: (cx + (R + h * k) * math.sin(a), cy - (R + h * k) * math.cos(a))
    A0 = 0.37
    f.a(f'<path d="M {P(-A0, 0)[0]:.1f},{P(-A0, 0)[1]:.1f} A {R} {R} 0 0 1 {P(A0, 0)[0]:.1f},{P(A0, 0)[1]:.1f} L 760,400 L 0,400 Z" '
        f'fill="{GROUND}" fill-opacity="0.45" stroke="#7a5a2e" stroke-width="2"/>')
    for h0, h1, lab, c, op in ((60, 90, 'D', RED, 0.30), (100, 125, 'E', BL, 0.25), (250, 340, 'F2', BL, 0.40)):
        r, w_ = R + (h0 + h1) / 2 * k, (h1 - h0) * k
        a0, a1 = P(-A0, (h0 + h1) / 2), P(A0, (h0 + h1) / 2)
        f.a(f'<path d="M {a0[0]:.1f},{a0[1]:.1f} A {r:.1f} {r:.1f} 0 0 1 {a1[0]:.1f},{a1[1]:.1f}" stroke="{c}" '
            f'stroke-width="{w_:.1f}" stroke-opacity="{op}" fill="none"/>')
        p = P(-0.335, (h0 + h1) / 2)
        f.t(p[0] + 4, p[1] + 5, lab, size=14, c=c, w='bold', anchor='start')
    a_tx, a_rx = -0.31, 0.31
    # 20 m – dva skoky od F2
    pts = [P(a_tx, 0), P(a_tx / 2, 295), P(0, 0), P(a_rx / 2, 295), P(a_rx, 0)]
    f.path(pts, c=GRN, w=3.4)
    for p in pts[1::2]: f.circle(*p, 5, fill=GRN, stroke=GRN)
    # 40 m – 4 kratší skoky, pokaždé útlum ve vrstvě D
    hops = [a_tx + i * (a_rx - a_tx) / 4 for i in range(5)]
    for i in range(4):
        a, b = hops[i], hops[i + 1]
        w_ = 2.6 - i * 0.55
        f.path([P(a, 0), P((a + b) / 2, 112), P(b, 0)], c=ORA, w=w_, dash='7,4')
        f.circle(*P((a + b) / 2, 112), 3.5, fill=ORA, stroke=ORA)
        for t in (0.25, 0.75):
            q = P(a + (b - a) * (0.32 if t < 0.5 else 0.68), 75)
            f.t(q[0], q[1] + 5, '×', size=13, c=RED, w='bold')
    # 15 m a výš – projde
    s0, s1 = P(a_tx, 0), P(-0.17, 295)
    dx, dy = s1[0] - s0[0], s1[1] - s0[1]
    f.path([s0, s1, (s1[0] + dx * 0.55, s1[1] + dy * 0.75)], c=RED, w=2.6)
    f.arrow([(s1[0] + dx * 0.5, s1[1] + dy * 0.68), (s1[0] + dx * 0.55, s1[1] + dy * 0.75)], c=RED, w=2.6)
    p = P(a_tx, 0); f.t(p[0], p[1] + 24, 'Praha', size=14, w='bold')
    p = P(a_rx, 0); f.t(p[0], p[1] + 24, 'Tokio', size=14, w='bold')
    p = P(0, 0); f.t(p[0], p[1] + 58, '≈ 9 000 km – skoky jsou zkreslené (schematicky), výšky vrstev zvětšeny', size=12, c='#5a4020')
    for p_, lab, c in ((P(a_tx / 2, 295), '20 m', GRN), (P(-0.12, 112), '40 m', ORA)):
        f.t(p_[0] + 10, p_[1] - 8, lab, size=16, c=c, w='bold', anchor='start')
    f.t(s1[0] + dx * 0.55 + 10, s1[1] + dy * 0.75 + 16, '17 m a výš – projde', size=16, c=RED, w='bold', anchor='start')

def g_muf17():
    f = F(537)
    X = freqaxis(f, 40, 700, 180, 5, 30, [(5, '5'), (10, '10'), (15, '15'), (17, '17'), (20, '20'), (25, '25')])
    f.rect(X(5), 50, X(17) - X(5), 130, fill=GRN, stroke='none', op=0.07)
    f.rect(X(17), 50, X(30) - X(17), 130, fill=RED, stroke='none', op=0.08)
    f.l(X(17), 40, X(17), 180, RED, 2.4); f.t(X(17) + 6, 58, 'MUF 17 MHz', size=14, c=RED, w='bold', anchor='start')
    f.t(X(9.5), 72, 'pod MUF – vlna se vrátí k Zemi', size=12, c=GRN, w='bold')
    f.t(X(24.5), 82, 'nad MUF – projde do vesmíru', size=12, c=RED, w='bold')
    f.t(X(14.5) - 6, 40, 'optimum ≈ 0,85 · MUF ≈ 14,5 MHz', size=12, c=GRN, anchor='end')
    f.arrow([(X(14.5), 44), (X(14.5), 96)], c=GRN, w=1.6)
    for nm, a, b, mhz in (('40 m', 7.0, 7.2, '7,0–7,2'), ('30 m', 10.1, 10.15, '10,1'), ('20 m', 14.0, 14.35, '14,0–14,35'),
                          ('17 m', 18.068, 18.168, '18,07–18,17'), ('15 m', 21.0, 21.45, '21,0–21,45'),
                          ('12 m', 24.89, 24.99, '24,89–24,99'), ('10 m', 28.0, 29.7, '28,0–29,7')):
        best = nm == '20 m'
        c = GRN if best else (RED if a > 17 else BL)
        f.rect(X(a) - 3, 135, max(6, X(b) - X(a) + 6), 45, fill=c, stroke=c, op=0.8 if best else 0.45)
        xo = 12 if nm == '17 m' else 0
        f.t((X(a) + X(b)) / 2 + xo, 112, nm, size=13 if best else 12, c=c, w='bold')
        f.t((X(a) + X(b)) / 2 + xo, 127, mhz, size=10.5, c=c)
    f.t(X(14.2), 225, '20 m (14,0–14,35 MHz) leží těsně pod MUF → nejlepší podmínky', size=14, c=GRN, w='bold')
    f.t(380, 262, 'Jak to vypadá na trase Praha–Tokio (schematicky):', size=13, w='bold')
    f.a('<g transform="translate(76,215) scale(0.8)">')
    _muf17_rays(f)
    f.a('</g>')
    return f, ('Horní graf: pásma pod MUF 17 MHz (zeleně podbarvená oblast) se od ionosféry vracejí, pásma nad MUF '
               '(červeně) projdou do vesmíru. Nejlepší je pásmo těsně pod MUF – 20 m (14,0–14,35 MHz), kde je útlum malý. '
               'Dolní obrázek: 20 m se odráží od vrstvy F2 a dvěma dlouhými skoky dojde do Tokia. '
               'Pásmo 40 m (7,0–7,2 MHz) se ve dne odráží už od nižší vrstvy E, potřebuje proto více '
               'kratších skoků a při každém průchodu vrstvou D ztrácí energii. Pásmo 17 m (18,068–18,168 MHz) a vyšší jsou '
               'nad MUF – vlna ionosférou projde a nevrátí se.')


# ---------------------------------------------------------------- g) 11 rozptyl – zkreslení vícecestným šířením
def g_scatter_dist():
    f = F(360)
    gy = 200
    ground(f, gy)
    import random
    rnd = random.Random(2)
    for i in range(16):
        f.ellipse(250 + rnd.random() * 260, 45 + rnd.random() * 40, 22 + rnd.random() * 20, 9 + rnd.random() * 6, fill=BL, stroke='none', op=0.18)
    f.t(380, 30, 'nehomogenity ionosféry (rozptylová oblast)', size=12, c=BL)
    mast(f, 70, gy, 34, 'TX'); mast(f, 690, gy, 34, 'RX')
    cols = [GRN, BL, ORA, RED]
    for k, (px, py) in enumerate(((290, 85), (360, 60), (430, 75), (500, 50))):
        f.path([(70, gy - 34), (px, py), (690, gy - 34)], c=cols[k], w=2)
        f.circle(px, py, 4, fill=cols[k], stroke=cols[k])
    f.t(380, 236, 'každá cesta je jinak dlouhá → signály dorazí v různých časech', size=13, w='bold')
    x0, w = 70, 520
    base = lambda t: math.sin(2 * math.pi * 3 * t) * (1 if 0.1 < t < 0.75 else 0.15)
    for k, d in enumerate((0, 0.05, 0.1)):
        y = 262 + k * 22
        f.path([(x0 + w * i / 300, y - 8 * base(i / 300 - d)) for i in range(301)], c=cols[k], w=1.4)
    yS = 336
    f.path([(x0 + w * i / 300, yS - 6 * sum(base(i / 300 - d) for d in (0, 0.05, 0.1))) for i in range(301)], c=TX, w=2)
    f.t(x0 + w + 20, 250, 'opožděné kopie', size=12, anchor='start')
    f.t(x0 + w + 20, yS + 4, 'součet = zkreslený\n(„dutý“, ozvěna)', size=12, anchor='start', c=RED, w='bold')
    return f, ('Rozptýlený (scatter) signál přichází do místa příjmu současně po mnoha drahách různé délky. Kopie signálu '
               'jsou vzájemně časově posunuté, sčítají se a ruší – výsledný signál zní zkresleně, dutě, s ozvěnou a '
               'rychlým úniky.')


# ---------------------------------------------------------------- g) 12 rozptyl vyplní pásmo ticha
def g_skipzone():
    f = F(300)
    gy = 230
    layer(f, 0, 760, 40, 75, 'ionosféra', c=BL, op=0.22)
    ground(f, gy)
    mast(f, 50, gy, 34, 'TX')
    f.path([(50, gy - 2)] + [(50 + i * 1.6, gy - 2 - 40 * math.exp(-i / 50)) for i in range(100)] + [(210, gy - 2)], c=GRN, fill=GRN, op=0.2, w=1.5)
    f.t(130, gy - 50, 'přízemní\nvlna', size=12, c=GRN, w='bold')
    f.path(quad((50, gy - 34), (400, -60), (735, gy)), c=BL, w=2.6); f.arrow([(731, gy - 12), (735, gy)], c=BL, w=2.6)
    f.t(650, 120, 'odraz\n(prostorová vlna)', size=12, c=BL, w='bold')
    for x in (280, 360, 440, 520):
        f.arrow([(x + 30, 75), (x, gy - 4)], c=ORA, w=1.6, dash='5,4')
    f.t(262, 125, 'rozptyl', size=14, c=ORA, w='bold', anchor='end')
    f.arrow([(210, gy + 28), (735, gy + 28)], c=RED, w=1.6, both=True)
    f.t(470, gy + 48, 'pásmo ticha – sem přízemní vlna ani odraz nedosáhnou, slyšet je jen rozptyl', size=13, c=RED, w='bold')
    return f, ('Mezi místem, kam ještě dosáhne přízemní vlna, a místem dopadu první odražené vlny je pásmo ticha. '
               'Signály se do něj dostanou jen rozptylem (scatter) na nehomogenitách ionosféry nebo od zemského povrchu.')


# ---------------------------------------------------------------- g) 13 výška vrstvy E
def g_e100():
    f = F(310)
    y = lambda km: 280 - km * 0.6
    f.arrow([(110, 280), (110, 20)], c=TX, w=1.6)
    for km in (0, 100, 200, 300, 400):
        f.l(104, y(km), 116, y(km), w=1.4); f.t(98, y(km) + 5, f'{km} km', size=12, anchor='end')
    ground(f, 280, 110, 740)
    for nm, a, b, c, op in (('D', 60, 90, RED, 0.25), ('E', 90, 130, BL, 0.55), ('F', 200, 400, BL, 0.22)):
        layer(f, 120, 740, y(b), y(a), None, c=c, op=op)
    f.l(120, y(100), 740, y(100), RED, 2.2, '8,5')
    f.t(140, y(100) - 8, 'vrstva E ≈ 100 km', size=17, c=RED, w='bold', anchor='start')
    f.t(140, y(75) + 5, 'D', size=14, c=RED, w='bold', anchor='start'); f.t(140, y(300) + 5, 'F (F1, F2)', size=14, c=BL, w='bold', anchor='start')
    f.t(470, y(10) - 4, '✈ dopravní letadlo ≈ 10 km', size=12, anchor='start')
    f.t(470, y(400) + 16, 'ISS (vesmírná stanice) ≈ 400 km', size=12, anchor='start')
    f.circle(455, y(400) + 12, 5, fill=GR, stroke=GR)
    f.t(330, y(100) + 22, 'odráží hlavně nižší KV pásma; v létě sporadická vrstva Es', size=12, anchor='start', c=BL)
    return f, ('Vrstva E leží v průměrné výšce kolem 100 km (asi 90–130 km). Pro srovnání: dopravní letadla létají '
               've výšce asi 10 km, Mezinárodní vesmírná stanice obíhá ve výšce asi 400 km.')


# ---------------------------------------------------------------- g) 14 F2 – nejvyšší vrstva, nejdelší skok
def g_f2hop():
    f = F(350)
    cx, cy, R, ex = 380, 1255, 1000, 3.0
    P = lambda ang, hkm: (cx + (R + hkm * 0.157 * ex) * math.sin(ang), cy - (R + hkm * 0.157 * ex) * math.cos(ang))
    f.a(f'<path d="M {P(-0.4, 0)[0]:.1f},{P(-0.4, 0)[1]:.1f} A {R} {R} 0 0 1 {P(0.4, 0)[0]:.1f},{P(0.4, 0)[1]:.1f} L 760,350 L 0,350 Z" '
        f'fill="{GROUND}" fill-opacity="0.45" stroke="#7a5a2e" stroke-width="2"/>')
    for hk, lab, c, op in ((110, 'E ≈ 110 km', BL, 0.35), (300, 'F2 ≈ 300 km', BL, 0.6)):
        r = R + hk * 0.157 * ex
        a0, a1 = P(-0.4, hk), P(0.4, hk)
        f.a(f'<path d="M {a0[0]:.1f},{a0[1]:.1f} A {r:.1f} {r:.1f} 0 0 1 {a1[0]:.1f},{a1[1]:.1f}" stroke="{c}" stroke-width="10" '
            f'stroke-opacity="{op * 0.6}" fill="none"/>')
        f.t(P(-0.3, hk)[0], P(-0.3, hk)[1] - 12, lab, size=13, c=c, w='bold', anchor='start')
    th = 0.314
    for hk, ap, end, c in ((110, -th / 2, 0, GRN), (300, 0, th, RED)):
        a, top, b = P(-th, 0), P(ap, hk), P(end, 0)
        f.path([a, top, b], c=c, w=2.6); f.circle(*top, 4, fill=c, stroke=c)
        f.circle(*b, 5, fill=c, stroke=c)
    tx = P(-th, 0)
    f.t(P(0, 0)[0], P(0, 0)[1] + 24, '', size=1)
    f.t(P(0, 0)[0], P(0, 0)[1] + 26, 'skok E ≤ 2 000 km', size=13, c=GRN, w='bold')
    f.t(P(th, 0)[0] - 10, P(th, 0)[1] + 26, 'skok F2 ≤ 4 000 km', size=13, c=RED, w='bold')
    f.t(P(-th, 0)[0], P(-th, 0)[1] + 26, 'TX', size=13, w='bold')
    f.t(380, 22, 'čím výš se vlna odrazí, tím dál dopadne (výšky vrstev zvětšeny)', size=14, w='bold')
    return f, ('Vrstva F2 je nejvyšší, a proto má odražená vlna nejdelší skok – jedním odrazem až asi 4 000 km (od vrstvy '
               'E jen asi 2 000 km). F2 je navíc nejsilněji ionizovaná, takže odráží i nejvyšší KV kmitočty.')


# ---------------------------------------------------------------- g) 15 pokles pole 1/d
def g_inv_d():
    f = F(290)
    x0, y0, w, h = 80, 235, 620, 200
    f.axes(x0, y0, w, h, '', 'intenzita pole E'); f.t(x0 + w, y0 + 40, 'vzdálenost', size=13, anchor='end')
    X = lambda d: x0 + d / 8.5 * (w - 20)
    Y = lambda e: y0 - e / 1.15 * (h - 20)
    f.path([(X(0.7 + i * 0.039), Y(min(1.15, 1 / (0.7 + i * 0.039)))) for i in range(201)], c=BL, w=2.6)
    f.path([(X(0.95 + i * 0.0378), Y(min(1.15, 1 / (0.95 + i * 0.0378) ** 2))) for i in range(201)], c=GR, w=1.8, dash='6,4')
    for d, lab in ((1, 'E'), (2, 'E/2'), (4, 'E/4'), (8, 'E/8')):
        f.l(X(d), y0, X(d), Y(1 / d), BL, 1, '3,3'); f.circle(X(d), Y(1 / d), 5, fill=BL, stroke=BL)
        f.t(X(d) + 8, Y(1 / d) - 8, lab, size=13, c=BL, w='bold', anchor='start')
        f.t(X(d), y0 + 20, f'{d} d' if d > 1 else 'd', size=12)
    f.t(X(5.3), Y(0.75), 'E ~ 1/d: 2× dál → poloviční pole (−6 dB)', size=14, c=BL, w='bold')
    f.t(X(5.3), Y(0.6), 'hustota výkonu ~ 1/d² (čárkovaně)', size=13, c=GR)
    return f, ('Ve vzdálené zóně (dál než asi 10 λ od antény) klesá intenzita elektrického pole nepřímo úměrně '
               'vzdálenosti – dvojnásobná vzdálenost znamená poloviční pole. Výkon na jednotku plochy klesá se čtvercem '
               'vzdálenosti.')


# ---------------------------------------------------------------- g) 16 EME
def g_eme():
    f = F(300)
    ex, ey, mx, my = 130, 165, 680, 120
    f.a(f'<circle cx="{ex}" cy="{ey}" r="92" fill="none" stroke="{BL}" stroke-opacity="0.25" stroke-width="16"/>')
    f.circle(ex, ey, 72, fill='#5dade2', stroke=BL, sw=2)
    f.t(ex, ey + 5, 'Země', size=14, w='bold', c='#ffffff')
    f.t(ex, ey - 110, 'ionosféra', size=12, c=BL)
    f.circle(mx, my, 40, fill='#dddddd', stroke=GR, sw=2); f.t(mx, my + 5, 'Měsíc', size=13, w='bold')
    a = (ex + 60, ey - 40)
    f.arrow([a, (mx - 40, my - 8)], c=GRN, w=2.6)
    f.arrow([(mx - 40, my + 6), (ex + 66, ey - 22)], c=GRN, w=2.6, dash='7,4')
    f.t(420, 98, 'VKV/UKV projde ionosférou → odraz od Měsíce', size=13, c=GRN, w='bold')
    f.path([(ex + 50, ey + 50), (ex + 90, ey + 75), (ex + 60, ey + 72)], c=RED, w=2.4)
    f.t(ex + 105, ey + 80, 'KV se od ionosféry vrátí – k Měsíci nedoletí', size=13, c=RED, w='bold', anchor='start')
    f.t(420, 160, '≈ 384 000 km, ozvěna za ≈ 2,5 s, útlum trasy ≈ 250 dB', size=13)
    f.t(380, 285, 'pásma 6 m až 3 cm (50 MHz – 10 GHz), nejvíc 2 m, 70 cm a 23 cm', size=14, w='bold')
    return f, ('Pro spojení odrazem od Měsíce musí vlna projít ionosférou – proto se používají VKV a vyšší pásma, od 6 m '
               '(50–52 MHz) po 3 cm (10 GHz). Útlum trasy je obrovský, takže jsou potřeba velké antény, výkon a citlivé '
               'přijímače (často digitální druh provozu JT65/Q65).')


# ---------------------------------------------------------------- g) 17 Doppler – družice
def g_doppler():
    f = F(320)
    cx, cy, R = 200, 595, 420
    f.a(f'<path d="M 0,{cy - math.sqrt(R*R - 200*200):.1f} A {R} {R} 0 0 1 400,{cy - math.sqrt(R*R - 200*200):.1f} L 400,320 L 0,320 Z" '
        f'fill="{GROUND}" fill-opacity="0.45" stroke="#7a5a2e" stroke-width="2"/>')
    mast(f, 200, cy - R, 30, 'stanice')
    ro = R + 125
    pts = [(cx + ro * math.sin(a / 100), cy - ro * math.cos(a / 100)) for a in range(-30, 31)]
    f.path(pts, c=GR, w=1.4, dash='5,4')
    for a, lab, c in ((-0.25, 'blíží se: f ↑', RED), (0.0, 'nad hlavou: f₀', TX), (0.25, 'vzdaluje se: f ↓', BL)):
        x, y = cx + ro * math.sin(a), cy - ro * math.cos(a)
        f.rect(x - 9, y - 6, 18, 12, fill='#888', stroke=TX, sw=1); f.l(x - 22, y, x + 22, y, BL, 3)
        f.t(x, y - 14, lab, size=12, c=c, w='bold')
        f.l(200, cy - R - 30, x, y + 6, c, 1, '3,3')
    f.arrow([(cx + ro * math.sin(-0.33), cy - ro * math.cos(-0.33)), (cx + ro * math.sin(-0.29), cy - ro * math.cos(-0.29))], c=GR, w=2)
    x0, y0, w, h = 450, 180, 280, 220
    f.arrow([(x0, y0), (x0 + w, y0)], c=TX, w=1.5); f.arrow([(x0, y0 + 100), (x0, y0 - 105)], c=TX, w=1.5)
    f.t(x0 + w, y0 + 20, 'čas přeletu', size=12, anchor='end'); f.t(x0 + 6, y0 - 95, 'Δf', size=14, anchor='start', w='bold')
    f.path([(x0 + 10 + i * 2.5, y0 - 80 * math.tanh(-(i - 50) / 12)) for i in range(101)], c=RED, w=2.6)
    f.t(x0 + 50, y0 - 85, '+10 kHz', size=12, c=RED); f.t(x0 + w - 40, y0 + 98, '−10 kHz', size=12, c=BL)
    f.t(x0 + w / 2 + 50, y0 - 40, 'Δf = f · v / c', size=15, w='bold', anchor='start')
    f.t(x0 + w / 2 + 50, y0 - 18, '(435 MHz, 7,5 km/s)', size=11, c=GR, anchor='start')
    return f, ('Družice na nízké dráze letí rychlostí kolem 7,5 km/s. Když se blíží, přijímáme vyšší kmitočet, když se '
               'vzdaluje, nižší – v pásmu 70 cm (430–440 MHz) až asi ±10 kHz. Při provozu přes družice je proto nutné '
               'kmitočet během přeletu dolaďovat.')


FIGS_G = {
    ('g', 0): g_layers, ('g', 1): g_cycle, ('g', 2): g_night, ('g', 3): g_los, ('g', 4): g_muf_max, ('g', 5): g_sun,
    ('g', 6): g_below_muf, ('g', 7): g_storm, ('g', 8): g_factors, ('g', 9): g_muf17, ('g', 10): g_scatter_dist,
    ('g', 11): g_skipzone, ('g', 12): g_e100, ('g', 13): g_f2hop, ('g', 14): g_inv_d, ('g', 15): g_eme, ('g', 16): g_doppler,
}
