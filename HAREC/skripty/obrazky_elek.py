# -*- coding: utf-8 -*-
"""Názorné obrázky k otázkám části Elektrotechnika, oddíly c) až f) (SVG bez externích knihoven).

FIGS[(oddíl, pořadí)] -> funkce vracející (svg_bytes, šířka, výška, popisek)
  pořadí = 0-based pozice otázky v oddílu (v oddílu c) jsou v originále dvě otázky s číslem 1).
figure(oddíl, pořadí) -> (svg, w, h, popisek) | None
Schémata a grafy jsou ilustrativní (typické hodnoty), nejde o měřená data.
"""
import math
from xml.sax.saxutils import escape

W = 760
FONT = 'font-family="Liberation Sans, Arial, sans-serif"'
BL, BLF, RED, GR, TX, GRN, ORA = '#2e5597', '#c9d8f0', '#c0392b', '#888888', '#222222', '#2e7d32', '#d68910'


class F:
    def __init__(self, h, w=W):
        self.w, self.h = w, h
        self.o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT} font-size="15">',
                  f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>']

    def a(self, s): self.o.append(s)

    def t(self, x, y, s, c=TX, anchor='middle', size=15, w='normal', rot=None, italic=False):
        for k, line in enumerate(str(s).split('\n')):
            yy = y + k * size * 1.22
            tr = f' transform="rotate({rot} {x:.1f} {yy:.1f})"' if rot is not None else ''
            st = ' font-style="italic"' if italic else ''
            self.a(f'<text x="{x:.1f}" y="{yy:.1f}" fill="{c}" text-anchor="{anchor}" font-size="{size}" '
                   f'font-weight="{w}"{st}{tr}>{escape(line)}</text>')

    def l(self, x1, y1, x2, y2, c=TX, w=1.8, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>')

    def wire(self, *pts, c=TX, w=1.8):
        self.path(pts, c=c, w=w)

    def path(self, pts, c=BL, w=2.2, fill='none', dash=None, op=1.0, close=False):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        z = ' Z' if close else ''
        self.a('<path d="M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + z +
               f'" stroke="{c}" stroke-width="{w}" fill="{fill}" fill-opacity="{op}" stroke-linejoin="round"{d}/>')

    def arrow(self, pts, c=BL, w=2.2, dash=None, both=False):
        self.path(pts, c=c, w=w, dash=dash)
        self._head(pts[-2], pts[-1], c, w)
        if both:
            self._head(pts[1], pts[0], c, w)

    def _head(self, p1, p2, c, w):
        (x1, y1), (x2, y2) = p1, p2
        a = math.atan2(y2 - y1, x2 - x1); L = 8 + w * 1.6; b = 0.42
        self.a(f'<polygon points="{x2:.1f},{y2:.1f} {x2 - L * math.cos(a - b):.1f},{y2 - L * math.sin(a - b):.1f} '
               f'{x2 - L * math.cos(a + b):.1f},{y2 - L * math.sin(a + b):.1f}" fill="{c}"/>')

    def rect(self, x, y, w, h, fill='none', stroke=TX, sw=1.8, rx=0, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
               f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, x, y, r, fill='none', stroke=TX, sw=1.8, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def ellipse(self, x, y, rx, ry, fill='none', stroke=TX, sw=1.8, op=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.a(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" fill-opacity="{op}" '
               f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def dot(self, x, y, c=TX): self.circle(x, y, 3.6, fill=c, stroke=c, sw=1)

    def term(self, x, y): self.circle(x, y, 5, fill='#ffffff')

    def done(self):
        return '\n'.join(self.o + ['</svg>']).encode('utf-8')

    # ------------------------------------------------ bloky a grafy
    def box(self, x, y, w, h, text, fill='#eef3fb', stroke=BL, size=14, c=TX, wt='normal', sw=1.8):
        """x, y = levý horní roh"""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=6)
        n = len(text.split('\n'))
        self.t(x + w / 2, y + h / 2 + size * 0.36 - (n - 1) * size * 0.61, text, size=size, c=c, w=wt)

    def mixer(self, x, y, r=20, c=TX):
        self.circle(x, y, r, fill='#ffffff', stroke=c)
        k = r * 0.7
        self.l(x - k, y - k, x + k, y + k, c); self.l(x - k, y + k, x + k, y - k, c)

    def axes(self, x0, y0, w, h, xl='', yl='', c=TX):
        """x0, y0 = počátek (vlevo dole)"""
        self.arrow([(x0, y0), (x0 + w, y0)], c=c, w=1.6)
        self.arrow([(x0, y0), (x0, y0 - h)], c=c, w=1.6)
        if xl: self.t(x0 + w, y0 + 22, xl, anchor='end', size=14)
        if yl: self.t(x0 + 8, y0 - h + 6, yl, anchor='start', size=14)

    def plot(self, f, x0, y0, w, h, xa, xb, ya, yb, n=200, c=BL, wd=2.4, dash=None, clip=True):
        pts = []
        for i in range(n + 1):
            xv = xa + (xb - xa) * i / n
            yv = f(xv)
            if clip: yv = max(ya, min(yb, yv))
            pts.append((x0 + (xv - xa) / (xb - xa) * w, y0 - (yv - ya) / (yb - ya) * h))
        self.path(pts, c=c, w=wd, dash=dash)
        return pts

    def sine(self, x0, y0, w, a, periods, c=BL, wd=2, f=None, n=240):
        f = f or (lambda u: math.sin(u))
        self.path([(x0 + w * i / n, y0 - a * f(2 * math.pi * periods * i / n)) for i in range(n + 1)], c=c, w=wd)


# ---------------------------------------------------------------- schematické značky součástek
BODY = {'R': 26, 'C': 7, 'Cv': 7, 'L': 30, 'D': 11, 'Z': 11, 'X': 12}


def part(f, kind, p1, p2, lab=None, side=1, c=TX, off=None, size=14, lc=None):
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    P = lambda a, b: (mx + ux * a + nx * b, my + uy * a + ny * b)
    B = BODY[kind]
    a, b = P(-B, 0), P(B, 0)
    f.l(x1, y1, *a, c=c); f.l(*b, x2, y2, c=c)
    if kind == 'R':
        f.path([P(-B, -9), P(B, -9), P(B, 9), P(-B, 9)], c=c, w=1.9, fill='#ffffff', close=True)
    elif kind in ('C', 'Cv'):
        f.l(*P(-B, -18), *P(-B, 18), c=c, w=3); f.l(*P(B, -18), *P(B, 18), c=c, w=3)
        if kind == 'Cv':
            f.arrow([P(-16, 20), P(16, -22)], c=c, w=1.4)
    elif kind == 'X':
        f.l(*P(-B, -16), *P(-B, 16), c=c, w=2.5); f.l(*P(B, -16), *P(B, 16), c=c, w=2.5)
        f.path([P(-6, -12), P(6, -12), P(6, 12), P(-6, 12)], c=c, w=1.6, fill='#ffffff', close=True)
    elif kind == 'L':
        d = 'M %.1f,%.1f' % a
        for k in range(4):
            e = P(-B + (k + 1) * 2 * B / 4, 0)
            d += ' A %.1f %.1f 0 0 1 %.1f,%.1f' % (B / 4, B / 4, e[0], e[1])
        f.a(f'<path d="{d}" stroke="{c}" stroke-width="2" fill="none"/>')
    elif kind in ('D', 'Z'):
        f.path([P(-B, -11), P(-B, 11), P(B, 0)], c=c, w=1.8, fill=c, close=True)
        f.l(*P(B, -11), *P(B, 11), c=c, w=2.4)
        if kind == 'Z':
            f.l(*P(B, -11), *P(B - 6, -15), c=c, w=2.4); f.l(*P(B, 11), *P(B + 6, 15), c=c, w=2.4)
    if lab:
        o = off if off is not None else {'R': 22, 'C': 30, 'Cv': 32, 'L': 22, 'D': 22, 'Z': 24, 'X': 26}[kind]
        dx, dy = -nx * side, -ny * side
        tx, ty = mx + dx * o, my + dy * o
        if abs(dx) > abs(dy):
            f.t(tx, ty + 5, lab, anchor='start' if dx > 0 else 'end', size=size, c=lc or c)
        else:
            f.t(tx, ty + (5 if dy > 0 else 0) + (10 if dy > 0 else 0), lab, size=size, c=lc or c)


def gnd(f, x, y):
    f.l(x, y, x, y + 10); f.l(x - 13, y + 10, x + 13, y + 10, w=2.4)
    f.l(x - 8, y + 15, x + 8, y + 15, w=2); f.l(x - 3, y + 20, x + 3, y + 20, w=1.6)


def acsrc(f, x, y, r=20, lab=None):
    f.circle(x, y, r, fill='#ffffff')
    f.path([(x - r * 0.6 + i * r * 1.2 / 30, y - r * 0.38 * math.sin(2 * math.pi * i / 30)) for i in range(31)], c=TX, w=1.6)
    if lab: f.t(x - r - 8, y + 5, lab, anchor='end', size=14)


def antenna(f, x, y, h=40):
    f.l(x, y, x, y - h); f.l(x, y - h + 14, x - 14, y - h - 4); f.l(x, y - h + 14, x + 14, y - h - 4); f.l(x, y - h, x, y - h - 6)


def freqaxis(f, x0, x1, y, fa, fb, ticks=(), unit='MHz', log=False, size=13):
    X = (lambda v: x0 + (math.log10(v) - math.log10(fa)) / (math.log10(fb) - math.log10(fa)) * (x1 - x0)) if log else \
        (lambda v: x0 + (v - fa) / (fb - fa) * (x1 - x0))
    f.arrow([(x0, y), (x1 + 18, y)], c=TX, w=1.6)
    f.t(x1 + 18, y + 22, f'f [{unit}]' if unit else 'f', anchor='end', size=size)
    for v, lab in ticks:
        f.l(X(v), y - 4, X(v), y + 4, w=1.4)
        f.t(X(v), y + 20, lab, size=size)
    return X


def bar(f, x, y, h, c=BL, lab=None, w=4, size=13, lc=None, anchor='middle'):
    f.l(x, y, x, y - h, c=c, w=w)
    f.circle(x, y - h, 4, fill=c, stroke=c, sw=1)
    if lab: f.t(x + {'middle': 0, 'start': -4, 'end': 4}[anchor], y - h - 10, lab, size=size, c=lc or c, anchor=anchor)


def reson(fr, f0, Q):
    return 1 / (1 + (Q * (fr / f0 - f0 / fr)) ** 2)

# ---------------------------------------------------------------- obrazovka osciloskopu (průběhy v čase)
SC_COL = ['#f4d03f', '#5dade2', '#ec7fd0', '#58d68d']
LANE = 88
NOTE = 'Měřítko je schematické – vf kmitočty jsou ve skutečnosti mnohem vyšší vůči nf průběhům.'


def cs(v): return math.cos(2 * math.pi * v)
def sn(v): return math.sin(2 * math.pi * v)
def clip(v, a): return max(-a, min(a, v))


_NZ = [(53 + 37 * k % 97 + k * 3.1, (k * 2.399) % 6.283) for k in range(14)]


def noise(t):
    """deterministický „šum“ (součet mnoha nesouměřitelných sinusovek)"""
    return sum(math.sin(2 * math.pi * fk * t * 1.7 + ph) for fk, ph in _NZ) / 4.2


def scope_h(k, note=True):
    return 34 + LANE * k + (50 if note else 14)


def scope(f, y0, chans, tb='měřítko schematické', note=None, env=None, title=None, X0=30, SW=700):
    """chans = [(popis, odečet, fn(t) pro t∈⟨0,1⟩ s rozsahem ±1)]; env = [(kanál, fn)] čárkovaná obálka"""
    k = len(chans)
    Y0, SH = y0 + 34, LANE * k
    f.rect(X0 - 12, y0, SW + 24, scope_h(k, bool(note)), fill='#2b2b2b', stroke='#111111', sw=2, rx=10)
    f.rect(X0, Y0, SW, SH, fill='#0d1117', stroke='#555555', sw=1.2)
    f.t(X0, Y0 - 12, title or f'osciloskop – průběhy v čase ({k} kanály)' if k < 5 else title, size=13, c='#dddddd', anchor='start', w='bold')
    f.t(X0 + SW, Y0 - 12, tb, size=12, c='#bbbbbb', anchor='end')
    for j in range(1, 10):
        f.l(X0 + j * SW / 10, Y0, X0 + j * SW / 10, Y0 + SH, '#2a3340', 0.8, '2,3')
    for j in range(1, 2 * k):
        f.l(X0, Y0 + j * SH / (2 * k), X0 + SW, Y0 + j * SH / (2 * k), '#2a3340', 0.8, '2,3')
    for i, (lab, meas, fn) in enumerate(chans):
        col = SC_COL[i % 4]
        yc, amp = Y0 + LANE * i + LANE / 2 + 7, LANE * 0.31
        n = 2400
        f.path([(X0 + SW * j / n, yc - amp * fn(j / n)) for j in range(n + 1)], c=col, w=1.1)
        f.rect(X0 + 4, Y0 + LANE * i + 4, 36, 17, fill=col, stroke='none', rx=3)
        f.t(X0 + 22, Y0 + LANE * i + 17, f'CH{i + 1}', size=11, c='#000000', w='bold')
        f.t(X0 + 46, Y0 + LANE * i + 17, lab, size=12, c=col, anchor='start')
        if meas: f.t(X0 + SW - 6, Y0 + LANE * i + 17, meas, size=12, c=col, anchor='end')
    for i, fn in (env or []):
        yc, amp = Y0 + LANE * i + LANE / 2 + 7, LANE * 0.31
        f.path([(X0 + SW * j / 600, yc - amp * fn(j / 600)) for j in range(601)], c='#ffffff', w=1, dash='4,3')
    if note:
        f.t(X0 + 7, Y0 + SH + 20, note, size=11.5, c='#cccccc', anchor='start')


# ================================================================ c) Elektrické obvody
def c_lc_par():
    f = F(300)
    yt, yb = 70, 230
    f.wire((40, yt), (300, yt)); f.wire((40, yb), (300, yb))
    f.term(40, yt); f.term(40, yb)
    for x in (90, 180): f.dot(x, yt); f.dot(x, yb)
    part(f, 'L', (90, yt), (90, yb), 'L', side=-1)
    part(f, 'C', (180, yt), (180, yb), 'C₁', side=-1)
    f.wire((180, yt), (270, yt), c=RED); f.wire((180, yb), (270, yb), c=RED)
    part(f, 'C', (270, yt), (270, yb), 'C₂', side=-1, c=RED)
    f.t(270, yb + 32, 'přidaný kondenzátor', size=13, c=RED)
    f.t(170, 32, 'C = C₁ + C₂ (paralelně se kapacity sčítají)', size=13)
    x0, y0, w, h = 380, 250, 340, 180
    f.axes(x0, y0, w, h, 'f', 'U, |Z|')
    f.plot(lambda v: reson(v, 0.65, 5), x0, y0, w - 20, h - 25, 0.2, 1.1, 0, 1)
    f.plot(lambda v: reson(v, 0.45, 5), x0, y0, w - 20, h - 25, 0.2, 1.1, 0, 1, c=RED)
    X = lambda v: x0 + (v - 0.2) / 0.9 * (w - 20)
    f.l(X(0.65), y0, X(0.65), y0 - h + 25, BL, 1.2, '4,4'); f.l(X(0.45), y0, X(0.45), y0 - h + 25, RED, 1.2, '4,4')
    f.t(X(0.65), y0 + 20, 'f₀', c=BL, w='bold'); f.t(X(0.45), y0 + 20, 'f₀′', c=RED, w='bold')
    f.arrow([(X(0.62), y0 - h + 12), (X(0.49), y0 - h + 12)], c=RED, w=1.8)
    f.t(550, 32, 'f₀ = 1 / (2π·√(L·C))', size=16, w='bold')
    return f, ('Paralelní LC obvod. Připojením dalšího kondenzátoru se celková kapacita zvětší, a protože C je ve '
               'vzorci pod odmocninou ve jmenovateli, rezonanční kmitočet f₀ klesne (červená křivka). Totéž by udělalo '
               'zvětšení indukčnosti L.')


def c_graetz():
    f = F(330)
    T, R_, B, L_ = (210, 60), (300, 150), (210, 240), (120, 150)
    for a, b in [(L_, T), (T, R_), (L_, B), (B, R_)]:
        part(f, 'D', a, b)
    for p in (T, R_, B, L_): f.dot(*p)
    f.wire(T, (210, 30), (50, 30), (50, 128)); acsrc(f, 50, 150, lab='~')
    f.wire((50, 172), (50, 275), (210, 275), B)
    f.wire(R_, (380, 150)); f.wire(L_, (120, 305), (380, 305))
    part(f, 'R', (380, 150), (380, 305), 'zátěž')
    f.t(368, 140, '+', size=20, w='bold', c=RED); f.t(368, 325, '−', size=20, w='bold', c=BL)
    f.t(210, 160, '4 diody\nv můstku', size=13, c=GR)
    f.t(585, 40, 'vstup (střídavé napětí)', size=13, w='bold')
    f.l(470, 105, 720, 105, GR, 1)
    f.sine(470, 105, 250, 45, 2)
    f.t(585, 190, 'výstup – obě půlvlny', size=13, w='bold')
    f.l(470, 290, 720, 290, GR, 1)
    f.sine(470, 290, 250, 80, 2, f=lambda u: abs(math.sin(u)), c=RED)
    f.t(585, 318, 'pulzující stejnosměrné napětí 2× 50 Hz = 100 Hz', size=12, c=GR)
    return f, ('Graetzův můstek: v každé půlperiodě vedou dvě protilehlé diody a proud tekoucí zátěží má stále stejný '
               'směr. Využijí se obě půlvlny, proto jde o dvoucestný usměrňovač (zvlnění má dvojnásobný kmitočet, '
               'snáze se vyhlazuje).')


def _par2(f, l1, l2, x0=40):
    yt, yb = 60, 200
    f.wire((x0, yt), (x0 + 210, yt)); f.wire((x0, yb), (x0 + 210, yb))
    f.term(x0, yt); f.term(x0, yb)
    for x in (x0 + 90, x0 + 190):
        f.dot(x, yt); f.dot(x, yb)
    part(f, 'R', (x0 + 90, yt), (x0 + 90, yb), l1)
    part(f, 'R', (x0 + 190, yt), (x0 + 190, yb), l2)
    f.t(x0 - 4, 138, 'R', size=16, w='bold', anchor='end')


def c_rpar():
    f = F(240)
    _par2(f, 'R₁', 'R₂')
    f.t(510, 85, 'R = R₁ · R₂ / (R₁ + R₂)', size=22, w='bold', c=BL)
    f.t(510, 125, 'obecně: 1/R = 1/R₁ + 1/R₂ + …', size=15)
    f.t(510, 165, 'Výsledný odpor je vždy menší\nnež nejmenší z paralelních odporů.', size=14, c=GR)
    return f, ('Paralelní zapojení: proud se rozdělí do obou větví, takže celkem prochází větší proud než jedním '
               'odporem – výsledný odpor je menší. Pro dva odpory platí „součin lomeno součtem“.')


def c_cpar():
    f = F(240)
    yt, yb = 60, 200
    f.wire((40, yt), (330, yt)); f.wire((40, yb), (330, yb)); f.term(40, yt); f.term(40, yb)
    for k, x in enumerate((130, 230, 330)):
        f.dot(x, yt); f.dot(x, yb)
        part(f, 'C', (x, yt), (x, yb), '10 nF')
    f.t(420, 140, '=', size=36, w='bold')
    f.wire((480, yt), (600, yt)); f.wire((480, yb), (600, yb)); f.term(480, yt); f.term(480, yb)
    part(f, 'C', (600, yt), (600, yb), '30 nF', lc=RED)
    f.t(380, 232, 'paralelně: C = C₁ + C₂ + C₃ = 10 + 10 + 10 = 30 nF', size=15, w='bold', c=BL)
    return f, ('Paralelně spojené kondenzátory se chovají jako jeden kondenzátor se součtem ploch desek – kapacity se '
               'sčítají. (U odporů je to naopak: v sérii se sčítají odpory.)')


def c_rpar_num():
    f = F(240)
    _par2(f, '2 kΩ', '3 kΩ')
    f.t(520, 75, 'R = R₁ · R₂ / (R₁ + R₂)', size=18, c=BL)
    f.t(520, 115, 'R = 2 · 3 / (2 + 3) = 6 / 5', size=18)
    f.t(520, 160, 'R = 1,2 kΩ', size=24, w='bold', c=RED)
    f.t(520, 200, 'kontrola: 1,2 kΩ < 2 kΩ (nejmenší) ✓', size=14, c=GR)
    return f, 'Výpočet podle vzorce „součin lomeno součtem“; výsledek musí být menší než menší z obou odporů.'


def c_pi():
    f = F(280)
    yt, yb = 80, 210
    f.term(40, yt); f.term(40, yb); f.term(350, yt); f.term(350, yb)
    f.wire((40, yt), (110, yt)); f.wire((280, yt), (350, yt))
    part(f, 'L', (110, yt), (280, yt), 'L (cívka v podélné větvi)')
    f.wire((40, yb), (350, yb))
    for x, lab in ((90, 'C₁'), (300, 'C₂')):
        f.dot(x, yt); f.dot(x, yb)
        part(f, 'C', (x, yt), (x, yb), lab, side=-1 if x < 200 else 1)
    f.t(40, 245, 'vstup', size=13); f.t(350, 245, 'výstup', size=13)
    f.t(195, 160, 'tvar písmene π', size=13, c=GR, italic=True)
    x0, y0, w, h = 430, 230, 290, 170
    f.axes(x0, y0, w, h, 'f', 'propustnost')
    f.plot(lambda v: 1 / math.sqrt(1 + v ** 6), x0, y0, w - 20, h - 30, 0, 2.4, 0, 1.05, c=BL)
    X = lambda v: x0 + v / 2.4 * (w - 20)
    f.l(X(1), y0, X(1), y0 - h + 30, GR, 1.2, '4,4'); f.t(X(1), y0 + 20, 'f mezní', size=13)
    f.t(X(0.45), y0 - h + 18, 'propouští', size=13, c=GRN); f.t(X(1.85), y0 - 60, 'potlačí\n(harmonické)', size=13, c=RED)
    return f, ('π článek jako dolní propust: kondenzátory napříč (paralelně ke vstupu a výstupu) svádějí vysoké kmitočty '
               'k zemi, cívka v podélné větvi jim klade velký odpor. Nízké kmitočty projdou, harmonické se potlačí.')


def c_overmod():
    f = F(538)
    for k, (x0, title, bad) in enumerate([(40, 'správně vybuzený SSB signál', False), (400, 'přemodulovaný SSB signál', True)]):
        y0, w = 200, 320
        f.t(x0 + w / 2, 28, title, size=15, w='bold', c=RED if bad else GRN)
        f.arrow([(x0, y0), (x0 + w, y0)], c=TX, w=1.5); f.t(x0 + w, y0 + 22, 'f', anchor='end', size=13)
        cx = x0 + w / 2
        if bad:
            pts = [(x0 + 10, y0)]
            for i in range(61):
                u = i / 60
                pts.append((x0 + 10 + u * (cx - 60 - x0 - 10), y0 - 70 * (u ** 3)))
            f.path(pts + [(cx - 60, y0)], c=RED, fill=RED, op=0.25, w=1.5)
            pts = [(cx + 60, y0)]
            for i in range(61):
                u = i / 60
                pts.append((cx + 60 + u * (x0 + w - 10 - cx - 60), y0 - 70 * ((1 - u) ** 3)))
            f.path(pts + [(x0 + w - 10, y0)], c=RED, fill=RED, op=0.25, w=1.5)
            f.t(x0 + 55, y0 - 80, 'rozstřik\n(splatter)', size=12, c=RED); f.t(x0 + w - 55, y0 - 80, 'ruší\nsousedy', size=12, c=RED)
        f.path([(cx - 60, y0), (cx - 60, y0 - 120), (cx + 60, y0 - 120), (cx + 60, y0)], c=BL, fill=BLF, op=0.9, w=2)
        f.t(cx, y0 - 60, 'hovor', size=14, c=BL, w='bold')
        f.arrow([(cx - 60, y0 + 30), (cx + 60, y0 + 30)] if not bad else [(x0 + 15, y0 + 30), (x0 + w - 15, y0 + 30)],
                c=GRN if not bad else RED, w=1.6, both=True)
        f.t(cx, y0 + 52, '≈ 2,7 kHz' if not bad else 'šířka pásma mnohonásobně větší', size=13, c=GRN if not bad else RED)
    ssb2 = lambda t: 0.5 * (cs(42 * t) + cs(45 * t))
    scope(f, 270, [
        ('správně vybuzený SSB signál (dva tóny)', 'obálka hladká', lambda t: 0.9 * ssb2(t)),
        ('přemodulovaný: špičky obálky jsou ořezané', 'zkreslení → nové kmitočty', lambda t: clip(1.7 * ssb2(t), 0.8) / 0.8),
    ], env=[(0, lambda t: 0.9 * abs(math.cos(math.pi * 3 * t)))], note=NOTE)
    return f, ('Při přemodulování (příliš velký zisk mikrofonu, přebuzený koncový stupeň) se signál ořezává – vzniká '
               'zkreslení a nové kmitočtové složky. Signál se „rozteče“ do okolí a ruší stanice na sousedních kmitočtech.')


def c_psfilter():
    f = F(350)
    y1, y2 = 70, 190
    acsrc(f, 50, 130)
    f.wire((50, 110), (50, y1), (95, y1)); f.wire((50, 150), (50, y2), (95, y2))
    for x in (110, 140):
        d = 'M %d,%d' % (x, y1 + 5)
        for k in range(4):
            d += ' A 14 14 0 0 %d %d,%d' % (1 if x == 140 else 0, x, y1 + 5 + (k + 1) * 27.5)
        f.a(f'<path d="{d}" stroke="{TX}" stroke-width="2" fill="none"/>')
    f.l(122, y1, 122, y2, w=2); f.l(128, y1, 128, y2, w=2)
    f.wire((95, y1), (110, y1), (110, y1 + 5)); f.wire((95, y2), (110, y2), (110, y1 + 115))
    f.wire((140, y1 + 5), (140, y1), (170, y1)); f.wire((140, y1 + 115), (140, y2), (170, y2))
    f.t(125, y2 + 30, 'transformátor', size=12)
    f.box(170, y1 - 10, 80, y2 - y1 + 20, 'usměr-\nňovač', size=13)
    f.wire((250, y1), (420, y1)); f.wire((250, y2), (690, y2))
    part(f, 'L', (420, y1), (560, y1), 'L', c=RED, lc=RED)
    f.wire((560, y1), (690, y1))
    for x, lab in ((330, 'C₁'), (630, 'C₂')):
        f.dot(x, y1); f.dot(x, y2); part(f, 'C', (x, y1), (x, y2), lab, c=RED, lc=RED)
    f.term(690, y1); f.term(690, y2); f.t(708, y1 + 5, '+', size=18, w='bold'); f.t(708, y2 + 5, '−', size=18, w='bold')
    f.t(480, 24, 'filtr: kondenzátory a tlumivka', size=14, w='bold', c=RED)
    yw = 290
    for x0, fn, lab in [(30, lambda u: math.sin(u), 'střídavé'),
                        (200, lambda u: abs(math.sin(u)), 'pulzující'),
                        (390, lambda u: 0.82 + 0.18 * abs(math.cos(u)) ** 0.3, 'zvlněné'),
                        (580, lambda u: 0.9, 'vyhlazené')]:
        f.l(x0, yw, x0 + 130, yw, GR, 1)
        f.sine(x0, yw, 130, 35, 2, f=fn, c=BL)
        f.t(x0 + 65, yw + 52, lab, size=12, c=GR)
    return f, ('Síťový zdroj: transformátor → usměrňovač → filtr. Kondenzátory se nabíjejí ve špičkách a vybíjejí do '
               'zátěže, tlumivka brání rychlým změnám proudu. Výsledkem je téměř hladké stejnosměrné napětí.')


def c_osc():
    f = F(270)
    f.path([(260, 70), (260, 170), (360, 120)], c=BL, fill='#eef3fb', close=True, w=2)
    f.t(292, 126, 'A', size=20, w='bold', c=BL)
    f.t(300, 190, 'zesilovač', size=13)
    f.wire((360, 120), (560, 120)); f.dot(450, 120)
    f.arrow([(560, 120), (610, 120)], c=TX, w=1.8); f.t(640, 112, 'výstup', size=13, anchor='start')
    f.box(300, 205, 120, 46, 'zpětná\nvazba β', size=13, fill='#fdecea', stroke=RED)
    f.wire((450, 120), (450, 228), (420, 228))
    f.l(300, 228, 200, 228); f.l(200, 228, 200, 120)
    f.arrow([(200, 120), (258, 120)], c=TX, w=1.8)
    f.t(205, 100, '+ (ve fázi)', size=14, c=RED, w='bold')
    pts = [(480 + i * 1.2, 75 - (i / 125) * 26 * math.sin(i / 5)) for i in range(126)]
    f.path(pts, c=GRN, w=1.8)
    f.t(560, 40, 'kmity se rozkmitají a udrží', size=13, c=GRN)
    f.t(100, 40, 'podmínka kmitání:', size=14, w='bold')
    f.t(100, 64, 'A · β ≥ 1', size=17, c=RED, w='bold')
    f.t(100, 88, 'fáze 0° (360°)', size=14, c=RED)
    return f, ('Oscilátor = zesilovač, jehož část výstupního signálu se vrací na vstup ve fázi (kladná zpětná vazba). '
               'Pokud zesílení vyrovná ztráty ve zpětné vazbě (A·β ≥ 1), obvod se rozkmitá sám. Záporná zpětná vazba '
               'naopak kmitání brání.')


def coil(f, x, y1, y2, n=5, side=1, c=TX):
    """svislá cívka z (x, y1) do (x, y2); side=1 závity vpravo, -1 vlevo"""
    r = (y2 - y1) / n / 2
    d = 'M %.1f,%.1f' % (x, y1)
    for k in range(n):
        d += ' A %.1f %.1f 0 0 %d %.1f,%.1f' % (r, r, 1 if side > 0 else 0, x, y1 + (k + 1) * 2 * r)
    f.a(f'<path d="{d}" stroke="{c}" stroke-width="2" fill="none"/>')


def c_bfo():
    f = F(326 + 436 + 6)
    # ---------------- schéma produktového detektoru (diodový kruhový směšovač)
    yt, yb, ym = 90, 210, 150
    f.t(380, 24, 'produktový detektor = směšovač, do kterého BFO dodává chybějící nosnou', size=15, w='bold')
    # vstup
    f.term(40, yt); f.term(40, yb)
    f.t(30, ym - 6, 'z mf\nfiltru', size=13, anchor='start')
    f.t(30, yb + 34, 'SSB / CW\n455 kHz', size=12, anchor='start', c=BL)
    f.wire((40, yt), (130, yt), (130, yt + 5)); f.wire((40, yb), (130, yb), (130, yb - 5))
    coil(f, 130, yt + 5, yb - 5, side=1)
    f.l(146, yt, 146, yb, w=2); f.l(152, yt, 152, yb, w=2)
    coil(f, 168, yt + 5, yb - 5, side=-1)
    f.t(149, yt - 12, 'T1', size=13, w='bold')
    # ring
    P, R, Q, S = (250, yt), (400, yt), (250, yb), (400, yb)
    f.wire((168, yt + 5), (168, yt), P); f.wire((168, yb - 5), (168, yb), Q)
    part(f, 'D', P, R); part(f, 'D', Q, S)
    pt = lambda a, b, t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    for (a, b, t0, t1) in ((R, Q, 0.12, 0.42), (S, P, 0.58, 0.88)):
        f.l(*a, *pt(a, b, t0)); part(f, 'D', pt(a, b, t0), pt(a, b, t1)); f.l(*pt(a, b, t1), *b)
    for p in (P, R, Q, S): f.dot(*p)
    f.rect(225, yt - 28, 200, yb - yt + 56, stroke=RED, sw=1.3, dash='6,4', rx=8)
    f.t(325, yb + 48, 'kruh 4 diod (ring mixer)', size=12, c=RED)
    # střední odbočka T1 -> zem
    f.wire((168, ym), (200, ym)); gnd(f, 200, ym)
    # T2
    f.wire(R, (480, yt), (480, yt + 5)); f.wire(S, (480, yb), (480, yb - 5))
    coil(f, 480, yt + 5, yb - 5, side=1)
    f.l(496, yt, 496, yb, w=2); f.l(502, yt, 502, yb, w=2)
    coil(f, 518, yt + 5, yb - 5, side=-1)
    f.t(499, yt - 12, 'T2', size=13, w='bold')
    f.wire((518, yt + 5), (518, yt), (560, yt)); f.wire((518, yb - 5), (518, yb), (540, yb)); gnd(f, 540, yb)
    f.box(560, yt - 30, 170, 62, 'BFO 455,000 kHz\n(krystalový oscilátor)', size=12, fill='#fdecea', stroke=RED, wt='bold')
    # nf výstup ze střední odbočky T2
    f.dot(480, ym); f.wire((480, ym), (445, ym), (445, 290), (520, 290))
    f.t(452, 275, 'nf', size=12, c=GRN, anchor='start')
    f.box(520, 265, 110, 50, 'dolní propust\n< 3 kHz', size=12, fill='#eaf5ea', stroke=GRN)
    f.arrow([(630, 290), (650, 290)], c=TX, w=1.8)
    f.box(650, 265, 70, 50, 'nf zes.', size=12)
    f.arrow([(720, 290), (735, 290)], c=TX, w=1.8)
    f.path([(736, 283), (742, 283), (750, 274), (750, 306), (742, 297), (736, 297)], c=TX, w=1.6, fill='#fff', close=True)
    FC, F1, F2 = 40, 2, 5
    ssb = lambda t: 0.5 * (cs((FC + F1) * t) + cs((FC + F2) * t))
    scope(f, 326, [
        ('vstup: mf SSB signál (dva tóny)', '455,70 + 456,75 kHz', ssb),
        ('BFO – nosná stálé amplitudy', '455,00 kHz', lambda t: cs(FC * t)),
        ('výstup směšovače = CH1 × CH2', 'nf + zbytky vf ≈ 910 kHz', lambda t: ssb(t) * cs(FC * t) * 1.15),
        ('po dolní propusti: nf signál (slyšíme)', '0,70 + 1,75 kHz', lambda t: 0.4 * (cs(F1 * t) + cs(F2 * t))),
    ], tb='časová základna: 0,5 ms/díl', env=[(0, lambda t: abs(math.cos(math.pi * (F2 - F1) * t)))],
       note='Měřítko je schematické: nosná 455 kHz kmitá ve skutečnosti asi 400× rychleji než nf tóny –\n'
            'osciloskop by ji při 0,5 ms/díl ukázal jen jako vyplněný pás.')
    return f, ('Schéma: mezifrekvenční SSB nebo CW signál (T1) a nosná z BFO (T2) se setkají v kruhu čtyř diod, který '
               'pracuje jako přepínač s kmitočtem BFO – signál se tím násobí nosnou. Osciloskop: CH1 – SSB signál se dvěma '
               'tóny (nosná chybí, obálka kolísá jejich rozdílem); CH2 – BFO; CH3 – výstup směšovače, v němž je už vidět '
               'nf průběh, na kterém „sedí“ vf složky součtového kmitočtu (≈ 910 kHz); CH4 – po dolní propusti zbývá jen '
               'nf signál s původními tóny 0,7 a 1,75 kHz (f nf = f signál − f BFO). Bez BFO by tóny nevznikly. V praxi se '
               'tomuto detektoru říká produktový (směšovací); ČTÚ v odpovědi uvádí „poměrový“.')


def c_diodrc():
    f = F(290)
    y0 = 140
    f.term(40, y0); f.wire((40, y0), (120, y0))
    for k, x in enumerate((120, 360)):
        xe = x + 200
        f.dot(x, y0); f.dot(xe, y0)
        part(f, 'D', (x, y0), (xe, y0), f'D{k + 1}')
        f.wire((x, y0), (x, 80), (x + 70, 80)); f.wire((xe - 70, 80), (xe, 80), (xe, y0))
        part(f, 'C', (x + 70, 80), (xe - 70, 80), 'C', c=BL, lc=BL)
        f.wire((x, y0), (x, 210), (x + 70, 210)); f.wire((xe - 70, 210), (xe, 210), (xe, y0))
        part(f, 'R', (x + 70, 210), (xe - 70, 210), 'R', side=-1, c=GRN, lc=GRN)
    f.wire((560, y0), (620, y0)); f.term(620, y0)
    f.t(380, 20, 'C – pohltí rychlé napěťové špičky (zákmity při spínání)', size=13, c=BL)
    f.t(380, 282, 'R – rovnoměrně rozdělí napětí mezi diody v sérii', size=13, c=GRN)
    return f, ('Kondenzátor paralelně k diodě zkratuje rychlé napěťové špičky, které by diodu mohly prorazit. Odpor '
               'vyrovnává napětí na diodách řazených do série (například ve vysokonapěťových zdrojích elektronkových PA).')


def c_zener():
    f = F(290)
    yt, yb = 70, 220
    f.term(40, yt); f.term(40, yb); f.t(48, 140, 'U vst\n(kolísá)', size=13, anchor='start')
    f.wire((40, yt), (80, yt)); part(f, 'R', (80, yt), (200, yt), 'R (srážecí)')
    f.wire((200, yt), (330, yt)); f.wire((40, yb), (330, yb))
    f.dot(240, yt); f.dot(240, yb)
    part(f, 'Z', (240, yb), (240, yt), 'ZD', side=1, c=RED, lc=RED)
    f.term(330, yt); f.term(330, yb); f.t(340, 150, 'U výst\n= U z', size=13, anchor='start', c=RED)
    x0, y0 = 600, 160
    f.arrow([(430, y0), (740, y0)], c=TX, w=1.5); f.arrow([(x0, 270), (x0, 30)], c=TX, w=1.5)
    f.t(740, y0 + 20, 'U', anchor='end', size=14); f.t(x0 + 8, 40, 'I', anchor='start', size=14)
    f.path([(x0, y0), (x0 + 60, y0 - 4), (x0 + 85, y0 - 40), (x0 + 95, y0 - 120)], c=BL, w=2.4)
    f.path([(x0, y0), (x0 - 120, y0 + 3), (x0 - 135, y0 + 20), (x0 - 140, y0 + 105)], c=RED, w=2.6)
    f.l(x0 - 133, y0 - 6, x0 - 133, y0 + 108, RED, 1, '4,4')
    f.t(x0 - 133, y0 - 14, 'U z', size=14, c=RED, w='bold')
    f.t(x0 - 150, y0 + 70, 'napětí se\nskoro nemění', size=12, c=RED, anchor='end')
    f.t(x0 + 105, y0 - 80, 'propustný\nsměr', size=12, anchor='start', c=BL)
    f.t(x0 - 60, y0 - 40, 'závěrný\nsměr', size=12, c=GR)
    return f, ('Zenerova dioda je zapojena v závěrném směru. Po dosažení Zenerova napětí U z jí může protékat velmi '
               'různý proud, ale napětí na ní zůstává téměř stálé. Přebytečné napětí se ztratí na sériovém odporu R.')


def c_lc_series():
    f = F(270)
    f.term(40, 80); f.wire((40, 80), (70, 80))
    part(f, 'L', (70, 80), (180, 80), 'L'); part(f, 'C', (180, 80), (270, 80), 'C')
    f.wire((270, 80), (300, 80)); f.term(300, 80)
    f.t(170, 150, 'na f₀: X L = X C,\nreaktance se odečtou →\nZ = 0 Ω (ideální obvod)', size=14)
    x0, y0, w, h = 380, 240, 340, 200
    f.axes(x0, y0, w, h, 'f', '|Z|')
    f.plot(lambda v: abs(v - 1 / v) * 1.6, x0, y0, w - 20, h - 20, 0.25, 2.3, 0, 3, c=BL)
    X = lambda v: x0 + (v - 0.25) / 2.05 * (w - 20)
    f.l(X(1), y0, X(1), y0 - h + 20, GR, 1.2, '4,4'); f.t(X(1), y0 + 20, 'f₀', w='bold')
    f.t(X(1) + 6, y0 - 10, 'Z = 0', anchor='start', c=RED, w='bold')
    return f, ('Sériový rezonanční obvod: na rezonančním kmitočtu se induktivní a kapacitní reaktance navzájem '
               'vyruší. Ideální obvod (bez ztrát) má nulovou impedanci, propouští tedy proud bez omezení.')


def c_lc_parz():
    f = F(270)
    yt, yb = 60, 200
    f.term(40, yt); f.term(40, yb); f.wire((40, yt), (220, yt)); f.wire((40, yb), (220, yb))
    for x in (120, 220): f.dot(x, yt); f.dot(x, yb)
    part(f, 'L', (120, yt), (120, yb), 'L', side=-1); part(f, 'C', (220, yt), (220, yb), 'C')
    f.t(150, 245, 'na f₀ proud jen „krouží“ mezi L a C;\nz vnějšku obvod neodebírá proud → Z = ∞', size=13)
    x0, y0, w, h = 380, 240, 340, 200
    f.axes(x0, y0, w, h, 'f', '|Z|')
    f.plot(lambda v: 0.5 / max(abs(v - 1 / v), 1e-3), x0, y0, w - 20, h - 20, 0.25, 2.3, 0, 3, c=BL, n=600)
    X = lambda v: x0 + (v - 0.25) / 2.05 * (w - 20)
    f.l(X(1), y0, X(1), y0 - h + 20, GR, 1.2, '4,4'); f.t(X(1), y0 + 20, 'f₀', w='bold')
    f.t(X(1) + 10, y0 - h + 26, 'Z → ∞', anchor='start', c=RED, w='bold')
    return f, ('Paralelní rezonanční obvod se chová opačně než sériový: na rezonanci má ideální obvod nekonečnou '
               'impedanci (skutečný velkou). Proto se používá jako laděný obvod zesilovačů a oscilátorů.')


def c_pll():
    f = F(260)
    f.box(20, 40, 130, 56, 'krystalový\nref. oscilátor', size=13, fill='#fff6e0', stroke=ORA)
    f.arrow([(150, 68), (200, 68)], c=TX, w=1.8)
    f.box(200, 40, 120, 56, 'fázový\ndetektor', size=13, fill='#fdecea', stroke=RED)
    f.arrow([(320, 68), (370, 68)], c=TX, w=1.8)
    f.box(370, 40, 110, 56, 'filtr\n(dolní propust)', size=13)
    f.arrow([(480, 68), (530, 68)], c=TX, w=1.8)
    f.box(530, 40, 90, 56, 'VCO', size=15, wt='bold')
    f.arrow([(620, 68), (735, 68)], c=TX, w=1.8); f.t(735, 56, 'výstup', anchor='end', size=13)
    f.dot(660, 68); f.wire((660, 68), (660, 170), (460, 170))
    f.box(330, 145, 130, 50, 'dělič ÷ N\n(volí kmitočet)', size=13)
    f.wire((330, 170), (260, 170)); f.arrow([(260, 170), (260, 98)], c=TX, w=1.8)
    f.t(85, 125, 'f ref', size=14, c=ORA, w='bold')
    f.t(360, 120, 'ladicí napětí', size=12, c=GR)
    f.t(380, 238, 'smyčka se ustálí, když f výst / N = f ref → f výst = N · f ref', size=15, w='bold', c=BL)
    return f, ('PLL syntezátor: fázový detektor stále porovnává fázi děleného signálu VCO s fází krystalového '
               'referenčního oscilátoru a ladicím napětím VCO doladí. Výstup má stabilitu krystalu; kmitočet se '
               'mění dělicím poměrem N.')


# ================================================================ d) Rádiové přijímače
def d_rit():
    f = F(210)
    X = freqaxis(f, 40, 700, 160, 14.1985, 14.2015, [(14.199, '14,199'), (14.200, '14,200'), (14.201, '14,201')])
    bar(f, X(14.2000), 160, 90, c=RED, lab='vysílání 14,2000 MHz', size=13)
    bar(f, X(14.2006), 160, 70, c=BL, lab='RX (RIT +0,6 kHz)', size=13)
    f.arrow([(X(14.2000), 120), (X(14.2006), 120)], c=BL, w=1.6, both=True)
    f.t(370, 30, 'RIT posune jen kmitočet příjmu – vysílám dál na původním kmitočtu', size=14, w='bold')
    return f, ('RIT (Receiver Incremental Tuning): jemné rozladění přijímače o několik set Hz, např. když protistanice '
               'vysílá trochu vedle. Vysílací kmitočet zůstává stejný (obdobně XIT rozladí jen vysílač).')


def d_upconv():
    f = F(300)
    antenna(f, 40, 90)
    f.arrow([(40, 90), (40, 110), (70, 110)], c=TX, w=1.8)
    f.box(70, 85, 130, 50, 'dolní propust\n0–30 MHz', size=13)
    f.arrow([(200, 110), (248, 110)], c=TX, w=1.8)
    f.mixer(270, 110)
    f.box(215, 170, 110, 46, 'VFO\n45–75 MHz', size=13)
    f.arrow([(270, 170), (270, 132)], c=TX, w=1.8)
    f.arrow([(292, 110), (340, 110)], c=TX, w=1.8)
    f.box(340, 85, 150, 50, '1. mf 45 MHz\nkrystalový filtr', size=13, fill='#fdecea', stroke=RED)
    f.arrow([(490, 110), (530, 110)], c=TX, w=1.8)
    f.box(530, 85, 180, 50, '2. směšovač → 2. mf\n(455 kHz, 10,7 MHz…)', size=12)
    X = freqaxis(f, 40, 690, 270, 0, 80, [(0, '0'), (30, '30'), (45, '45'), (75, '75')])
    f.rect(X(0), 240, X(30) - X(0), 30, fill=BLF, stroke=BL, sw=1.2); f.t((X(0) + X(30)) / 2, 260, 'přijímané pásmo', size=12, c=BL)
    bar(f, X(45), 270, 40, c=RED, lab='1. mf', size=12)
    f.rect(X(45.5), 248, X(75) - X(45.5), 22, fill='#eeeeee', stroke=GR, sw=1); f.t((X(46) + X(75)) / 2, 263, 'VFO', size=12)
    return f, ('Up-konvertor: 1. mezifrekvence (např. 45 MHz) leží nad celým přijímaným rozsahem. Zrcadlové kmitočty '
               '(90–120 MHz) jsou daleko a snadno je potlačí jednoduchá dolní propust, ladí se jedním VFO bez přepínání.')


def _superhet(f, y, hl=None, bfo=True):
    xs = [(30, 'vf\nzesilovač'), (160, 'směšovač'), (300, 'mf\nzesilovač'), (440, 'detektor'), (580, 'nf\nzesilovač')]
    antenna(f, 15, y - 25, 32)
    f.wire((15, y - 25), (15, y), (30, y))
    for i, (x, lab) in enumerate(xs):
        red = hl == i
        f.box(x, y - 27, 105, 54, lab, size=13, fill='#fdecea' if red else '#eef3fb', stroke=RED if red else BL, wt='bold' if red else 'normal')
        if i: f.arrow([(xs[i - 1][0] + 105, y), (x, y)], c=TX, w=1.8)
    f.arrow([(685, y), (710, y)], c=TX, w=1.8)
    f.path([(712, y - 10), (722, y - 10), (735, y - 24), (735, y + 24), (722, y + 10), (712, y + 10)], c=TX, w=1.8, fill='#fff', close=True)
    f.box(160, y + 55, 105, 44, 'oscilátor', size=13)
    f.arrow([(212, y + 55), (212, y + 27)], c=TX, w=1.8)
    if bfo:
        f.box(440, y + 55, 105, 44, 'BFO', size=14, wt='bold', fill='#fdecea' if hl == 'bfo' else '#eef3fb', stroke=RED if hl == 'bfo' else BL)
        f.arrow([(492, y + 55), (492, y + 27)], c=RED if hl == 'bfo' else TX, w=1.8)


def d_nobfo():
    f = F(684)
    _superhet(f, 70, hl='bfo')
    f.t(380, 200, 'bez BFO: SSB je nesrozumitelné „kvákání“, telegrafie (CW) je neslyšitelná', size=14, c=RED, w='bold')
    FC, F1, F2 = 40, 2, 5
    scope(f, 240, [
        ('mf SSB signál (dva tóny) – nosná chybí', '455 kHz', lambda t: 0.5 * (cs((FC + F1) * t) + cs((FC + F2) * t))),
        ('obálkový detektor bez BFO: zkreslený tvar', '„kvákání“', lambda t: 1.6 * abs(math.cos(math.pi * (F2 - F1) * t)) - 0.8),
        ('produktový detektor s BFO: původní tóny', '0,7 + 1,75 kHz', lambda t: 0.4 * (cs(F1 * t) + cs(F2 * t))),
        ('CW bez BFO: jen stálé napětí – tón neslyšíme', '0 Hz', lambda t: 0.5),
    ], env=[(0, lambda t: abs(math.cos(math.pi * (F2 - F1) * t)))], note=NOTE)
    return f, ('SSB a CW nemají nosnou (u CW je jen nemodulovaná nosná, kterou obálkový detektor neslyší). Detektor '
               'potřebuje místní nosnou z BFO – superhet bez BFO umí přijímat jen AM (a s jiným detektorem FM).')


def d_lo():
    f = F(200)
    X = freqaxis(f, 40, 700, 150, 3.4, 4.5, [(3.5, '3,5'), (3.75, '3,750'), (4.0, '4,0'), (4.205, '4,205')])
    bar(f, X(3.75), 150, 80, c=BL, lab='přijímaný f s')
    bar(f, X(4.205), 150, 80, c=RED, lab='oscilátor f o')
    f.arrow([(X(3.75), 105), (X(4.205), 105)], c=GRN, w=1.8, both=True); f.t((X(3.75) + X(4.205)) / 2, 98, '455 kHz', c=GRN, w='bold')
    f.t(370, 30, 'f o = f s + f mf = 3,750 + 0,455 = 4,205 MHz', size=17, w='bold')
    return f, ('Oscilátor superhetu kmitá o mezifrekvenci výš (obvyklé u KV přijímačů) – rozdíl obou kmitočtů je '
               'právě mezifrekvenční kmitočet 455 kHz.')


def d_mixer():
    f = F(674)
    f.t(60, 75, 'f s', size=16, w='bold', c=BL); f.t(60, 98, '14,255 MHz', size=13, c=BL)
    f.arrow([(110, 85), (318, 85)], c=BL, w=2)
    f.mixer(340, 85, 24); f.t(340, 40, 'směšovač', size=15, w='bold')
    f.box(285, 150, 110, 46, 'oscilátor f o\n13,8 MHz', size=13)
    f.arrow([(340, 150), (340, 110)], c=TX, w=2)
    f.arrow([(364, 85), (440, 85)], c=TX, w=2)
    f.box(440, 60, 110, 50, 'mf filtr\n455 kHz', size=13, fill='#eef3fb')
    f.arrow([(550, 85), (600, 85)], c=TX, w=2)
    f.t(605, 70, 'rozdíl |f s − f o|', size=13, anchor='start', c=GRN)
    f.t(605, 92, '= 455 kHz (mf)', size=14, anchor='start', c=GRN, w='bold')
    f.t(605, 130, 'f s + f o = 28,055 MHz', size=13, anchor='start', c=RED)
    f.t(605, 150, '(filtr ho odstraní)', size=12, anchor='start', c=RED)
    scope(f, 230, [
        ('přijímaný signál f s', '14,255 MHz', lambda t: cs(36 * t)),
        ('místní oscilátor f o', '13,800 MHz', lambda t: cs(30 * t)),
        ('výstup směšovače = CH1 × CH2', 'rozdíl + součet', lambda t: cs(36 * t) * cs(30 * t)),
        ('za mf filtrem: jen rozdílový kmitočet', '0,455 MHz', lambda t: 0.8 * cs(6 * t)),
    ], env=[(2, lambda t: abs(cs(6 * t)))], note=NOTE)
    return f, ('Směšovač je nelineární obvod: z přijímaného signálu a signálu oscilátoru vytvoří součtový i rozdílový '
               'kmitočet. Mezifrekvenční filtr propustí jen žádaný rozdíl – mezifrekvenci.')


def d_sum():
    f = F(586)
    X = freqaxis(f, 40, 700, 170, 0, 30, [(0, '0'), (5, '5'), (10, '10'), (15, '15'), (20, '20'), (25, '25')])
    bar(f, X(0.455), 170, 70, c=GRN, lab='mf 0,455', anchor='start')
    bar(f, X(13.8), 170, 100, c=TX, lab='VFO 13,8', anchor='end')
    bar(f, X(14.255), 170, 70, c=BL, lab='signál 14,255', anchor='start')
    bar(f, X(28.055), 170, 70, c=RED, lab='součet 28,055 – nežádoucí', anchor='end')
    f.t(370, 30, '14,255 + 13,8 = 28,055 MHz    |    14,255 − 13,8 = 0,455 MHz', size=15, w='bold')
    scope(f, 230, [
        ('výstup směšovače (14,255 × 13,8 MHz)', 'rozdíl + součet', lambda t: cs(36 * t) * cs(30 * t)),
        ('za dolní propustí: rozdíl = mf', '0,455 MHz', lambda t: 0.8 * cs(6 * t)),
        ('za horní propustí: součet – nežádoucí', '28,055 MHz', lambda t: 0.8 * cs(66 * t)),
    ], note=NOTE)
    return f, ('Směšováním vzniká vždy součet i rozdíl obou kmitočtů. Pro mezifrekvenci 455 kHz je žádaný rozdíl, '
               'součet 28,055 MHz je nežádoucí produkt.')


def d_smeter():
    f = F(270)
    cx, cy, R = 230, 220, 170
    marks = [('1', 0), ('3', 2), ('5', 4), ('7', 6), ('9', 8), ('+20', 10), ('+40', 12), ('+60', 14)]
    ang = lambda k: math.radians(150 - k * 120 / 14)
    pts = [(cx + R * math.cos(ang(k / 10)), cy - R * math.sin(ang(k / 10))) for k in range(0, 81)]
    f.path(pts, c=TX, w=2.2)
    pts = [(cx + R * math.cos(ang(k / 10)), cy - R * math.sin(ang(k / 10))) for k in range(80, 141)]
    f.path(pts, c=RED, w=4)
    for lab, k in marks:
        a = ang(k)
        f.l(cx + R * math.cos(a), cy - R * math.sin(a), cx + (R - 16) * math.cos(a), cy - (R - 16) * math.sin(a), w=2)
        f.t(cx + (R + 20) * math.cos(a), cy - (R + 20) * math.sin(a) + 5, lab, size=14, c=RED if '+' in lab else TX, w='bold')
    a = ang(8)
    f.arrow([(cx, cy), (cx + (R - 25) * math.cos(a), cy - (R - 25) * math.sin(a))], c=BL, w=2.5)
    f.circle(cx, cy, 6, fill=TX)
    f.t(cx, cy + 35, 'S', size=18, w='bold')
    f.t(480, 70, '1 stupeň S = 6 dB (2× napětí)', size=15, anchor='start')
    f.t(480, 105, 'S9 ≈ 50 µV na 50 Ω (KV)', size=15, anchor='start')
    f.t(480, 140, 'nad S9 v dB: S9 + 20 dB…', size=15, anchor='start', c=RED)
    f.t(480, 185, 'hodnota se hlásí v reportu RST\n(např. 59 = srozumitelnost 5, síla 9)', size=13, anchor='start', c=GR)
    return f, ('S-metr ukazuje sílu přijímaného signálu ve stupních S1 až S9, nad S9 v decibelech. Údaje různých '
               'přijímačů se často liší – jde spíš o orientační, srovnávací měřidlo.')


def d_image():
    f = F(694)
    X = freqaxis(f, 40, 700, 190, 3.4, 5.0, [(3.75, '3,750'), (4.205, '4,205'), (4.66, '4,660')])
    f.plot(lambda v: 60 * reson(v, 3.75, 22), 40, 190, 660, 1, 3.4, 5.0, 0, 1, c=GRN, wd=2, dash='6,4', clip=False)
    bar(f, X(3.75), 190, 100, c=BL, lab='žádaný f s')
    bar(f, X(4.205), 190, 120, c=TX, lab='oscilátor f o')
    bar(f, X(4.66), 190, 60, c=RED, lab='zrcadlový f z')
    f.arrow([(X(3.75), 150), (X(4.205), 150)], c=BL, w=1.5, both=True); f.t((X(3.75) + X(4.205)) / 2, 143, '455 kHz', size=12, c=BL)
    f.arrow([(X(4.205), 150), (X(4.66), 150)], c=RED, w=1.5, both=True); f.t((X(4.205) + X(4.66)) / 2, 143, '455 kHz', size=12, c=RED)
    f.t(X(3.52), 110, 'vstupní\nfiltr', size=12, c=GRN)
    f.t(370, 25, 'f z = f s + 2 · f mf – oba dávají po směšování stejnou mezifrekvenci', size=14, w='bold')
    scope(f, 250, [
        ('žádaný signál', '3,750 MHz', lambda t: cs(34 * t)),
        ('zrcadlový signál (jiná stanice)', '4,660 MHz', lambda t: 0.7 * cs(46 * t)),
        ('mf ze žádaného signálu', '455 kHz', lambda t: 0.8 * cs(6 * t)),
        ('mf ze zrcadlového – stejný kmitočet, nedá se odfiltrovat!', '455 kHz', lambda t: 0.56 * cs(6 * t + 0.3)),
    ], note=NOTE)
    return f, ('Zrcadlový kmitočet leží „na druhé straně“ oscilátoru, ve stejné vzdálenosti jako žádaný signál. '
               'Směšovač z něj vyrobí stejnou mezifrekvenci, proto se musí potlačit selektivním vstupním obvodem '
               '(nebo volbou vysoké mezifrekvence).')


def _snr(f, x, y, s, n, lab):
    f.rect(x, y - s, 40, s, fill=BL, stroke=BL, op=0.8)
    f.rect(x + 50, y - n, 40, n, fill=RED, stroke=RED, op=0.8)
    f.t(x + 20, y + 18, 'S', size=13, c=BL); f.t(x + 70, y + 18, 'N', size=13, c=RED)
    f.t(x + 45, y + 40, lab, size=13)


def d_nf():
    f = F(518)
    _snr(f, 40, 170, 120, 20, 'vstup: S/N = 6')
    f.arrow([(160, 110), (250, 110)], c=TX, w=2)
    f.box(250, 70, 160, 80, 'přijímač\n(přidává vlastní šum)', size=13)
    f.arrow([(410, 110), (480, 110)], c=TX, w=2)
    _snr(f, 490, 170, 120, 40, 'výstup: S/N = 3')
    f.t(680, 70, 'F = 6 / 3 = 2', size=16, w='bold', c=RED)
    f.t(680, 100, 'NF = 10·log 2', size=14)
    f.t(680, 122, '= 3 dB', size=14, w='bold')
    f.t(370, 30, 'F = (S/N) vstup / (S/N) výstup', size=16, w='bold', c=BL)
    scope(f, 250, [
        ('vstup přijímače: signál + šum', 'S/N = 6', lambda t: 0.75 * sn(4 * t) + 0.12 * noise(t)),
        ('výstup: stejný signál, šumu přibylo', 'S/N = 3', lambda t: 0.75 * sn(4 * t) + 0.25 * noise(t)),
    ], note='Šum je znázorněn schematicky; zesílení přijímače je pro srovnání vyrovnáno.')
    return f, ('Šumové číslo říká, kolikrát přijímač zhorší odstup signálu od šumu. Ideální bezšumový přijímač má F = 1 '
               '(0 dB). Na VKV a UKV rozhoduje hlavně šum prvního stupně (předzesilovače).')


def d_sens():
    f = F(270)
    x0, y0, w, h = 90, 220, 600, 180
    f.axes(x0, y0, w, h, 'U vstup [µV]', '(S+N)/N [dB]')
    Xv = lambda u: x0 + (math.log10(u) + 2) / 3 * (w - 30)
    Yv = lambda d: y0 - d / 45 * (h - 20)
    pts = [(Xv(10 ** (-2 + 3 * i / 200)), Yv(10 * math.log10(1 + (10 ** (-2 + 3 * i / 200) / 0.07) ** 2))) for i in range(201)]
    f.path([(x, max(y, y0 - h + 20)) for x, y in pts], c=BL, w=2.4)
    u10 = 0.07 * math.sqrt(9)
    f.l(x0, Yv(10), Xv(u10), Yv(10), RED, 1.4, '5,4'); f.l(Xv(u10), Yv(10), Xv(u10), y0, RED, 1.4, '5,4')
    f.t(x0 - 6, Yv(10) + 5, '10 dB', anchor='end', size=13, c=RED, w='bold')
    f.t(Xv(u10), y0 + 20, '0,2 µV', size=13, c=RED, w='bold')
    for u, lab in ((0.01, '0,01'), (0.1, '0,1'), (1, '1'), (10, '10')):
        f.l(Xv(u), y0 - 4, Xv(u), y0 + 4, w=1.2)
        if u in (0.01, 1): f.t(Xv(u), y0 + 20, lab, size=12)
    f.t(x0 + 20, y0 - h + 30, 'citlivost = nejmenší vstupní napětí,\npři kterém je odstup 10 dB', size=13, anchor='start')
    return f, ('Citlivost přijímače je vstupní napětí (typicky zlomky µV), při kterém je na výstupu dosaženo '
               'požadovaného odstupu signálu od šumu – zpravidla 10 dB. Čím menší napětí, tím citlivější přijímač.')


def d_imd():
    f = F(606)
    X = freqaxis(f, 40, 700, 190, 7.02, 7.09, [(7.03, '7,030'), (7.04, '7,040'), (7.05, '7,050'), (7.06, '7,060'), (7.07, '7,070'), (7.08, '7,080')])
    bar(f, X(7.05), 190, 120, c=BL, lab='f₁'); bar(f, X(7.06), 190, 120, c=BL, lab='f₂')
    bar(f, X(7.04), 190, 45, c=RED, lab='2f₁ − f₂'); bar(f, X(7.07), 190, 45, c=RED, lab='2f₂ − f₁')
    bar(f, X(7.03), 190, 20, c=RED, lab='3f₁ − 2f₂', size=11); bar(f, X(7.08), 190, 20, c=RED, lab='3f₂ − 2f₁', size=11)
    f.t(370, 25, 'dva silné signály → nové „falešné“ signály na kmitočtech, kde nikdo nevysílá', size=14, w='bold')
    two = lambda t: 0.45 * (cs(40 * t) + cs(44 * t))
    scope(f, 250, [
        ('vstup: dva silné signály f₁ + f₂', '7,050 + 7,060 MHz', two),
        ('lineární zesilovač: tvar zachován', 'jen f₁ a f₂', lambda t: two(t)),
        ('přebuzený (nelineární) stupeň: ořezané špičky', '+ 2f₁−f₂, 2f₂−f₁…', lambda t: clip(1.6 * two(t), 0.75) / 0.75),
    ], env=[(0, lambda t: 0.9 * abs(math.cos(math.pi * 4 * t)))], note=NOTE)
    return f, ('Intermodulace: silné signály se v nelineárním stupni (přebuzený vf zesilovač, směšovač) smísí '
               'navzájem i se svými harmonickými. Nejnepříjemnější jsou produkty 3. řádu 2f₁ − f₂ a 2f₂ − f₁, které '
               'padnou do stejného pásma.')


def d_sel():
    f = F(240)
    X = freqaxis(f, 40, 700, 190, -8, 8, [(-6, '−6'), (-3, '−3'), (0, '0'), (3, '3'), (6, '6')], unit='kHz')
    def filt(v):
        return 1 / (1 + (abs(v) / 1.35) ** 14)
    f.plot(lambda v: filt(v), 40, 190, 660, 140, -8, 8, 0, 1, c=GRN, wd=2.2)
    f.path([(X(-1.35), 190)] + [(X(v / 20), 190 - 140 * filt(v / 20)) for v in range(-27, 28)] + [(X(1.35), 190)], c=GRN, fill=GRN, op=0.12, w=0.1)
    bar(f, X(0), 190, 100, c=BL, lab='žádaný')
    bar(f, X(-3.2), 190, 130, c=RED, lab='silný soused')
    bar(f, X(4), 190, 80, c=RED, lab='soused')
    f.t(X(0), 40, 'propustné pásmo filtru', size=13, c=GRN)
    return f, ('Selektivita = schopnost oddělit žádaný signál od signálů na sousedních kmitočtech. Zajišťují ji hlavně '
               'mezifrekvenční filtry: čím strmější boky propustné křivky, tím lepší selektivita.')


def d_squelch():
    f = F(300)
    x0, w = 120, 600
    f.t(20, 50, 'přijímaný\nsignál', size=13, anchor='start')
    f.arrow([(x0, 120), (x0 + w, 120)], c=TX, w=1.4)
    import random
    rnd = random.Random(3)
    pts = []
    for i in range(301):
        u = i / 300
        lvl = 60 if 0.35 < u < 0.7 else 18
        pts.append((x0 + u * (w - 20), 120 - lvl - rnd.uniform(-6, 6)))
    f.path(pts, c=BL, w=1.6)
    f.l(x0, 85, x0 + w - 20, 85, RED, 1.6, '7,5'); f.t(x0 + w - 15, 82, 'práh SQL', size=13, c=RED, anchor='start')
    f.t(20, 190, 'reproduktor', size=13, anchor='start')
    f.arrow([(x0, 220), (x0 + w, 220)], c=TX, w=1.4)
    a, b = x0 + 0.35 * (w - 20), x0 + 0.7 * (w - 20)
    f.l(x0, 220, a, 220, GR, 3); f.l(b, 220, x0 + w - 20, 220, GR, 3)
    f.sine(a, 220, b - a, 22, 14, c=GRN)
    f.t((x0 + a) / 2, 272, 'ticho (jen šum → zavřeno)', size=13, c=GR)
    f.t((a + b) / 2, 272, 'signál nad prahem → otevřeno', size=13, c=GRN)
    f.t((b + x0 + w) / 2, 272, 'ticho', size=13, c=GR)
    f.t(x0 + w - 10, 245, 't', size=14)
    return f, ('Squelch (umlčovač šumu) uzavře nf výstup, dokud signál nepřekročí nastavený práh. Typické u FM '
               'provozu přes převáděče – bez něj by z reproduktoru neustále šuměl šum.')


def d_ifamp():
    f = F(230)
    for k, (fr, y) in enumerate((('3,7 MHz', 50), ('7,1 MHz', 100), ('14,2 MHz', 150))):
        f.t(70, y + 5, fr, size=13, c=BL, w='bold')
        f.arrow([(110, y), (205, 100)], c=BL, w=1.4)
    f.mixer(230, 100, 24)
    f.box(180, 160, 100, 44, 'laditelný\noscilátor', size=12)
    f.arrow([(230, 160), (230, 124)], c=TX, w=1.8)
    f.arrow([(254, 100), (320, 100)], c=TX, w=2)
    f.t(287, 88, '455 kHz', size=12, c=RED)
    for i in range(3):
        x = 320 + i * 110
        f.box(x, 72, 90, 56, f'mf {i + 1}' if i else 'mf filtr', size=13, fill='#fdecea' if i == 0 else '#eef3fb', stroke=RED if i == 0 else BL)
        f.arrow([(x + 90, 100), (x + 110, 100)], c=TX, w=1.8)
    f.t(650, 105, 'detektor', size=13, anchor='start')
    f.t(470, 170, 'vždy stejný pevný kmitočet → filtry a zesílení\nse nastaví jednou provždy, není třeba je přelaďovat', size=13, c=GR)
    return f, ('Mezifrekvenční zesilovač zesiluje už jen signál převedený na pevný mezifrekvenční kmitočet – ať '
               'posloucháme kterékoli pásmo. Proto může mít velký zisk a kvalitní (krystalové) filtry.')


def d_sdr():
    f = F(285)
    f.t(20, 40, 'klasický:', size=14, w='bold', anchor='start')
    xs = ['vf', 'směšovač', 'mf filtr', 'detektor', 'nf']
    for i, lab in enumerate(xs):
        x = 120 + i * 120
        f.box(x, 20, 100, 40, lab, size=13)
        if i: f.arrow([(x - 20, 40), (x, 40)], c=TX, w=1.6)
    f.t(380, 85, 'analogové obvody (cívky, filtry, směšovače)', size=12, c=GR)
    f.t(20, 150, 'SDR:', size=14, w='bold', anchor='start')
    f.box(120, 125, 100, 50, 'vf / filtr', size=13)
    f.arrow([(220, 150), (250, 150)], c=TX, w=1.6)
    f.box(250, 125, 110, 50, 'A/D\npřevodník', size=13, fill='#fdecea', stroke=RED, wt='bold')
    f.arrow([(360, 150), (390, 150)], c=TX, w=1.6)
    f.box(390, 115, 230, 70, 'počítač / DSP (FPGA)\nfiltry, demodulace,\nvodopád – software', size=13, fill='#eaf5ea', stroke=GRN)
    f.arrow([(620, 150), (650, 150)], c=TX, w=1.6)
    f.box(650, 125, 80, 50, 'nf / D/A', size=13)
    f.path([(x, 230 - 18 * math.sin(x / 9) - 6 * math.sin(x / 3.1)) for x in range(130, 330)], c=BL, w=1.6)
    f.t(230, 275, 'analogový signál', size=12, c=BL)
    for i in range(20):
        x = 400 + i * 10
        y = 230 - 18 * math.sin(x / 9) - 6 * math.sin(x / 3.1)
        f.l(x, 230, x, y, GRN, 3)
    f.t(500, 275, 'čísla (vzorky) – zpracuje program', size=12, c=GRN)
    return f, ('SDR (Software Defined Radio): signál se co nejdříve převede A/D převodníkem na čísla a filtrování, '
               'demodulaci i zobrazení spektra dělá software. Funkce přijímače lze měnit pouhou změnou programu.')


# ================================================================ e) Rádiové vysílače
def e_stab():
    f = F(250)
    x0, y0, w, h = 80, 210, 620, 170
    f.axes(x0, y0, w, h, 'čas od zapnutí', 'kmitočet')
    ym = y0 - h / 2
    f.l(x0, ym, x0 + w - 20, ym, GR, 1, '5,4'); f.t(x0 - 6, ym + 5, 'f nast.', anchor='end', size=13)
    f.plot(lambda t: 0.5 + 0.004 * math.sin(t * 9), x0, y0, w - 20, h, 0, 1, 0, 1, c=GRN)
    f.plot(lambda t: 0.5 + 0.38 * (1 - math.exp(-t * 4)) + 0.03 * math.sin(t * 25), x0, y0, w - 20, h, 0, 1, 0, 1, c=RED)
    f.t(x0 + w - 30, ym + 25, 'stabilní (krystal, PLL, TCXO)', size=13, c=GRN, anchor='end')
    f.t(x0 + w - 30, y0 - h + 12, 'nestabilní – „ujíždí“ (teplota, napětí)', size=13, c=RED, anchor='end')
    return f, ('Oscilátor určuje kmitočet vysílače. Když „ujíždí“, protistanice nás ztrácí, signál může vyjet z pásma '
               'a ruší ostatní. Proto se používají krystaly, PLL syntezátory a teplotně kompenzované oscilátory.')


def e_am_ssb():
    f = F(250)
    x0, y = 40, 100
    f.t(170, 28, 'AM signál v čase', size=14, w='bold')
    f.l(x0, y, x0 + 260, y, GR, 1)
    env = lambda u: 1 + 0.7 * math.sin(u / 9)
    f.path([(x0 + i, y - 50 / 1.7 * env(i) * math.sin(i * 1.3)) for i in range(261)], c=BL, w=1.3)
    f.path([(x0 + i, y - 50 / 1.7 * env(i)) for i in range(261)], c=RED, w=1.6, dash='5,4')
    f.t(170, 175, 'obálka nese hovor', size=12, c=RED)
    X = freqaxis(f, 380, 700, 200, -5, 5, [(0, 'f n')], unit='')
    f.t(540, 28, 'spektrum AM', size=14, w='bold')
    bar(f, X(0), 200, 130, c=TX, lab='nosná')
    for a, b, lab, c in ((-3.5, -0.4, 'LSB', BL), (0.4, 3.5, 'USB', BL)):
        f.path([(X(a), 200), (X(a), 140), (X(b), 140), (X(b), 200)], c=c, fill=BLF, op=0.9, w=1.5)
        f.t((X(a) + X(b)) / 2, 175, lab, size=13, c=BL, w='bold')
    f.t(540, 240, 'SSB = AM bez nosné a bez jednoho pásma', size=13, c=RED, w='bold')
    return f, ('SSB vychází z amplitudové modulace: AM má nosnou a dvě zrcadlová postranní pásma, která nesou stejnou '
               'informaci. SSB z nich ponechá jediné – proto je SSB druhem amplitudové modulace.')


def e_ssb_steps():
    f = F(684)
    titles = ['AM', 'DSB (potlačená nosná)', 'SSB (USB)']
    for k in range(3):
        x0 = 25 + k * 250
        X = lambda v, x0=x0: x0 + 105 + v * 28
        f.arrow([(x0, 180), (x0 + 215, 180)], c=TX, w=1.4)
        f.t(x0 + 105, 30, titles[k], size=14, w='bold', c=RED if k == 2 else TX)
        if k == 0:
            bar(f, X(0), 180, 110, c=TX, lab='nosná', size=12)
        else:
            f.l(X(0), 180, X(0), 95, GR, 1.4, '4,3'); f.l(X(0) - 10, 105, X(0) + 10, 85, RED, 2.5); f.l(X(0) - 10, 85, X(0) + 10, 105, RED, 2.5)
        for a, b, keep in ((-3.3, -0.4, k < 2), (0.4, 3.3, True)):
            f.path([(X(a), 180), (X(a), 125), (X(b), 125), (X(b), 180)], c=BL if keep else GR, fill=BLF if keep else '#ffffff',
                   op=0.9, w=1.5, dash=None if keep else '4,3')
        f.t(X(-1.85), 160, 'LSB', size=12, c=BL if k < 2 else GR); f.t(X(1.85), 160, 'USB', size=12, c=BL)
        if k < 2: f.arrow([(x0 + 218, 120), (x0 + 245, 120)], c=RED, w=2)
    f.t(380, 220, 'celý výkon vysílače jde do jediného postranního pásma, šířka pásma je poloviční', size=13, c=GR)
    scope(f, 240, [
        ('nf modulační tón', '1 kHz', lambda t: cs(3 * t)),
        ('AM: nosná, obálka kopíruje nf', 'nosná + 2 pásma', lambda t: (1 + 0.7 * cs(3 * t)) * cs(40 * t) / 1.7),
        ('DSB: bez nosné – obálka |nf|, fáze se převrací', '2 postranní pásma', lambda t: cs(3 * t) * cs(40 * t)),
        ('SSB (USB): stálá amplituda, kmitočet f n + 1 kHz', '1 postranní pásmo', lambda t: 0.85 * cs(43 * t)),
    ], env=[(1, lambda t: (1 + 0.7 * cs(3 * t)) / 1.7), (2, lambda t: abs(cs(3 * t)))], note=NOTE)
    return f, ('Odvození SSB: z AM se nejprve potlačí nosná (balanční modulátor → DSB) a pak se odfiltruje jedno '
               'postranní pásmo. Na KV pod 10 MHz se běžně používá LSB, nad 10 MHz USB.')


def e_dev():
    f = F(360)
    scope(f, 6, [
        ('nf modulace (hovor)', '', lambda t: sn(1.5 * t)),
        ('FM – malý zdvih: kmitočet se skoro nemění', 'slabá modulace', lambda t: math.cos(2 * math.pi * 30 * t - 2 * math.cos(2 * math.pi * 1.5 * t))),
        ('FM – správný zdvih: zřetelně „dýchá“', 'správně', lambda t: math.cos(2 * math.pi * 30 * t - 10.5 * math.cos(2 * math.pi * 1.5 * t))),
    ], note='Amplituda (a tedy výkon) je v obou případech stejná – liší se jen rozkmit kmitočtu (zdvih).')
    return f, ('U FM je informace v kolísání kmitočtu (zdvihu, deviaci); amplituda a tedy výkon se nemění. Malý zdvih = '
               'silný, ale tichý signál – modulace je slabá (málo hlasitý mikrofon, nízko nastavený zisk).')


def e_hum():
    f = F(626)
    x0, y = 40, 120
    f.t(180, 30, 'špatně vyhlazené napájení', size=14, w='bold')
    f.l(x0, y, x0 + 280, y, GR, 1)
    pts = []
    for i in range(281):
        u = (i / 70) % 1
        pts.append((x0 + i, y - 60 + (u * 30 if u < 0.8 else (1 - u) / 0.2 * 30)))
    f.path(pts, c=RED, w=2)
    f.l(x0, y - 60, x0 + 280, y - 60, GRN, 1.3, '5,4'); f.t(x0 + 285, y - 56, 'ideál', size=12, c=GRN, anchor='start')
    f.t(180, y + 22, 'zvlnění 100 Hz → brum v modulaci', size=12, c=RED)
    f.t(560, 30, 'poškozená mikrofonní šňůra', size=14, w='bold')
    f.path([(440, 90), (470, 90)], c=TX, w=3)
    f.rect(400, 75, 40, 30, fill='#dddddd', stroke=TX, rx=8); f.t(420, 125, 'mikrofon', size=12)
    f.path([(470, 90), (560, 90)], c=GR, w=9); f.path([(600, 90), (690, 90)], c=GR, w=9)
    f.path([(470, 90), (700, 90)], c=TX, w=2)
    f.t(580, 70, 'přerušené stínění', size=12, c=RED)
    f.rect(700, 76, 30, 28, fill='#bbbbbb', stroke=TX, rx=3)
    for k in range(3):
        f.path([(565 + k * 14, 140 - k * 4), (575 + k * 14, 110), (585 + k * 14, 140 - k * 4)], c=RED, w=1.2)
    f.t(580, 160, 'síťové rušení 50 Hz se indukuje do vodiče', size=12, c=RED)
    X = freqaxis(f, 160, 600, 235, -200, 200, [(-100, '−100'), (-50, '−50'), (0, 'f'), (50, '+50'), (100, '+100 Hz')], unit='', size=12)
    bar(f, X(0), 235, 50, c=BL)
    for d, hh in ((50, 18), (100, 25), (-50, 18), (-100, 25)):
        bar(f, X(d), 235, hh, c=RED, w=2.5)
    f.t(660, 222, 'brum ve spektru', size=12, c=RED, anchor='start')
    saw = lambda t: 1 - 2 * ((t * 4) % 1) if (t * 4) % 1 < 0.85 else -0.7 + 2 * (((t * 4) % 1) - 0.85) / 0.15 * 0.85
    scope(f, 270, [
        ('napájecí napětí – zvlnění 100 Hz', '100 Hz', lambda t: 0.5 * saw(t)),
        ('nf signál z mikrofonu + brum', '1 kHz + 100 Hz', lambda t: 0.45 * sn(40 * t) + 0.4 * sn(4 * t)),
        ('vysílaný signál: obálka „pulzuje“ brumem', 'vf', lambda t: (0.55 + 0.3 * sn(4 * t)) * cs(90 * t)),
    ], env=[(2, lambda t: 0.55 + 0.3 * sn(4 * t))], note=NOTE)
    return f, ('Brum (50 Hz ze sítě, 100 Hz po dvoucestném usměrnění) se do signálu dostane nejčastěji ze špatně '
               'vyhlazeného napájení nebo přes poškozené stínění mikrofonního kabelu.')


def e_pep():
    f = F(265)
    x0, y0, w, h = 80, 210, 620, 170
    f.axes(x0, y0, w, h, 'čas', 'okamžitý výkon [W]')
    import random
    rnd = random.Random(7)
    pts = []
    for i in range(301):
        u = i / 300
        e = abs(math.sin(u * 23) * math.sin(u * 7.3 + 1)) ** 1.6 * (0.6 + 0.4 * math.sin(u * 3)) + 0.03 * rnd.random()
        pts.append((x0 + u * (w - 20), y0 - e * (h - 30)))
    f.path([(x0, y0)] + pts + [(x0 + w - 20, y0)], c=BL, fill=BLF, op=0.8, w=1.6)
    ymax = min(p[1] for p in pts)
    f.l(x0, ymax, x0 + w - 20, ymax, RED, 1.8, '7,5'); f.t(x0 - 6, ymax + 5, '100', anchor='end', size=13, c=RED, w='bold')
    f.t(x0 + w - 20, ymax - 8, 'PEP – výkon ve špičce obálky = 100 W PEP', anchor='end', size=13, c=RED, w='bold')
    ya = y0 - 0.22 * (h - 30)
    f.l(x0, ya, x0 + w - 20, ya, GRN, 1.6, '4,4'); f.t(x0 + 10, y0 + 24, '- - - střední výkon (hovor) je mnohem menší', anchor='start', size=12, c=GRN)
    return f, ('U SSB se výkon mění podle hlasitosti hovoru. Výkon PEP (Peak Envelope Power) je střední výkon během '
               'jedné periody vf signálu v okamžiku nejvyšší špičky modulační obálky. Povolené výkony ve vyhlášce se '
               'udávají v PEP.')


def e_tube():
    f = F(260)
    cx, cy = 110, 130
    f.circle(cx, cy, 52, fill='#fafafa')
    f.l(cx - 25, cy - 30, cx + 25, cy - 30, w=3); f.t(cx + 30, cy - 36, 'anoda', size=11, anchor='start')
    for k in range(6): f.l(cx - 25 + k * 10, cy, cx - 20 + k * 10, cy, w=2)
    f.path([(cx - 25, cy + 28), (cx - 20, cy + 33), (cx + 20, cy + 33), (cx + 25, cy + 28)], c=TX, w=2)
    f.t(cx, 205, 'elektronka', size=13)
    f.wire((cx, cy - 30), (cx, 40), (230, 40))
    f.t(cx + 6, 32, '', size=1)
    part(f, 'C', (230, 40), (230, 40.1)) if False else None
    f.wire((230, 40), (230, 70)); f.dot(230, 70)
    f.wire((200, 70), (540, 70))
    part(f, 'L', (300, 70), (460, 70), 'L')
    f.wire((200, 70), (300, 70)); f.wire((460, 70), (560, 70))
    for x, lab in ((250, 'C ladění'), (520, 'C vazba')):
        f.dot(x, 70); part(f, 'Cv', (x, 70), (x, 190), lab, c=RED, lc=RED); gnd(f, x, 190)
    f.wire((560, 70), (640, 70)); antenna(f, 640, 70, 45)
    f.t(380, 235, 'π článek – laděný výstupní obvod (přelaďuje se ručně: PLATE / LOAD)', size=13, c=RED, w='bold')
    return f, ('Elektronkový koncový stupeň má velkou výstupní impedanci (kΩ). Laděný obvod – typicky π článek s '
               'otočnými kondenzátory – ji přizpůsobí na 50 Ω a zároveň potlačí harmonické. Při změně kmitočtu se musí '
               'doladit.')


def e_trans():
    f = F(260)
    f.box(30, 100, 120, 60, 'tranzistorový\nPA (širokopásmový)', size=12)
    f.arrow([(150, 130), (200, 130)], c=TX, w=1.8)
    bands = ['160 m (1,8 MHz)', '80 m (3,5 MHz)', '40/30 m (7/10 MHz)', '20/17 m (14/18 MHz)', '15/12/10 m (21/24/28 MHz)']
    for i, b in enumerate(bands):
        y = 30 + i * 46
        f.wire((200, 130), (230, y + 18)) if i == 1 else None
        f.box(270, y, 230, 36, f'propust {b}', size=12, fill='#fdecea' if i == 2 else '#eef3fb', stroke=RED if i == 2 else BL)
        f.l(250, y + 18, 270, y + 18, w=1.4); f.l(500, y + 18, 520, y + 18, w=1.4)
        f.dot(250, y + 18); f.dot(520, y + 18)
    f.l(200, 130, 248, 30 + 2 * 46 + 18, RED, 2.4); f.l(522, 30 + 2 * 46 + 18, 570, 130, RED, 2.4)
    f.arrow([(570, 130), (630, 130)], c=TX, w=1.8); antenna(f, 640, 130, 45); f.wire((630, 130), (640, 130))
    f.t(560, 220, 'filtry se přepínají podle pásma\n(relé) – nic se neladí', size=13, anchor='start', c=GR)
    return f, ('Tranzistorový koncový stupeň je širokopásmový (výstup přes transformátor na 50 Ω). Harmonické '
               'kmitočty potlačuje sada pevných filtrů (pásmových nebo dolních propustí), které se přepínají '
               'automaticky podle zvoleného pásma.')


def e_ssbfilter():
    f = F(686)
    f.box(20, 50, 90, 46, 'mikrofon\nnf', size=13)
    f.arrow([(110, 73), (150, 73)], c=TX, w=1.8)
    f.box(150, 45, 130, 56, 'balanční\nmodulátor', size=13)
    f.box(150, 130, 130, 44, 'nosná 9 MHz', size=13)
    f.arrow([(215, 130), (215, 101)], c=TX, w=1.8)
    f.arrow([(280, 73), (340, 73)], c=TX, w=1.8); f.t(310, 62, 'DSB', size=12, c=BL)
    f.box(340, 45, 150, 56, 'krystalový filtr\n(pásmová propust)', size=13, fill='#fdecea', stroke=RED, wt='bold')
    f.arrow([(490, 73), (550, 73)], c=TX, w=1.8); f.t(520, 62, 'SSB', size=12, c=BL)
    f.box(550, 45, 170, 56, 'směšování na\nkmitočet pásma, PA', size=13)
    X = freqaxis(f, 120, 640, 290, 8.994, 9.006, [(9.0, '9,000 MHz (potlačená nosná)')])
    f.l(X(9.0), 290, X(9.0), 225, GR, 1.4, '4,3')
    for a, b, keep in ((8.9965, 8.9997, False), (9.0003, 9.0035, True)):
        f.path([(X(a), 290), (X(a), 240), (X(b), 240), (X(b), 290)], c=BL if keep else GR, fill=BLF if keep else '#eeeeee', op=0.9, w=1.5)
    f.t(X(8.9981), 270, 'LSB – potlačí', size=12, c=GR); f.t(X(9.0019), 270, 'USB – projde', size=12, c=BL, w='bold')
    pts = [(X(9.0003 + 0.0032 * i / 40 + (-0.0002 if i == 0 else 0)), 205) for i in range(41)]
    f.path([(X(8.99995), 290), (X(9.0002), 205), (X(9.0036), 205), (X(9.0039), 290)], c=RED, w=2.2, dash='6,4')
    f.t(X(9.0045), 200, 'propustná křivka filtru', size=12, c=RED, anchor='start')
    scope(f, 330, [
        ('nf modulační tón (mikrofon)', '1 kHz', lambda t: cs(3 * t)),
        ('za balančním modulátorem: DSB', '9 MHz ± 1 kHz', lambda t: cs(3 * t) * cs(40 * t)),
        ('za krystalovým filtrem: SSB (USB)', '9,001 MHz', lambda t: 0.85 * cs(43 * t)),
    ], env=[(1, lambda t: abs(cs(3 * t)))], note=NOTE)
    return f, ('Filtrová metoda SSB: balanční modulátor potlačí nosnou a vytvoří DSB. Strmý krystalový pásmový filtr '
               'propustí jen žádané postranní pásmo. Druhé pásmo se volí posunem kmitočtu nosné vůči filtru.')


def e_match():
    f = F(270)
    acsrc(f, 60, 130, lab='U')
    f.wire((60, 110), (60, 60), (100, 60)); part(f, 'R', (100, 60), (220, 60), 'R i (vnitřní)', side=-1)
    f.wire((220, 60), (280, 60)); part(f, 'R', (280, 60), (280, 200), 'R z (zátěž)')
    f.wire((60, 150), (60, 200), (280, 200))
    f.rect(15, 20, 225, 205, stroke=GR, sw=1.2, dash='5,4'); f.t(130, 250, 'vysílač', size=13, c=GR)
    x0, y0, w, h = 400, 220, 320, 180
    f.axes(x0, y0, w, h, 'R z / R i', 'výkon v zátěži')
    f.plot(lambda r: 4 * r / (1 + r) ** 2, x0, y0, w - 20, h - 30, 0, 5, 0, 1.05)
    X = lambda r: x0 + r / 5 * (w - 20)
    f.l(X(1), y0, X(1), y0 - (h - 30) / 1.05, RED, 1.4, '4,4'); f.t(X(1), y0 + 20, '1', size=14, c=RED, w='bold')
    f.t(X(1) + 8, y0 - h + 22, 'maximum při R z = R i', size=13, c=RED, anchor='start', w='bold')
    for r in (2, 3, 4): f.t(X(r), y0 + 20, str(r), size=12)
    return f, ('Zdroj odevzdá do zátěže největší výkon, když se impedance zátěže rovná jeho vnitřní (výstupní) '
               'impedanci – výkonové přizpůsobení. U vysílače je to 50 Ω: anténa s napáječem má mít také 50 Ω.')


def e_noload():
    f = F(220)
    f.box(30, 70, 140, 70, 'koncový\nstupeň', size=14, wt='bold', fill='#fdecea', stroke=RED)
    f.l(170, 95, 560, 95, w=3); f.l(170, 115, 560, 115, w=3)
    f.circle(565, 105, 8, fill='#ffffff'); f.t(600, 110, 'nic nepřipojeno', size=13, anchor='start', c=RED, w='bold')
    f.arrow([(200, 65), (520, 65)], c=BL, w=2.5); f.t(360, 55, 'vyslaný výkon', size=13, c=BL)
    f.arrow([(520, 150), (200, 150)], c=RED, w=2.5); f.t(360, 172, 'odražený výkon – vrací se celý zpět', size=13, c=RED)
    f.t(30, 205, 'přehřátí, průraz tranzistoru (elektronky)', size=13, c=RED, w='bold', anchor='start')
    for k in range(3):
        f.path([(60 + k * 30, 60), (70 + k * 30, 45), (60 + k * 30, 30)], c=ORA, w=2)
    return f, ('Bez antény nebo zátěže se výkon nemá kam vyzářit, odrazí se na konci vedení a vrátí se do koncového '
               'stupně (PSV → ∞). Vzniká vysoké napětí a teplo, které mohou koncový stupeň zničit. Proto zkoušíme do '
               'umělé zátěže.')


# ================================================================ f) Antény a napájecí vedení
def f_swr():
    f = F(270)
    x0, y0, w, h = 90, 220, 600, 180
    f.axes(x0, y0, w, h, 'PSV', 'přenesený výkon [%]')
    sx = lambda s: x0 + (s - 1) / 5 * (w - 30)
    py = lambda p: y0 - (p - 40) / 60 * (h - 20)
    trans = lambda s: 100 * (1 - ((s - 1) / (s + 1)) ** 2)
    f.path([(sx(1 + 5 * i / 200), py(trans(1 + 5 * i / 200))) for i in range(201)], c=BL, w=2.5)
    for s in (1, 2, 3, 4, 5):
        f.t(sx(s), y0 + 20, f'1:{s}' if s > 1 else '1:1', size=12)
    for p in (50, 75, 100):
        f.t(x0 - 6, py(p) + 5, f'{p}', anchor='end', size=12)
    f.l(sx(3), y0, sx(3), py(75), RED, 1.5, '5,4'); f.l(x0, py(75), sx(3), py(75), RED, 1.5, '5,4')
    f.circle(sx(3), py(75), 5, fill=RED, stroke=RED)
    f.t(sx(3) + 12, py(75) - 10, 'PSV 1:3 → 75 % (odraz 25 %)', anchor='start', size=14, c=RED, w='bold')
    f.t(sx(4), 40, '|Γ| = (PSV − 1)/(PSV + 1) = 2/4 = 0,5\nodražený výkon = Γ² = 25 %', size=14, anchor='middle')
    return f, ('Z PSV se spočte činitel odrazu Γ; jeho druhá mocnina udává podíl odraženého výkonu. Pro PSV 3 je '
               'Γ = 0,5, odráží se 25 % a do antény přejde zhruba 75 % (bez započtení ztrát ve vedení).')


def f_dipole():
    f = F(260)
    y = 140
    f.l(60, y, 370, y, w=4); f.l(390, y, 700, y, w=4)
    f.circle(60, y, 5, fill=TX); f.circle(700, y, 5, fill=TX)
    f.wire((370, y), (375, y + 70)); f.wire((390, y), (385, y + 70)); f.t(380, y + 92, 'napáječ', size=13)
    f.path([(60 + i * 6.4, y - 70 * math.sin(math.pi * i / 100)) for i in range(101)], c=RED, w=1.8, dash='6,4')
    f.t(380, y - 78, 'proud: maximum uprostřed', size=12, c=RED)
    f.arrow([(60, y + 30), (370, y + 30)], c=BL, w=1.6, both=True); f.t(215, y + 50, 'rameno ≈ λ/4 ≈ 20 m', size=14, c=BL, w='bold')
    f.arrow([(390, y + 30), (700, y + 30)], c=BL, w=1.6, both=True); f.t(545, y + 50, '≈ 20 m', size=14, c=BL)
    f.t(380, 22, 'λ = 300 / f [MHz] = 300 / 3,5 ≈ 86 m;   λ/2 ≈ 43 m;   s činitelem zkrácení ≈ 0,95 → 2 × 20 m', size=14, w='bold')
    return f, ('Půlvlnný dipól má celkovou délku zhruba λ/2, každé rameno tedy asi λ/4. Pro 3,5 MHz vychází rameno '
               'přibližně 20 m (skutečná délka je o několik procent kratší než teoretická).')


def f_folded():
    f = F(645)
    x0, x1, gap0, gap1 = 90, 670, 368, 392
    L = x1 - x0
    U = lambda u: x0 + u * L
    env = lambda u: math.sin(math.pi * u)

    def envelope(y, A, sign, col):
        pts = [(U(i / 100), y - sign * A * env(i / 100)) for i in range(101)]
        f.path([(x0, y)] + pts + [(x1, y)], c=col, fill=col, op=0.12, w=1.6, dash='6,4')

    def arrows(y, A, col, skip_mid=False):
        for u in (0.12, 0.25, 0.38, 0.5, 0.62, 0.75, 0.88):
            if skip_mid and abs(u - 0.5) < 0.05: continue
            ln = 8 + 34 * env(u)
            f.arrow([(U(u) - ln / 2, y), (U(u) + ln / 2, y)], c=col, w=1.5 + 2 * env(u))

    # ---------------- 1) otevřený dipól pro srovnání
    y = 95
    f.t(380, 24, '1) otevřený půlvlnný dipól (pro srovnání)', size=15, w='bold')
    envelope(y, 42, 1, BL)
    f.l(x0, y, gap0, y, w=4); f.l(gap1, y, x1, y, w=4)
    arrows(y - 16, 42, BL, skip_mid=True)
    f.wire((gap0, y), (gap0 + 4, y + 40)); f.wire((gap1, y), (gap1 - 4, y + 40))
    f.arrow([(gap0 - 18, y + 38), (gap0 - 18, y + 8)], c=RED, w=2); f.t(gap0 - 26, y + 30, 'I', size=16, c=RED, w='bold', anchor='end')
    f.t(U(0.5), y - 52, 'rozložení proudu (max. uprostřed, na koncích 0)', size=12, c=BL)
    f.t(x1, y + 34, 'vyzařuje proud I → Z ≈ 73 Ω', size=14, anchor='end', w='bold')

    # ---------------- 2) uzavřený (smyčkový) dipól
    yt, yb = 255, 295
    f.t(380, 165, '2) uzavřený (smyčkový) dipól – dva vodiče λ/2 spojené na koncích', size=15, w='bold')
    envelope(yt, 50, 1, BL)
    envelope(yb, 50, -1, RED)
    r = (yb - yt) / 2
    f.a(f'<path d="M {gap0},{yb} L {x0},{yb} A {r} {r} 0 0 1 {x0},{yt} L {x1},{yt} A {r} {r} 0 0 1 {x1},{yb} L {gap1},{yb}" '
        f'stroke="{TX}" stroke-width="4" fill="none"/>')
    arrows(yt - 17, 50, BL)
    arrows(yb + 17, 50, RED, skip_mid=True)
    f.t(x0 - 2, yt - 44, 'horní vodič: proud I', size=13, c=BL, w='bold', anchor='start')
    f.t(x0 - 2, yb + 58, 'dolní vodič: proud I (z napáječe)', size=13, c=RED, w='bold', anchor='start')
    f.t(x1 + 4, (yt + yb) / 2 + 5, '', size=1)
    f.t(x0 - 30, (yt + yb) / 2 + 5, 'I = 0', size=13, c=GR, anchor='end'); f.t(x1 + 30, (yt + yb) / 2 + 5, 'I = 0', size=13, c=GR, anchor='start')
    # napáječ
    f.wire((gap0, yb), (gap0, yb + 105)); f.wire((gap1, yb), (gap1, yb + 105))
    f.arrow([(gap0 - 14, yb + 105), (gap0 - 14, yb + 62)], c=RED, w=2.2); f.t(gap0 - 22, yb + 92, 'I z napáječe', size=14, c=RED, w='bold', anchor='end')
    f.t(gap1 + 12, yb + 95, 'napáječ (dvoulinka 300 Ω)', size=12, anchor='start')
    f.t(U(0.5), yt + 25, 'proudy v obou vodičích mají STEJNÝ směr →', size=12, c=TX, w='bold')

    # ---------------- vysvětlení
    yy = 460
    f.rect(30, yy - 22, 700, 190, fill='#f7f9fc', stroke=BLF, sw=1.2, rx=8)
    lines = [
        ('① Vyzářený výkon závisí na celkovém proudu antény (jako u dipólu):  P = I celk² · 73 Ω', TX, 'normal'),
        ('② Celkový proud: I celk = I (dolní) + I (horní) = 2 I   →   P = (2 I)² · 73 Ω = 4 · I² · 73 Ω', TX, 'normal'),
        ('③ Napáječ ale dodává jen svůj proud I. Pro výkon na jeho svorkách platí  P = I² · Z vst', TX, 'normal'),
        ('④ Jde o tentýž výkon, tedy:  I² · Z vst = 4 · I² · 73 Ω   →   Z vst = 4 · 73 Ω ≈ 292 Ω ≈ 300 Ω', RED, 'bold'),
        ('Jednoduše: výkon roste s druhou mocninou proudu. Stejný výkon projde při polovičním proudu,', GR, 'normal'),
        ('proto musí být impedance 2² = 4× větší.', GR, 'normal'),
    ]
    for k, (txt, c, w) in enumerate(lines):
        f.t(48, yy + 6 + k * 28, txt, size=14, c=c, w=w, anchor='start')
    return f, ('Rozložení proudu: čárkované obrysy ukazují velikost proudu podél vodičů (uprostřed maximum, na koncích '
               'nula), šipky jeho směr a velikost. U smyčkového dipólu teče horním i dolním vodičem stejně velký proud '
               've stejném směru, takže anténa vyzařuje jako dipól s dvojnásobným proudem. Napáječ přitom dodává jen proud '
               'jednoho vodiče – vstupní impedance je proto asi 4 × 73 Ω ≈ 300 Ω.')


def f_standing():
    f = F(300)
    for k, (y0, s, lab, c) in enumerate([(110, 1, 'PSV = 1 (přizpůsobeno) – napětí všude stejné', GRN),
                                          (250, 3, 'PSV = 3 – stojaté vlny: maxima a minima', RED)]):
        x0, w = 140, 560
        f.t(x0 + w / 2, y0 - 75, lab, size=14, w='bold', c=c)
        f.box(20, y0 - 45, 90, 40, 'TX', size=14)
        f.l(110, y0 - 25, x0, y0 - 25, w=2)
        f.l(x0, y0, x0 + w, y0, GR, 1.2)
        g = (s - 1) / (s + 1)
        pts = [(x0 + i * w / 300, y0 - 50 * math.sqrt(1 + g * g + 2 * g * math.cos(2 * math.pi * 2.5 * i / 300)) / (1 + g)) for i in range(301)]
        f.path(pts, c=c, w=2.4)
        f.t(x0 + w + 10, y0 - 20, 'anténa', anchor='start', size=13)
        if s > 1:
            f.t(x0 + w * 0.6 - 30, y0 - 58, 'U max', size=12, c=RED); f.t(x0 + w * 0.4 - 25, y0 - 2, 'U min', size=12, c=RED)
    f.t(380, 290, 'PSV = U max / U min', size=16, w='bold', c=BL)
    return f, ('Je-li vedení zakončeno impedancí rovnou jeho charakteristické impedanci, odražená vlna nevzniká a '
               'napětí podél vedení je všude stejné (PSV = 1). Při nepřizpůsobení se přímá a odražená vlna skládají do '
               'stojatých vln.')


def f_coax():
    f = F(260)
    cx, cy = 150, 130
    f.circle(cx, cy, 100, fill='#555555', stroke=TX)
    f.circle(cx, cy, 90, fill='#c08a3e', stroke=TX)
    f.circle(cx, cy, 82, fill='#f4f1e1', stroke=TX)
    f.circle(cx, cy, 20, fill='#c08a3e', stroke=TX)
    f.arrow([(cx - 82, cy + 48), (cx + 82, cy + 48)], c=RED, w=1.6, both=True); f.t(cx, cy + 70, 'D', size=16, c=RED, w='bold')
    f.arrow([(cx - 20, cy), (cx + 20, cy)], c=BL, w=1.4, both=True); f.t(cx, cy - 26, 'd', size=16, c=BL, w='bold')
    f.t(cx + 46, cy - 40, 'ε r', size=15, w='bold')
    f.t(cx, 252, 'plášť, stínění, dielektrikum, střední vodič', size=12, c=GR)
    f.t(500, 70, 'Z₀ = (60 / √ε r) · ln (D / d)', size=20, w='bold', c=BL)
    f.t(500, 115, 'příklad: plné PE (ε r = 2,3), D/d = 3,5', size=14)
    f.t(500, 140, '→ Z₀ ≈ 39,6 · 1,25 ≈ 50 Ω', size=15, w='bold')
    f.t(500, 185, 'Na délce kabelu impedance nezávisí!', size=14, c=RED)
    f.t(500, 210, 'běžně 50 Ω (vysílače) a 75 Ω (TV)', size=13, c=GR)
    return f, ('Charakteristická impedance koaxiálního kabelu závisí jen na poměru průměrů vnějšího a vnitřního vodiče '
               'a na permitivitě dielektrika – ne na délce kabelu ani na kmitočtu.')


def f_vf():
    f = F(290)
    x0, w = 160, 560
    f.t(20, 75, 'volný prostor', size=13, anchor='start')
    f.sine(x0, 80, w, 35, 2, c=BL)
    f.arrow([(x0, 130), (x0 + w / 2, 130)], c=BL, w=1.5, both=True); f.t(x0 + w / 4, 150, 'λ', size=15, c=BL, w='bold')
    f.t(20, 205, 'v kabelu', size=13, anchor='start')
    f.rect(x0 - 10, 170, w + 20, 70, fill='#f4f1e1', stroke=GR, sw=1, rx=8)
    f.sine(x0, 205, w * 0.66, 30, 2 * 0.66 / 0.66, c=RED)
    f.arrow([(x0, 262), (x0 + w * 0.33, 262)], c=RED, w=1.5, both=True); f.t(x0 + w * 0.33 + 10, 267, 'k · λ', size=15, c=RED, w='bold', anchor='start')
    f.t(560, 20, 'k = v vedení / c ≈ 1 / √ε r', size=15, w='bold', anchor='middle')
    f.t(640, 200, 'plné PE: k ≈ 0,66\npěnové: k ≈ 0,8', size=13, c=GR)
    return f, ('V dielektriku kabelu se vlna šíří pomaleji než ve vzduchu, proto je vlnová délka na vedení kratší. '
               'Zkracovací činitel k je nutné započítat např. při stavbě vedení λ/4 nebo λ/2 (transformátory, fázovací '
               'vedení).')


def f_wg():
    f = F(260)
    x, y, a, b, d = 60, 90, 170, 85, 70
    f.path([(x, y), (x + a, y), (x + a, y + b), (x, y + b)], c=TX, fill='#d9d9d9', close=True, w=2)
    f.path([(x, y), (x + d, y - d * 0.6), (x + a + d, y - d * 0.6), (x + a, y)], c=TX, fill='#eeeeee', close=True, w=2)
    f.path([(x + a, y), (x + a + d, y - d * 0.6), (x + a + d, y + b - d * 0.6), (x + a, y + b)], c=TX, fill='#bbbbbb', close=True, w=2)
    f.rect(x + 8, y + 8, a - 16, b - 16, fill='#ffffff', stroke=TX, sw=1.2)
    f.arrow([(x, y + b + 20), (x + a, y + b + 20)], c=RED, w=1.5, both=True); f.t(x + a / 2, y + b + 42, 'a (širší strana)', size=13, c=RED)
    f.t(x + a / 2, 240, 'f mezní = c / (2a)', size=16, w='bold', c=RED)
    x0, y0, w, h = 400, 220, 320, 180
    f.axes(x0, y0, w, h, 'f', 'útlum')
    X = lambda v: x0 + v / 3 * (w - 20)
    f.path([(X(1.0 + i * 0.025), y0 - 25 - (h - 50) * math.exp(-i / 4)) for i in range(77)], c=BL, w=2.5)
    f.rect(x0 + 1, y0 - h + 20, X(1) - x0 - 1, h - 20, fill=RED, stroke='none', op=0.12)
    f.t((x0 + X(1)) / 2, y0 - 60, 'vlna\nneprojde', size=13, c=RED)
    f.l(X(1), y0, X(1), y0 - h + 20, RED, 1.2, '4,4'); f.t(X(1), y0 + 20, 'f mezní', size=13, c=RED)
    f.t(X(2.1), y0 - 85, 'malý útlum', size=13, c=GRN)
    return f, ('Vlnovod je dutá kovová trubka. Vlna se jím šíří jen nad mezním kmitočtem, který je dán rozměry '
               '(širší strana a ≈ λ/2). Proto se vlnovody používají až na mikrovlnách – pro nízké kmitočty by byly '
               'obrovské.')


def f_gp():
    f = F(280)
    bx, by = 170, 170
    f.l(bx, by, bx, 40, w=4); f.t(bx + 12, 70, 'zářič λ/4', anchor='start', size=13)
    for dx, dy in ((-120, 60), (120, 60), (-60, 85), (70, 80)):
        f.l(bx, by, bx + dx, by + dy, w=2.5)
    f.t(bx - 110, by + 85, 'radiály', size=13)
    f.wire((bx, by), (bx, 265)); f.t(bx + 10, 262, 'koax', size=12, anchor='start')
    f.arrow([(bx - 70, 140), (bx - 70, 60)], c=RED, w=2.2, both=True); f.t(bx - 80, 105, 'E', size=16, c=RED, w='bold', anchor='end')
    f.t(bx - 80, 125, 'vertikální\npolarizace', size=12, c=RED, anchor='end')
    cx, cy, R = 560, 145, 95
    f.circle(cx, cy, R, fill=BLF, stroke=BL, sw=2.5, op=0.6)
    f.circle(cx, cy, 6, fill=TX)
    for k in range(8):
        a = k * math.pi / 4
        f.arrow([(cx + 15 * math.cos(a), cy + 15 * math.sin(a)), (cx + (R - 12) * math.cos(a), cy + (R - 12) * math.sin(a))], c=BL, w=1.4)
    f.t(cx, 30, 'diagram v horizontální rovině (pohled shora)', size=13, w='bold')
    f.t(cx, 268, 'všesměrová – vyzařuje stejně do všech směrů', size=12, c=GR)
    return f, ('Anténa GP je svislý čtvrtvlnný zářič s radiály, které tvoří umělou zem. Vyzařuje všesměrově (v '
               'horizontální rovině kruh) a protože je zářič svislý, je polarizace vertikální.')


def f_balun():
    f = F(240)
    f.l(30, 70, 150, 70, w=4); f.l(170, 70, 290, 70, w=4)
    f.t(160, 35, 'dipól – symetrický', size=14, w='bold')
    f.wire((150, 70), (150, 120)); f.wire((170, 70), (170, 120))
    f.t(160, 225, 'obě svorky „živé“', size=12, c=GR)
    for x, c in ((340, BL), (380, RED)):
        d = 'M %d,90' % x
        for k in range(4):
            d += ' A 12 12 0 0 %d %d,%d' % (1 if x == 380 else 0, x, 90 + (k + 1) * 24)
        f.a(f'<path d="{d}" stroke="{c}" stroke-width="2.2" fill="none"/>')
    f.l(357, 85, 357, 190, w=2); f.l(363, 85, 363, 190, w=2)
    f.wire((150, 120), (300, 120), (300, 90), (340, 90)); f.wire((170, 120), (170, 186), (340, 186))
    f.rect(280, 60, 160, 150, stroke=GR, sw=1.2, dash='5,4', rx=6); f.t(360, 230, 'BALUN', size=15, w='bold')
    f.wire((380, 90), (470, 90)); f.wire((380, 186), (430, 186), (430, 110), (470, 110))
    f.l(470, 90, 700, 90, w=2.5); f.rect(470, 100, 230, 16, fill='#888888', stroke=TX, sw=1)
    f.t(585, 60, 'koaxiální kabel – nesymetrický', size=14, w='bold')
    f.t(585, 165, 'stínění je uzemněno', size=12, c=GR)
    gnd(f, 600, 116)
    f.t(585, 225, 'BALanced → UNbalanced', size=13, c=BL)
    return f, ('Balun (balanced–unbalanced) propojí symetrickou anténu (dipól) s nesymetrickým koaxiálním kabelem. '
               'Brání tomu, aby po vnějším povrchu stínění tekl proud a kabel vyzařoval; často zároveň transformuje '
               'impedanci (1:1, 1:4).')


def f_yagi():
    f = F(290)
    by = 140
    f.l(30, by, 420, by, w=4, c=GR); f.t(225, by + 105, 'ráhno', size=12, c=GR)
    els = [(50, 95, 'R', TX), (110, 88, 'Z', RED), (180, 80, 'D', BL), (250, 78, 'D', BL), (320, 76, 'D', BL), (390, 74, 'D', BL)]
    for x, hl, lab, c in els:
        f.l(x, by - hl, x, by + hl, w=3.5, c=c); f.t(x, by + hl + 18, lab, size=13, w='bold', c=c)
    f.arrow([(430, by), (470, by)], c=RED, w=2.5); f.t(450, by - 12, 'směr', size=12, c=RED)
    f.t(225, 28, 'R reflektor · Z zářič · D direktory', size=13)
    x0, y0, w, h = 500, 240, 230, 180
    f.axes(x0, y0, w, h, '', 'zisk [dBd]'); f.t(x0 + w, y0 + 38, 'počet prvků', anchor='end', size=13)
    pts = [(2, 4), (3, 6), (4, 7.2), (5, 8.2), (6, 9), (8, 10.3), (10, 11.2), (12, 12), (16, 13.2), (20, 14.2)]
    X = lambda n: x0 + (n - 1) / 20 * (w - 15)
    Y = lambda g: y0 - g / 16 * (h - 10)
    f.path([(X(n), Y(g)) for n, g in pts], c=BL, w=2.5)
    for n, g in pts: f.circle(X(n), Y(g), 3, fill=BL, stroke=BL)
    for n in (5, 10, 15): f.t(X(n), y0 + 18, str(n), size=12)
    for g in (5, 10, 15): f.t(x0 - 5, Y(g) + 4, str(g), size=12, anchor='end')
    f.t(x0 + 120, y0 - h + 10, 'orientačně', size=12, c=GR)
    return f, ('Yagi anténa: zářič, za ním delší reflektor a před ním kratší direktory. Každý další direktor (a delší '
               'ráhno) zúží hlavní lalok a zvýší zisk – ale stále pomaleji (zdvojnásobení délky přidá jen asi 2–3 dB).')


def f_quad():
    f = F(290)
    def sq(cx, cy, s, c, dx=40, dy=-25):
        f.path([(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s)], c=c, w=3, close=True)
    sq(240, 130, 90, GR)
    f.path([(150 + 120, 40 + 25), (330 + 120, 40 + 25), (330 + 120, 220 + 25), (150 + 120, 220 + 25)], c=RED, w=3, close=True)
    f.l(240, 130, 360, 155, GR, 3)
    f.circle(360, 245, 6, fill=RED, stroke=RED); f.t(360, 270 - 2, '', size=1)
    f.t(360, 274, 'napájení', size=12, c=RED)
    f.t(240, 30, 'reflektor', size=13, c=GR); f.t(470, 55, 'zářič – uzavřená smyčka\nobvod ≈ 1 λ (strana λ/4)', size=13, c=RED, anchor='start')
    f.t(560, 170, 'smyčkové antény: quad,\ndelta loop, magnetická\nsmyčka (malá loop)', size=13, anchor='start', c=GR)
    return f, ('Anténa quad má prvky tvořené uzavřenými čtvercovými smyčkami o obvodu asi jedné vlnové délky. '
               'Dvouprvkový quad má zisk podobný tříprvkové Yagi.')


def f_reflect():
    f = F(290)
    for k, (y, za, lab, c, refl) in enumerate([(80, '50 Ω', 'Z antény = Z₀ → žádný odraz, PSV = 1', GRN, False),
                                                (200, '150 Ω', 'Z antény ≠ Z₀ → část výkonu se odrazí', RED, True)]):
        f.box(20, y - 25, 80, 50, 'TX', size=14)
        f.l(100, y - 8, 470, y - 8, w=2.5); f.l(100, y + 8, 470, y + 8, w=2.5)
        f.t(285, y - 34, 'napáječ Z₀ = 50 Ω', size=12, c=GR)
        f.box(470, y - 25, 90, 50, 'anténa\n' + za, size=13, fill='#eaf5ea' if not refl else '#fdecea', stroke=c)
        f.arrow([(130, y - 18), (300, y - 18)], c=BL, w=2) if False else None
        f.arrow([(150, y + 25), (330, y + 25)], c=BL, w=2)
        if refl: f.arrow([(440, y + 42), (260, y + 42)], c=RED, w=2)
        f.t(620, y + 5, lab, size=12, c=c, anchor='start') if False else f.t(380, y + 62 if refl else y + 45, lab, size=13, c=c, w='bold')
    f.t(580, 190, 'Γ = (Z − Z₀)/(Z + Z₀)\n= 100/200 = 0,5\nPSV = 3', size=13, anchor='start', c=RED)
    return f, ('Stojaté vlny vznikají skládáním přímé a odražené vlny. Odraz nevznikne, když se impedance antény rovná '
               'charakteristické impedanci napáječe – případně se rozdíl vyrovná přizpůsobovacím členem přímo u antény.')


def polar(f, cx, cy, R, fn, c=BL, fill=BLF, rot=0, n=360, rings=True):
    if rings:
        for k in (0.25, 0.5, 0.75, 1):
            f.circle(cx, cy, R * k, stroke='#dddddd', sw=1)
        for k in range(12):
            a = k * math.pi / 6
            f.l(cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), '#e6e6e6', 0.8)
    pts = []
    for i in range(n + 1):
        th = 2 * math.pi * i / n
        r = fn(th)
        pts.append((cx + R * r * math.cos(th + rot), cy - R * r * math.sin(th + rot)))
    f.path(pts, c=c, fill=fill, op=0.55, w=2.2)


def f_fb():
    f = F(300)
    cx, cy, R = 300, 150, 125
    yagi = lambda th: ((1 + math.cos(th)) / 2) ** 3 + 0.1 * max(0, -math.cos(th)) ** 2 * (1 - 0.3 * math.sin(th) ** 2)
    polar(f, cx, cy, R, yagi)
    f.arrow([(cx, cy), (cx + R, cy)], c=BL, w=2.4); f.t(cx + R - 20, cy - 12, 'vpřed', size=13, c=BL, w='bold')
    f.arrow([(cx, cy), (cx - R * 0.1, cy)], c=RED, w=2.4); f.t(cx - R * 0.1 - 10, cy - 12, 'vzad', size=13, c=RED, w='bold', anchor='end')
    f.t(560, 100, 'F/B = 10 · log (P vpřed / P vzad)', size=15, w='bold', anchor='start' if False else 'middle')
    f.t(590, 140, 'příklad: P vzad = 1/100 P vpřed', size=13)
    f.t(590, 165, '→ F/B = 20 dB', size=15, c=RED, w='bold')
    f.t(590, 210, 'potlačí rušení a stanice\nze zadního směru', size=13, c=GR)
    return f, ('Předozadní poměr (F/B, front-to-back) porovnává výkon vyzářený hlavním lalokem dopředu s výkonem '
               'vyzářeným opačným směrem. Udává se v dB; u dobré Yagi bývá 15–25 dB.')


def f_dippat():
    f = F(300)
    dp = lambda th: abs(math.cos(math.pi / 2 * math.cos(th)) / math.sin(th)) if abs(math.sin(th)) > 1e-3 else 0
    cx, cy, R = 170, 160, 115
    polar(f, cx, cy, R, dp)
    f.l(cx - 60, cy, cx + 60, cy, RED, 5); f.t(cx, 22, 'řez rovinou dipólu: „osmička“', size=13, w='bold')
    f.t(cx + 70, cy + 20, 'dipól', size=12, c=RED, anchor='start')
    f.t(cx, 295, 've směru drátu (osy) nevyzařuje', size=12, c=GR)
    cx2 = 420
    f.circle(cx2, cy, R * 0.85, fill=BLF, stroke=BL, sw=2.2, op=0.55)
    f.circle(cx2, cy, 7, fill=RED, stroke=RED); f.t(cx2, 22, 'pohled ve směru osy: kruh', size=13, w='bold')
    cx3, cy3 = 640, 160
    f.ellipse(cx3 - 48, cy3, 45, 75, fill=BLF, stroke=BL, op=0.55, sw=2)
    f.ellipse(cx3 + 48, cy3, 45, 75, fill=BLF, stroke=BL, op=0.55, sw=2)
    f.ellipse(cx3, cy3 - 2, 92, 22, stroke=BL, sw=1.4, dash='5,4')
    f.l(cx3 - 110, cy3, cx3 + 110, cy3, RED, 4)
    f.t(cx3, 22, 'prostorově: „kobliha“ (toroid)', size=13, w='bold')
    f.t(cx3, 270, 'osmička rotující\nkolem osy antény', size=12, c=GR)
    return f, ('Diagram ideálního půlvlnného dipólu: v rovině procházející dipólem má tvar osmičky s nulami ve směru '
               'drátu. Otočením osmičky kolem osy antény vznikne prostorový tvar „koblihy“ (toroidu).')


def f_wire():
    f = F(250)
    items = [(95, 'dipól'), (265, 'invertované V'), (435, 'dlouhý drát'), (605, 'delta loop')]
    gy = 200
    for x, lab in items:
        f.l(x - 80, gy, x + 80, gy, GR, 1)
        f.t(x, gy + 25, lab, size=13)
    f.l(25, gy, 25, 80, '#8d6e63', 3); f.l(165, gy, 165, 80, '#8d6e63', 3)
    f.path([(25, 85), (90, 95), (100, 95), (165, 85)], c=BL, w=2.2); f.wire((95, 95), (95, gy))
    f.l(265, gy, 265, 60, '#8d6e63', 3); f.path([(195, gy - 20), (265, 65), (335, gy - 20)], c=BL, w=2.2)
    f.l(365, gy, 365, 90, '#8d6e63', 3); f.path([(365, 95), (505, 70)], c=BL, w=2.2); f.l(505, gy, 505, 65, '#8d6e63', 3)
    f.l(605, gy, 605, 50, '#8d6e63', 3); f.path([(605, 55), (540, 170), (670, 170)], c=BL, w=2.2, close=True)
    f.t(380, 25, 'drátové antény – natažený vodič mezi stožáry, stromy…', size=14, w='bold', c=BL)
    return f, ('Dipól, invertované V, dlouhý drát nebo smyčky se běžně staví z drátu nataženého mezi podpěrami. Yagi '
               'naopak potřebuje tuhé prvky (trubky) přesně rozmístěné na ráhnu, aby byla otočná a zachovala rozměry – '
               'viz obrázek u otázky f) 10.')


FIGS = {
    ('c', 0): c_lc_par, ('c', 1): c_graetz, ('c', 2): c_rpar, ('c', 3): c_cpar, ('c', 4): c_rpar_num, ('c', 5): c_pi,
    ('c', 6): c_overmod, ('c', 7): c_psfilter, ('c', 8): c_osc, ('c', 9): c_bfo, ('c', 10): c_diodrc, ('c', 11): c_zener,
    ('c', 12): c_lc_series, ('c', 13): c_lc_parz, ('c', 14): c_pll,
    ('d', 0): d_rit, ('d', 1): d_upconv, ('d', 2): d_nobfo, ('d', 3): d_lo, ('d', 4): d_mixer, ('d', 5): d_sum,
    ('d', 6): d_smeter, ('d', 7): d_image, ('d', 8): d_nf, ('d', 9): d_sens, ('d', 10): d_imd, ('d', 11): d_sel,
    ('d', 12): d_squelch, ('d', 13): d_ifamp, ('d', 14): d_sdr,
    ('e', 0): e_stab, ('e', 1): e_am_ssb, ('e', 2): e_ssb_steps, ('e', 3): e_dev, ('e', 4): e_hum, ('e', 5): e_pep,
    ('e', 6): e_tube, ('e', 7): e_trans, ('e', 8): e_ssbfilter, ('e', 9): e_match, ('e', 10): e_noload,
    ('f', 0): f_swr, ('f', 1): f_dipole, ('f', 2): f_folded, ('f', 3): f_standing, ('f', 4): f_coax, ('f', 5): f_vf,
    ('f', 6): f_wg, ('f', 7): f_gp, ('f', 8): f_balun, ('f', 9): f_yagi, ('f', 10): f_quad, ('f', 11): f_reflect,
    ('f', 12): f_fb, ('f', 13): f_dippat, ('f', 14): f_wire,
}


def figure(sec, pos):
    if sec == 'g':
        from obrazky_sireni_q import FIGS_G
        fn = FIGS_G.get((sec, pos))
    else:
        fn = FIGS.get((sec, pos))
    if not fn:
        return None
    fg, cap = fn()
    return fg.done(), fg.w, fg.h, cap


if __name__ == '__main__':   # náhledy: python3 -I obrazky_elek.py VÝSTUPNÍ_SLOŽKA
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for (s, p) in FIGS:
        svg, w, h, cap = figure(s, p)
        open(os.path.join(out, f'{s}{p:02d}.svg'), 'wb').write(svg)
    print(len(FIGS), 'obrázků')
