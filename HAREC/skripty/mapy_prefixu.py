# -*- coding: utf-8 -*-
"""Mapy kontinentů s hranicemi států a prefixy z otázek ČTÚ (provoz f) – SVG bez externích knihoven.

Hranice: Natural Earth 1:50m Admin 0 – Countries v5.1.2 (public domain),
zdroje/geo/ne_50m_admin_0_countries.geojson (https://www.naturalearthdata.com).
Na mapách jsou popsány JEN státy a území, na které se ptá ČTÚ (provoz f), a to přesně odpovědí ČTÚ;
ostatní státy jsou šedé bez popisku. Projekce: Lambertova azimutální stejnoplochá se středem v kontinentu.

generate(otazky_f, cesta_geojson) -> [(název, popis, svg_bytes, šířka, výška)]
  otazky_f = [(číslo, text otázky, odpověď)] – z data/faq.json (po opravách FIX v build.py)
Náhledy: python3 -I skripty/mapy_prefixu.py KOŘEN_PROJEKTU VÝST_SLOŽKA
"""
import json, math, re, sys
from xml.sax.saxutils import escape

W = 1700                     # 1 jednotka = 0,1 mm při šířce rámce 17 cm
HMAX = 2150                  # max. výška mapy (21,5 cm)
FONT = 'font-family="Liberation Sans, Arial, sans-serif"'
FS_P, FS_N = 27, 17          # prefix (≈ 7,7 pt), název (≈ 4,8 pt)

SEA, LAND, BORDER, GRAT = '#dbeaf7', '#e6e6e6', '#9a9a9a', '#c4d8ec'
PAL = ['#f6d8a8', '#c9e2b3', '#f4c2c2', '#c6d4ef', '#efe39b', '#d9c6ea', '#b8e0dc']   # podle MAPCOLOR7
C_PFX, C_NAME, C_DOT = '#14306b', '#333333', '#b03020'

# číslo otázky ČTÚ provoz f) -> (ADM0_A3 státu v Natural Earth | None, kotva (lon, lat) | None)
# kotva None = LABEL_X/LABEL_Y z Natural Earth; u území bez vlastního polygonu je kotva bod (tečka na mapě).
ENTRIES = {
    1: ('CZE', None), 2: ('NLD', None), 3: ('DEU', None), 4: ('SWE', (16.0, 63.5)), 5: ('AUT', None),
    6: ('FIN', None), 7: ('SVK', None), 8: ('DNK', None), 9: ('POL', None), 10: ('NOR', (9.0, 61.6)),
    11: ('FRA', None), 12: ('ESP', None), 13: ('ITA', (12.5, 43.0)), 14: ('GRC', (22.0, 39.6)), 15: ('SVN', None),
    16: ('BGR', None), 17: ('HUN', None), 18: ('ROU', None), 19: ('UKR', None), 20: ('PRT', None),
    21: ('RUS', None), 22: ('USA', None), 23: ('EST', None), 24: ('CAN', (-100.0, 57.0)), 25: ('LTU', None),
    26: ('AUS', None), 27: ('LVA', None), 28: ('JPN', None), 29: ('BEL', None), 30: ('BRA', None),
    31: ('LUX', None), 32: ('ZAF', None), 33: ('HRV', None), 34: ('ARG', None), 35: ('MKD', None),
    36: ('IND', None), 37: ('CHE', None), 38: (None, (-4.3, 57.0)), 39: (None, (-15.6, 28.3)), 40: ('AND', None),
    41: (None, (-28.0, 38.6)), 42: (None, (2.9, 39.6)), 43: (None, (-5.3, 35.9)), 44: ('IRL', None),
    45: ('MDA', None), 46: ('BLR', None), 47: (None, (-1.5, 52.4)), 48: ('IMN', None), 49: (None, (-6.7, 54.6)),
    50: ('JEY', None), 51: ('GGY', None), 52: (None, (-3.7, 52.3)), 53: ('LIE', None), 54: ('VAT', None),
    55: (None, (9.0, 40.0)), 56: (None, (17.0, 78.6)), 57: (None, (-8.5, 71.0)), 58: ('ALD', None),
    59: (None, (19.13, 60.30)), 60: ('GRL', None), 61: ('FRO', None), 62: (None, (28.0, 36.3)),
    63: (None, (24.9, 35.25)), 64: ('SMR', None), 65: ('BIH', None), 66: ('TUR', None), 67: ('ISL', None),
    68: (None, (9.1, 42.1)), 69: ('SRB', None), 70: ('ALB', None), 71: ('MCO', None), 72: ('MLT', None),
    73: ('TWN', None), 74: ('CHN', None), 75: ('CUB', None), 76: ('ARM', None), 77: ('KOR', None),
    78: ('PRK', None), 79: ('THA', None), 80: ('SAU', None), 81: ('MEX', None), 82: ('NZL', None),
    83: ('MNE', None), 84: ('GEO', None), 85: ('ISR', None),
}
# na které mapě je otázka popsána (výchozí: jen Evropa)
ON_MAPS = {21: ('evropa', 'asie'), 66: ('evropa', 'asie'), 84: ('asie',), 76: ('asie',), 85: ('asie',),
           28: ('asie',), 36: ('asie',), 73: ('asie',), 74: ('asie',), 77: ('asie',), 78: ('asie',), 79: ('asie',), 80: ('asie',),
           32: ('afrika',), 39: ('evropa', 'afrika'), 43: ('evropa', 'afrika'),
           22: ('samerika',), 24: ('samerika',), 75: ('samerika',), 81: ('samerika',), 60: ('evropa', 'samerika'),
           30: ('jamerika',), 34: ('jamerika',), 26: ('oceanie',), 82: ('oceanie',)}
# kotvy pro konkrétní mapu (stát na více mapách)
ANCHOR_MAP = {('asie', 21): (100.0, 63.0), ('evropa', 21): (37.0, 61.0), ('asie', 66): (35.0, 39.0), ('evropa', 66): (30.0, 39.8)}
# zkrácené názvy (jinak text otázky ČTÚ bez dvojtečky)
SHORT = {22: 'USA', 32: 'Jihoafrická rep.', 43: 'Ceuta', 48: 'Man', 59: 'Market Reef',
         77: 'Jižní Korea', 78: 'Severní Korea', 35: 'Makedonie', 65: 'Bosna a Herc.', 39: 'Kanárské o.'}


# (klíč, název, střed projekce (lon, lat), body, které musí být vidět (lon, lat))
# Území mimo výřez (např. Azory, Špicberky na mapě Evropy) mají popisek u okraje se šipkou směrem k nim.
MAPS = [
    ('evropa', 'Evropa', (12.0, 52.0), [(-24.5, 63.0), (-10.5, 36.0), (29.0, 71.2), (41.0, 56.0), (33.0, 34.8), (-10.5, 52.0), (14.4, 35.0), (24.9, 34.4), (-5.3, 35.3)]),
    ('asie', 'Asie', (95.0, 42.0), [(26.0, 30.0), (148.0, 40.0), (100.0, 77.0), (78.0, 6.0), (122.0, 21.0), (40.0, 13.0)]),
    ('afrika', 'Afrika', (17.0, 2.0), [(-18.5, 36.5), (52.0, 12.0), (17.0, -35.5), (17.0, 37.8), (-17.5, 27.5)]),
    ('samerika', 'Severní a Střední Amerika', (-95.0, 47.0), [(-168.0, 66.0), (-12.0, 76.0), (-80.0, 8.0), (-118.0, 18.0), (-60.0, 83.0)]),
    ('jamerika', 'Jižní Amerika', (-60.0, -20.0), [(-82.0, 12.0), (-34.0, -8.0), (-68.0, -56.0), (-60.0, 12.5)]),
    ('oceanie', 'Austrálie a Oceánie', (150.0, -25.0), [(112.0, -10.0), (179.0, -47.5), (150.0, -2.0), (113.0, -35.0), (179.0, -37.0)]),
]
G = 6   # mřížka masky pevniny (jednotky SVG)


def laea(lon0, lat0):
    l0, p0 = math.radians(lon0), math.radians(lat0)
    def f(lon, lat):
        l, p = math.radians(lon), math.radians(lat)
        c = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)
        if c < -0.94:
            return None
        k = math.sqrt(2 / (1 + c))
        x = k * math.cos(p) * math.sin(l - l0)
        y = k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
        return x, -y
    return f


def rings(geom):
    if geom['type'] == 'Polygon':
        return geom['coordinates']
    return [r for poly in geom['coordinates'] for r in poly]


def tw(s, fs, bold):
    return sum((0.66 if c.isupper() or c.isdigit() else 0.36 if c in ',.:il ' else 0.55) for c in s) * fs * (1.0 if bold else 0.92)


def overlap(a, b, pad=4):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def seg_x(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def seg_box(p1, p2, b):
    if b[0] <= p1[0] <= b[2] and b[1] <= p1[1] <= b[3]:
        return True
    cs = [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]
    return any(seg_x(p1, p2, cs[i], cs[(i + 1) % 4]) for i in range(4))


class Mask:
    """Rastrová maska polygonů (scanline, sudo-lichá pravidla po prstencích); hodnota = index státu + 1."""
    def __init__(self, W, H):
        self.nx, self.ny = W // G + 1, H // G + 1
        self.m = [bytearray(self.nx) for _ in range(self.ny)]

    def fill(self, ring, val):
        rows = {}
        n = len(ring)
        for i in range(n):
            (x1, y1), (x2, y2) = ring[i], ring[(i + 1) % n]
            if y1 == y2:
                continue
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            for r in range(max(0, math.ceil(lo / G - 0.5)), min(self.ny - 1, math.floor(hi / G - 0.5)) + 1):
                yc = (r + 0.5) * G
                if lo <= yc < hi:
                    rows.setdefault(r, []).append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        for r, xs in rows.items():
            xs.sort()
            row = self.m[r]
            for a, b in zip(xs[0::2], xs[1::2]):
                for c in range(max(0, math.ceil(a / G - 0.5)), min(self.nx - 1, math.floor(b / G - 0.5)) + 1):
                    row[c] = val

    def get(self, x, y):
        c, r = int(x // G), int(y // G)
        return self.m[r][c] if 0 <= r < self.ny and 0 <= c < self.nx else 0

    def frac(self, box, val=None, n=(6, 3)):
        """Podíl vzorků boxu na pevnině (val=None: libovolný zvýrazněný stát) / na státě val."""
        k = 0
        for i in range(n[0]):
            for j in range(n[1]):
                v = self.get(box[0] + (box[2] - box[0]) * (i + 0.5) / n[0], box[1] + (box[3] - box[1]) * (j + 0.5) / n[1])
                k += (v == val) if val is not None else (v > 0)
        return k / (n[0] * n[1])


def render(mkey, mtitle, center, must, feats, items_all):
    pr = laea(*center)
    pts = [pr(*p) for p in must]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min(W / (x1 - x0), HMAX / (y1 - y0))
    H = round((y1 - y0) * s)
    ox = (W - (x1 - x0) * s) / 2 - x0 * s
    oy = -y0 * s

    def P(lon, lat):
        q = pr(lon, lat)
        return None if q is None else (q[0] * s + ox, q[1] * s + oy)

    items = [it for it in items_all if mkey in ON_MAPS.get(it[0], ('evropa',))]
    codes = {it[3]: k + 1 for k, it in enumerate(items) if it[3]}

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" {FONT}>',
         f'<defs><clipPath id="c{mkey}"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SEA}"/>', f'<g clip-path="url(#c{mkey})">']
    for lat in range(-80, 90, 10):                       # zeměpisná síť po 10°
        o.append(polyline([P(lon / 2, lat) for lon in range(-360, 361)], H, GRAT, 1.4))
    for lon in range(-180, 180, 10):
        o.append(polyline([P(lon, lat / 2) for lat in range(-170, 171)], H, GRAT, 1.4))
    mask = Mask(W, H)
    for f in feats:
        pp = f['properties']
        code = pp['ADM0_A3']
        hl = code in codes
        fill = PAL[(pp['MAPCOLOR7'] - 1) % 7] if hl else LAND
        d = []
        for r in rings(f['geometry']):
            q = [P(*c) for c in r]
            if any(v is None for v in q):
                continue
            bx = [v[0] for v in q]; by = [v[1] for v in q]
            if max(bx) < -50 or min(bx) > W + 50 or max(by) < -50 or min(by) > H + 50:
                continue
            if max(bx) - min(bx) < 1.2 and max(by) - min(by) < 1.2:
                continue
            simp = [q[0]]
            for v in q[1:]:
                if abs(v[0] - simp[-1][0]) + abs(v[1] - simp[-1][1]) >= 2.5:
                    simp.append(v)
            if len(simp) < 3:
                continue
            d.append('M' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in simp) + 'Z')
            mask.fill(simp, codes[code] if hl else 255)
        if d:
            o.append(f'<path d="{" ".join(d)}" fill="{fill}" stroke="{BORDER}" stroke-width="{2.2 if hl else 1.4}" '
                     f'stroke-linejoin="round" fill-rule="evenodd"/>')
    o.append('</g>')

    # ---- popisky: kotvy (mimo výřez -> bod u okraje + šipka)
    M = 14
    cand = []
    for k, (n, name, pfx, code, anc) in enumerate(items):
        q = P(*ANCHOR_MAP.get((mkey, n), anc))
        edge = None
        if not (M < q[0] < W - M and M < q[1] < H - M):
            cx, cy = W / 2, H / 2
            dx, dy = q[0] - cx, q[1] - cy
            t = min((W / 2 - M) / abs(dx) if dx else 1e9, (H / 2 - M) / abs(dy) if dy else 1e9)
            q = (cx + dx * t, cy + dy * t)
            ang = math.degrees(math.atan2(dy, dx))
            edge = '→↓←↑'[int(((ang + 45) % 360) // 90)]   # jen 4 směry – diagonální šipky LibreOffice nevykreslí
        cand.append((n, name, pfx, code, q, edge, k + 1))

    placed, leaders, out_lbl, dots = [], [], [], []
    rest = []
    # 1) vnitřní popisky – box musí ležet z ≥ 85 % na vlastním státě
    for n, name, pfx, code, (x, y), edge, val in sorted(cand, key=lambda c: -tw(c[2], FS_P, True)):
        ok = None
        if code and not edge:
            wp, wn = tw(pfx, FS_P, True), tw(name, FS_N, False)
            for withname in (True, False):
                w = max(wp, wn if withname else 0) + 6
                h = FS_P + (FS_N + 3 if withname else 0) + 4
                for dx, dy in [(0, 0), (0, -25), (0, 25), (-30, 0), (30, 0), (-30, -25), (30, 25), (-30, 25), (30, -25), (0, -50), (0, 50)]:
                    box = (x + dx - w / 2, y + dy - FS_P * 0.85, x + dx + w / 2, y + dy - FS_P * 0.85 + h)
                    if box[0] > 4 and box[2] < W - 4 and box[1] > 4 and box[3] < H - 4 and \
                            mask.frac(box, val) >= 0.85 and not any(overlap(box, b) for b in placed):
                        ok = (box, withname); break
                if ok:
                    break
        if ok:
            box, withname = ok
            placed.append(box)
            out_lbl.append(label((box[0] + box[2]) / 2, box[1], pfx, name if withname else None))
        else:
            rest.append((n, name, pfx, code, (x, y), edge, val))
            dots.append((x, y))
    # 2) vnější popisky s odkazovou čarou – nejdřív ty v nejhustším okolí
    rest.sort(key=lambda c: -sum(1 for d in dots if math.hypot(d[0] - c[4][0], d[1] - c[4][1]) < 160))
    for n, name, pfx, code, (x, y), edge, val in rest:
        nm = f'{name} {edge}' if edge else name
        w = max(tw(pfx, FS_P, True), tw(nm, FS_N, False)) + 12; h = FS_P + FS_N + 10
        best, bcost = None, 1e18
        for r in (0, 30, 50, 75, 100, 130, 165, 205, 250, 300, 360, 430, 520):
            if best and r > bcost:
                break
            for k in range(24):
                ang = math.radians(k * 15)
                cx, cy = x + r * math.cos(ang), y + r * math.sin(ang)
                bx = cx - w / 2 if abs(math.cos(ang)) < 0.4 else (cx if math.cos(ang) > 0 else cx - w)
                by = cy - h / 2 if abs(math.sin(ang)) < 0.4 else (cy if math.sin(ang) > 0 else cy - h)
                if r == 0:
                    bx, by = (x + 8, y - h / 2) if k % 2 == 0 else (x - 8 - w, y - h / 2)
                box = (bx, by, bx + w, by + h)
                if box[0] < 4 or box[1] < 4 or box[2] > W - 4 or box[3] > H - 4:
                    continue
                if any(overlap(box, b, 6) for b in placed):
                    continue
                if any(box[0] - 7 < dx < box[2] + 7 and box[1] - 7 < dy < box[3] + 7 for dx, dy in dots if (dx, dy) != (x, y)):
                    continue
                ex, ey = min(max(x, box[0]), box[2]), min(max(y, box[1]), box[3])
                cost = r + 260 * mask.frac(box) + 120 * mask.frac(box, 255) * 0
                cost += 300 * sum(1 for a, b in leaders if seg_x((x, y), (ex, ey), a, b))
                cost += 300 * sum(1 for a, b in leaders if seg_box(a, b, box))
                cost += 300 * sum(1 for b in placed if seg_box((x, y), (ex, ey), b))
                if cost < bcost:
                    best, bcost = box, cost
        if not best:
            print(f'VAROVÁNÍ mapa {mkey}: popisek f) {n} se nevešel', file=sys.stderr)
            continue
        placed.append(best)
        bx0, by0, bx1, by1 = best
        ex, ey = min(max(x, bx0), bx1), min(max(y, by0), by1)
        if math.hypot(ex - x, ey - y) > 9:
            leaders.append(((x, y), (ex, ey)))
            out_lbl.insert(0, f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{C_DOT}" stroke-width="2"/>')
        out_lbl.append(f'<rect x="{bx0:.0f}" y="{by0:.0f}" width="{bx1 - bx0:.0f}" height="{by1 - by0:.0f}" rx="5" '
                       f'fill="#ffffff" fill-opacity="0.9" stroke="{C_DOT}" stroke-width="1.3"/>')
        out_lbl.append(label((bx0 + bx1) / 2, by0 + 4, pfx, nm))
    for (x, y), e in zip(dots, [c[5] for c in rest]):
        if not e:
            out_lbl.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{C_DOT}" stroke="#ffffff" stroke-width="1.5"/>')
    o += out_lbl
    o.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="#555555" stroke-width="2"/>')
    o.append('</svg>')
    return '\n'.join(o).encode('utf-8'), H, [it[0] for it in items]


def label(x, ytop, pfx, name):
    s = (f'<text x="{x:.0f}" y="{ytop + FS_P * 0.82:.0f}" text-anchor="middle" font-size="{FS_P}" font-weight="bold" '
         f'fill="{C_PFX}">{escape(pfx)}</text>')
    if name:
        s += (f'<text x="{x:.0f}" y="{ytop + FS_P + FS_N * 0.85 + 2:.0f}" text-anchor="middle" font-size="{FS_N}" '
              f'fill="{C_NAME}">{escape(name)}</text>')
    return s


def polyline(seg, H, c, w):
    out, cur = [], []
    for v in seg + [None]:
        if v is None or not (-200 < v[0] < W + 200 and -200 < v[1] < H + 200):
            if len(cur) > 1:
                out.append('M' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in cur))
            cur = []
        else:
            cur.append(v)
    return f'<path d="{" ".join(out)}" fill="none" stroke="{c}" stroke-width="{w}"/>' if out else ''


def norm(a):
    return re.sub(r'\s*,\s*', ', ', re.sub(r'\s*[-–]\s*', '–', a)).strip().replace('vč, ', 'vč. ')


TITLE = 'Mapy prefixů podle kontinentů'
INTRO = ('Mapy ukazují státy a území, na jejichž prefixy se ptá ČTÚ v oddílu provoz f) „Používání prefixů ve volacích '
         'značkách“ (85 otázek). Barevně jsou vyznačeny státy popsané na dané mapě; tmavě modrý prefix je přesně podle '
         'správné odpovědi ČTÚ. Ostatní státy jsou šedé a bez popisku. Malé státy a ostrovy (červená tečka) mají popisek '
         'v rámečku s odkazovou čarou. Ostrovy a části států, které jsou pro radioamatéry samostatnými „zeměmi“ '
         '(např. Sardinie, Kréta, Skotsko), jsou vyznačeny tečkou; území mimo výřez mapy mají popisek u okraje se šipkou. '
         'Hranice států: Natural Earth 1 : 50 m (v5.1.2, volné dílo); Lambertova azimutální stejnoplochá projekce, '
         'zeměpisná síť po 10°.')


def generate(qs, geo):
    gj = json.load(open(geo, encoding='utf-8'))
    feats = [f for f in gj['features'] if f['properties']['ADM0_A3'] != 'ATA']
    byc = {f['properties']['ADM0_A3']: f for f in feats}
    items = []
    for n, q, a in qs:
        if n not in ENTRIES:
            print(f'VAROVÁNÍ: otázka provoz f) {n} není v mapách', file=sys.stderr)
            continue
        code, anc = ENTRIES[n]
        if anc is None:
            p = byc[code]['properties']; anc = (p['LABEL_X'], p['LABEL_Y'])
        name = SHORT.get(n, re.sub(r'\s*(:|OL, OK)\s*$', '', q).strip())
        items.append((n, name, norm(a), code, anc))
    res, shown = [], set()
    for mkey, mtitle, center, must in MAPS:
        data, h, on = render(mkey, mtitle, center, must, feats, items)
        shown |= set(on)
        res.append((mtitle, data, W, h))
    for n, *_ in items:
        if n not in shown:
            print(f'VAROVÁNÍ: otázka provoz f) {n} není na žádné mapě', file=sys.stderr)
    return res


if __name__ == '__main__':
    import os
    root, out = sys.argv[1], sys.argv[2]
    faq = json.load(open(f'{root}/data/faq.json', encoding='utf-8'))
    sec = [s for s in faq[1]['sections'] if s['label'] == 'f'][0]
    qs = [(i['n'], i['q'], i['a'] or 'OL, OK') for i in sec['items']]
    os.makedirs(out, exist_ok=True)
    for j, (t, d, w, h) in enumerate(generate(qs, f'{root}/zdroje/geo/ne_50m_admin_0_countries.geojson'), 1):
        open(f'{out}/mapa{j}.svg', 'wb').write(d)
        print(t, w, h, len(d) // 1024, 'kB')
