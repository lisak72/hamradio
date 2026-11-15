# -*- coding: utf-8 -*-
"""Mapa v Mercatorově projekci se středem nad Prahou a směry z otázek ČTÚ provoz c) 1–7 (SVG bez knihoven).

Směry jsou kresleny jako ortodromy (nejkratší cesty) s výchozím azimutem podle ČTÚ; v Mercatorově projekci
se jeví jako křivky, ale v Praze svírají se severem přesně daný azimut (projekce je úhlojevná).
Cíle mimo výřez jsou naznačeny šipkou u okraje.

Obrysy pevnin jsou ručně zjednodušené (hrubé body lon/lat) – mapa je schematická.
Ověření: azimut po ortodromě z Prahy (50,08 N; 14,42 E) k reprezentativním místům odpovídá odpovědím ČTÚ ±5°.
"""
import math
from xml.sax.saxutils import escape

PRAHA = (50.08, 14.42)
LON0, LON1 = PRAHA[1] - 76.4, PRAHA[1] + 76.4   # výřez: začátek Ameriky … Indie
LAT0, LAT1 = -38.0, 75.0
W = 1000

# (otázka, cíl, azimut podle ČTÚ, reprezentativní místo (lat, lon))
TARGETS = [
    (1, 'USA', 315, (39.0, -100.0)),
    (2, 'Austrálie', 85, (-23.7, 133.9)),
    (3, 'Japonsko', 45, (35.7, 139.7)),
    (4, 'Karibik', 280, (18.0, -75.0)),
    (5, 'Jihoafrická rep.', 175, (-30.0, 22.0)),
    (6, 'Havaj', 355, (20.5, -157.0)),
    (7, 'Argentina', 240, (-34.0, -64.0)),
]

LAND = {
    'Severní Amerika': [(-168, 66), (-162, 70), (-156, 71.3), (-140, 69.6), (-128, 70), (-115, 68.5), (-95, 68), (-85, 69.5), (-82, 66), (-90, 63),
        (-94, 59), (-92, 57), (-82, 55), (-79, 52), (-77, 60), (-78, 62.5), (-73, 62), (-64, 60), (-61, 56), (-56, 52), (-60, 50), (-66, 49.5),
        (-64, 47), (-61, 45.5), (-66, 44.5), (-70, 43), (-70, 41.7), (-74, 40.5), (-76, 37), (-75.5, 35.3), (-81, 31.5), (-80, 27), (-80.5, 25.2),
        (-82.7, 28), (-84, 30), (-89, 30.2), (-94, 29.5), (-97.4, 27.5), (-97.5, 24), (-96, 19.5), (-94.5, 18.3), (-91, 18.7), (-90.5, 21),
        (-87, 21.5), (-88, 16), (-84, 15.8), (-83.5, 11), (-79.5, 9.5), (-77.5, 8.5), (-80, 7.3), (-83, 8.3), (-85.7, 10), (-87.5, 13),
        (-92, 14.5), (-96, 15.7), (-101, 17.5), (-105.5, 20), (-105.5, 23), (-109.5, 26), (-112.5, 30), (-114.5, 31), (-112, 27),
        (-109.5, 23), (-110.2, 23), (-112, 25.5), (-114.5, 28), (-117, 32.5), (-120.5, 34.5), (-122.5, 37.5), (-124, 40.5), (-124, 46),
        (-123, 48.5), (-125, 50), (-130, 54.5), (-134, 58), (-140, 59.8), (-146, 60.6), (-152, 59), (-154, 57.5), (-158, 57), (-162, 55),
        (-158, 58.5), (-162, 60), (-165, 62.5), (-164.5, 64.5), (-166, 65.5)],
    'Grónsko': [(-73, 78), (-60, 82), (-30, 83.5), (-20, 81.5), (-18, 77), (-22, 72), (-24, 70), (-32, 68), (-40, 65), (-43, 60), (-48, 61),
        (-52, 64), (-54, 67), (-53, 70), (-56, 73.5), (-66, 76.5)],
    'Kanadské ostrovy': [(-120, 71.5), (-112, 73), (-100, 73.5), (-90, 74.5), (-80, 73.5), (-75, 72), (-68, 70), (-62, 67), (-68, 63), (-75, 65),
        (-85, 66), (-92, 70), (-105, 69), (-118, 69)],
    'Jižní Amerika': [(-77.5, 8.5), (-76, 9.5), (-72, 12), (-68, 10.6), (-62, 10.7), (-58, 6.8), (-52, 5), (-50, 1.5), (-48, -1), (-44, -2.5),
        (-38, -4), (-35, -7), (-35, -9), (-39, -13.5), (-39, -17.5), (-41, -22), (-44, -23), (-48.5, -26), (-49, -28.5), (-53, -34), (-58, -35),
        (-57, -38), (-62, -39), (-65, -41), (-63.5, -42.5), (-65.5, -45), (-67.5, -46.5), (-66, -48), (-69, -51), (-68.5, -52.5), (-66, -55),
        (-71, -55), (-74, -52), (-75.5, -48), (-74, -44), (-73.5, -40), (-73.5, -37), (-71.5, -32), (-71.4, -28), (-70.3, -23), (-70.2, -18.4),
        (-75, -15.5), (-77, -12), (-79.5, -7.5), (-81.2, -5), (-80, -2), (-80.5, 0), (-79, 1.5), (-77.5, 4), (-77.4, 7)],
    'Eurasie': [(-5.6, 36), (-9, 37), (-9.5, 39), (-8.8, 42.5), (-8, 43.7), (-1.5, 43.4), (-1.2, 46), (-4.5, 47.8), (-1.5, 48.7), (1.5, 50),
        (4, 51.3), (4.7, 53), (8, 53.5), (8.6, 55.5), (8.2, 57), (10.5, 57.7), (10.5, 56), (12, 54.3), (14, 54), (18, 54.8), (21, 55), (21, 57),
        (23.5, 57.5), (24, 59.3), (28.5, 59.8), (22.5, 60.3), (21.3, 61.5), (21.5, 63.5), (25, 65), (22, 65.7), (17.5, 62.5), (18.5, 60),
        (16.5, 57), (14, 55.5), (12.7, 56.5), (11.5, 58.3), (10, 59), (8, 58), (5.6, 59), (5, 62), (8, 63.5), (12.5, 66), (15, 68.3), (19, 70),
        (25, 71), (31, 70.3), (33, 69.3), (41, 67.5), (39.5, 66), (35, 66.5), (32.5, 67), (34.5, 64.5), (37, 63.8), (44, 66), (44, 68.5),
        (53, 68.5), (60, 69.5), (68, 68.5), (73, 72.5), (80, 72.5), (87, 74.5), (98, 76), (104, 77.7), (113, 73.5), (128, 72.5), (140, 72.5),
        (150, 71.5), (160, 69.6), (170, 70), (180, 69), (188, 65.5), (180, 64.5), (178, 62.5), (173, 61), (166, 60), (163, 57), (162, 54.5),
        (156.5, 51), (156, 57), (159, 61.5), (155, 59.3), (143, 59.3), (137, 54), (141, 52.5), (140, 48), (135, 43.5), (131, 42.5),
        (129.5, 41), (129.5, 36), (126.5, 34.5), (126, 37.5), (124.5, 40), (121, 39), (122, 40.8), (118, 39), (119, 37), (122.5, 37),
        (119.5, 35), (121.5, 32), (122, 29.8), (119.5, 25.5), (116.5, 23), (110.5, 21), (108, 21.5), (106, 18.5), (109, 12), (105, 8.7),
        (103, 10.5), (100.8, 13.5), (99, 10), (101, 6.5), (103.5, 1.4), (101, 3), (98.5, 8), (98.5, 13), (97.5, 16.5), (94.5, 16), (94, 19),
        (91.8, 22.3), (88.5, 21.7), (86.5, 20), (80.2, 15.5), (80.2, 13), (79.8, 10.3), (77.5, 8), (76.3, 9.8), (74.7, 14), (73, 19),
        (72.6, 21.5), (69, 22.4), (67, 24.8), (61.5, 25.2), (57.3, 25.8), (56.4, 27), (52, 27.8), (50, 30), (48, 30), (50, 26.5), (51.5, 24.5),
        (56, 26), (56.4, 24.5), (59.8, 22.5), (57.5, 19), (55, 17), (52, 16), (48.5, 14), (45, 12.8), (43.3, 12.7), (42.7, 15.5), (39.2, 21.5),
        (35, 28), (32.6, 30), (34.3, 31.3), (35.5, 33.8), (36, 36), (32, 36.2), (27.5, 37), (26.2, 39.5), (23, 40.3), (24, 38), (22, 36.5),
        (20, 39.7), (19.5, 41.8), (13.6, 45.5), (12.3, 44.5), (16, 41.5), (18.5, 40.2), (15.7, 38), (12.5, 41.8), (10.5, 43), (8.7, 44.4),
        (6.5, 43.1), (3.2, 43.3), (3, 41.8), (0.8, 41), (-0.3, 39.5), (0, 38.6), (-2, 36.8)],
    'Afrika': [(-5.9, 35.8), (-10, 29.5), (-13, 27.8), (-16.5, 22), (-17, 20.8), (-16.3, 16.5), (-17.5, 14.7), (-16.7, 12.5), (-15, 11),
        (-13.3, 9), (-11.5, 6.9), (-7.5, 4.4), (-2, 4.8), (2, 6.3), (5, 5.7), (6.1, 4.3), (8.5, 4.5), (9.6, 3.5), (9.5, 1), (8.8, -1),
        (11.8, -5), (13, -9), (13.6, -12), (11.8, -17), (14.5, -22.8), (15.3, -27), (17, -29), (18.4, -34), (20, -34.8), (25.6, -34),
        (28, -32.8), (30.8, -29.8), (32.5, -28.5), (32.6, -26), (35.5, -24), (35.5, -21.5), (34.8, -20), (36.5, -18.6), (40.5, -15),
        (40.5, -10.5), (39.3, -7), (39.2, -4.7), (41.5, -1.7), (44, 1.5), (48, 5), (51, 10.4), (51.3, 11.8), (48, 11.2), (44.5, 10.5),
        (43.2, 11.6), (42.7, 13.6), (40, 15.5), (38.5, 18), (37.2, 21), (35.7, 23.9), (34.5, 26), (32.5, 29.8), (32.3, 31.3), (29.7, 31),
        (25, 31.6), (20, 32), (19, 30.3), (15.3, 32.2), (11.3, 33.3), (10, 37), (7, 37), (3, 36.8), (-1, 35.6)],
    'Madagaskar': [(44, -25), (47, -25), (49.6, -17), (50.3, -15.3), (49.2, -12), (47, -15), (44.3, -16.5), (43.3, -22)],
    'Austrálie': [(113.5, -22), (114, -26), (115, -34), (117.8, -35), (123.5, -33.9), (129, -31.6), (132, -32), (135.5, -34.7), (137.8, -33),
        (138, -35.5), (140, -38), (143.5, -38.8), (146.3, -39.1), (150, -37.5), (151.3, -33.9), (153.6, -28.2), (153, -25), (150.5, -22.5),
        (146, -19), (145.4, -15), (143.5, -14), (142.5, -10.7), (141.5, -13), (141.6, -16.6), (139.5, -17.5), (136, -15), (137, -12),
        (132.5, -11.5), (130, -13), (129.5, -15), (127, -14), (125, -15.5), (122.2, -18), (121, -19.5), (117, -20.6)],
    'Tasmánie': [(144.6, -40.7), (148.3, -40.9), (148, -43.2), (146, -43.6)],
    'NZ sever': [(173, -34.5), (174.5, -36.5), (178.5, -37.7), (177, -39.2), (175, -41.5), (174.6, -39.8)],
    'NZ jih': [(172.7, -40.5), (174.3, -41.7), (172.8, -43.8), (171, -45.5), (169, -46.6), (166.5, -46), (168, -44), (171, -42)],
    'Japonsko': [(130, 31.5), (131.5, 31.5), (132, 33.8), (135, 33.5), (137, 34.5), (139.8, 35), (140.8, 36), (141.5, 38.5), (142, 40.5),
        (141.4, 41.4), (140, 40.5), (139.5, 38.5), (137, 37), (136, 35.6), (133, 35.5), (130.8, 34), (129.6, 33.2)],
    'Hokkaidó': [(140, 41.5), (141.2, 41.8), (143.2, 42), (145.6, 43.3), (141.6, 45.4), (141.3, 43.3), (140, 42.5)],
    'Velká Británie': [(-5.7, 50), (1.4, 51.1), (1.7, 52.7), (0, 53.5), (-1.6, 55.5), (-2, 57.6), (-4, 58.6), (-5, 58.6), (-6.2, 56.5),
        (-5, 55), (-3, 54.9), (-3.2, 53.4), (-4.6, 52.8), (-5.2, 51.7), (-3.4, 51.4)],
    'Irsko': [(-6, 52.2), (-6.2, 53.9), (-5.6, 55.2), (-7.5, 55.3), (-10, 54.2), (-10, 51.6), (-8, 51.6)],
    'Island': [(-22, 63.9), (-24, 65.5), (-22, 66.4), (-16, 66.5), (-13.5, 65), (-18, 63.4)],
    'Sumatra': [(95.3, 5.6), (97.5, 5.2), (100.4, 2.2), (104, -1), (106, -3), (105.8, -5.9), (104.5, -5.9), (102.3, -4), (100.4, -0.8), (98.7, 1.7)],
    'Borneo': [(109, 1.5), (110.5, -1.5), (111.5, -3), (114.5, -4), (116.5, -3.5), (116, 0.5), (118, 1), (119, 5), (117, 7), (115.5, 5),
        (113, 3.2), (111, 1.6)],
    'Jáva': [(105.2, -6.8), (108, -7.8), (111, -8.2), (114.5, -8.7), (114.4, -7.7), (110.5, -6.8), (108.3, -6.3), (106, -5.9)],
    'Nová Guinea': [(131, -1), (134, -1), (138, -1.6), (141, -2.6), (145.5, -5.3), (147.5, -6.2), (150, -10.3), (147, -10), (144, -7.7),
        (141, -9), (138, -8), (137.5, -5), (133, -4), (132, -2.8)],
    'Luzon': [(120, 18.5), (122, 18.5), (122.3, 16.3), (124, 13), (121, 13.8), (120, 16)],
    'Mindanao': [(122, 7), (126, 7.5), (126.5, 9), (125.5, 9.8), (123.5, 8.6)],
    'Srí Lanka': [(79.8, 8.2), (81.8, 7), (81.2, 8.5), (80.2, 9.8)],
    'Kuba': [(-85, 21.8), (-82, 23.2), (-77, 22.2), (-74.2, 20.2), (-77.5, 19.8), (-80, 21.7), (-82.5, 22.5)],
    'Hispaniola': [(-74.4, 18.4), (-72.8, 19.9), (-69.9, 19.6), (-68.4, 18.6), (-71, 18), (-72.5, 18.2)],
    'Nová země': [(52, 71.5), (57, 70.6), (68, 76.5), (60, 76.5), (55, 74)],
    'Špicberky': [(11, 78.5), (17, 76.6), (22, 77.5), (27, 79.5), (18, 80.4), (11, 79.8)],
    'Antarktida': [(-180, -77), (-160, -77), (-150, -76), (-130, -74), (-110, -74), (-100, -73), (-80, -73), (-70, -70), (-60, -64),
        (-57, -63.5), (-62, -66), (-63, -70), (-60, -75), (-45, -78), (-30, -77), (-20, -73), (-10, -71), (0, -70), (15, -70), (30, -69.5),
        (45, -67.5), (60, -67), (75, -69), (90, -66), (105, -66), (120, -66.5), (135, -66), (150, -68.5), (165, -71), (170, -72.5),
        (166, -77.5), (180, -78), (180, -90), (-180, -90)],
}



WATER = {
    'Černé moře': [(28, 41.2), (29, 41.5), (31, 41.2), (36, 41.7), (38.5, 40.9), (41.5, 41.5), (41.7, 42.5), (39, 44.2), (37.5, 45),
        (36.5, 45.3), (35, 45), (33.5, 44.5), (32.5, 45.4), (33.5, 46), (31, 46.6), (30, 45.8), (29.6, 45), (28.6, 44), (28, 43), (28, 41.7)],
    'Kaspické moře': [(47, 44.5), (47.5, 45.5), (49, 46.5), (51, 47), (53, 46.6), (53, 45.3), (51.3, 45), (51, 44.4), (52.7, 42.5), (53, 41),
        (54, 40.5), (53.8, 39), (54, 37.5), (51, 36.7), (49, 37.5), (49.5, 40.3), (48, 41.5), (47.5, 43)],
}
ISLANDS = {
    'Sicílie': [(12.4, 38), (15.6, 38.3), (15.1, 36.7)],
    'Sardinie': [(8.4, 41), (9.8, 41), (9.6, 39), (8.4, 39)],
    'Korsika': [(8.6, 43), (9.5, 42.9), (9.3, 41.4), (8.7, 41.6)],
    'Kréta': [(23.5, 35.5), (26.3, 35.3), (24.5, 35)],
    'Kypr': [(32.3, 35), (34.5, 35.6), (33.8, 34.6)],
}


def dens(poly, step=1.0):
    out = []
    for (a, b), (c, d) in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(max(abs(c - a), abs(d - b)) / step))
        out += [(a + (c - a) * i / n, b + (d - b) * i / n) for i in range(n)]
    return out


def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


Y0, Y1 = merc(LAT1), merc(LAT0)
H = int(round(W * (Y0 - Y1) / math.radians(LON1 - LON0)))


def xy(lat, lon):
    return (lon - LON0) / (LON1 - LON0) * W, (Y0 - merc(max(-85, min(85, lat)))) / (Y0 - Y1) * H


def great_circle(az, step=0.5, maxd=180):
    """Body ortodromy z Prahy s výchozím azimutem az (lat, lon), délka rozbalená (spojitá)."""
    f1, l1, th = math.radians(PRAHA[0]), math.radians(PRAHA[1]), math.radians(az)
    pts, prev = [], None
    for i in range(int(maxd / step) + 1):
        d = math.radians(i * step)
        f2 = math.asin(math.sin(f1) * math.cos(d) + math.cos(f1) * math.sin(d) * math.cos(th))
        l2 = l1 + math.atan2(math.sin(th) * math.sin(d) * math.cos(f1), math.cos(d) - math.sin(f1) * math.sin(f2))
        lon = math.degrees(l2)
        if prev is not None:
            while lon - prev > 180: lon -= 360
            while lon - prev < -180: lon += 360
        prev = lon
        pts.append((math.degrees(f2), lon))
    return pts


def inside(lat, lon, m=0.0):
    return LAT0 + m < lat < LAT1 - m and LON0 + m < lon < LON1 - m


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Liberation Sans, Arial, sans-serif" font-size="16">',
         f'<defs><clipPath id="ram"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect width="{W}" height="{H}" fill="#dbe9f7"/>', '<g clip-path="url(#ram)">']
    t = lambda x, y, s, c='#222222', size=16, w='normal', a='middle': o.append(
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{a}">{escape(s)}</text>')
    poly = lambda pts, fill, stroke: o.append('<path d="M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) +
                                               f' Z" fill="{fill}" stroke="{stroke}" stroke-width="1" stroke-linejoin="round"/>')
    # podbarvení pevnin podle podnebných pásů (svislý přechod podle zeměpisné šířky)
    stops = ''.join(f'<stop offset="{xy(lat, 0)[1] / H:.4f}" stop-color="{c}"/>' for lat, c in CLIMATE)
    o.append(f'<defs><linearGradient id="podnebi" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">{stops}</linearGradient></defs>')
    for name, p in list(LAND.items()) + list(ISLANDS.items()):
        if name == 'Antarktida': continue
        poly([xy(lat, lon) for lon, lat in dens(p)], 'url(#podnebi)', '#9c7b4f')
    for name, p in WATER.items():
        poly([xy(lat, lon) for lon, lat in dens(p)], '#dbe9f7', '#9c7b4f')
    # zeměpisná síť
    for lon in range(-60, 91, 15):
        x, _ = xy(0, lon)
        o.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H}" stroke="#7f95b8" stroke-width="{1.2 if lon == 0 else 0.6}" stroke-dasharray="3,4"/>')
        t(x + 3, H - 6, f'{abs(lon)}° {"z. d." if lon < 0 else "v. d."}' if lon else '0°', c='#5a6f92', size=12, a='start')
    for lat in range(-30, 76, 15):
        _, y = xy(lat, 0)
        o.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="#7f95b8" stroke-width="{1.2 if lat == 0 else 0.6}" stroke-dasharray="3,4"/>')
        t(4, y - 4, ('rovník' if lat == 0 else f'{abs(lat)}° {"s. š." if lat > 0 else "j. š."}'), c='#5a6f92', size=12, a='start')
    for lat, lab, lx in ((66.56, 'severní polární kruh', 590), (23.44, 'obratník Raka', 130), (-23.44, 'obratník Kozoroha', 760)):
        _, y = xy(lat, 0)
        o.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="#4f7a3a" stroke-width="1.3" stroke-dasharray="10,5"/>')
        t(lx, y - 6, lab, c='#3d6a2a', size=13, w='bold', a='start')
    # ortodromy
    for n, name, az, (la, lo) in TARGETS:
        gc = great_circle(az)
        seg = []
        for lat, lon in gc:
            if not inside(lat, lon): break
            seg.append((lat, lon))
        pts = [xy(*p) for p in seg]
        o.append('<path d="M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + '" fill="none" stroke="#c0392b" stroke-width="2.8"/>')
        tgt_in = inside(la, lo)
        if tgt_in:
            # konec u cíle
            k = min(range(len(seg)), key=lambda i: (seg[i][0] - la) ** 2 + (seg[i][1] - lo) ** 2)
            px, py = pts[k]
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="#c0392b" stroke="#ffffff" stroke-width="2"/>')
            ex, ey, lab = px, py, f'{name} {az}°'
        else:
            (x1, y1), (x2, y2) = pts[-6], pts[-1]
            a = math.atan2(y2 - y1, x2 - x1); L = 22
            o.append(f'<polygon points="{x2:.1f},{y2:.1f} {x2 - L * math.cos(a - 0.4):.1f},{y2 - L * math.sin(a - 0.4):.1f} '
                     f'{x2 - L * math.cos(a + 0.4):.1f},{y2 - L * math.sin(a + 0.4):.1f}" fill="#c0392b"/>')
            ex, ey, lab = x2, y2, f'{name} {az}°'
        LABEL_POS[name](o, ex, ey, lab)
    o.append('</g>')
    px, py = xy(*PRAHA)
    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="#1f3864" stroke="#ffffff" stroke-width="2"/>')
    # sever u Prahy
    o.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py - 60:.1f}" stroke="#1f3864" stroke-width="2"/>')
    o.append(f'<polygon points="{px:.1f},{py - 68:.1f} {px - 6:.1f},{py - 54:.1f} {px + 6:.1f},{py - 54:.1f}" fill="#1f3864"/>')
    t(px, py - 74, 'S (0°)', c='#1f3864', size=14, w='bold')
    t(px + 12, py + 22, 'Praha', c='#1f3864', size=16, w='bold', a='start')
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="#2e5597" stroke-width="2"/>')
    o.append('</svg>')
    return '\n'.join(o).encode('utf-8')


def _label(dx, dy, anchor):
    def f(o, x, y, lab):
        bw = 8.4 * len(lab) + 12
        bx = {'start': x + dx, 'end': x + dx - bw, 'middle': x + dx - bw / 2}[anchor]
        bx = max(4, min(W - bw - 4, bx)); by = max(4, min(H - 30, y + dy - 18))
        o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="24" rx="4" fill="#ffffff" fill-opacity="0.92" '
                 f'stroke="#c0392b" stroke-width="1"/>')
        o.append(f'<text x="{bx + bw / 2:.1f}" y="{by + 17:.1f}" fill="#a01f12" font-size="15" font-weight="bold" '
                 f'text-anchor="middle">{escape(lab)}</text>')
    return f


CLIMATE = [  # (zeměpisná šířka, barva) – polární bílá → mírné pásmo → subtropy → tropy zeleně
    (75.0, '#ffffff'), (66.6, '#f3f5f6'), (60.0, '#dde6cf'), (48.0, '#e2e7c3'), (36.0, '#ece1b6'),
    (26.0, '#e3e2b0'), (23.4, '#cfe2a6'), (12.0, '#b4d898'), (0.0, '#a9d38f'), (-12.0, '#b4d898'),
    (-23.4, '#cfe2a6'), (-30.0, '#e3e2b0'), (-38.0, '#e6e6c0'),
]

LABEL_POS = {   # umístění štítku vzhledem ke konci čáry (dx, dy, zarovnání)
    'USA': _label(12, 34, 'start'),
    'Austrálie': _label(-12, 34, 'end'),
    'Japonsko': _label(-14, 34, 'end'),
    'Karibik': _label(12, -14, 'start'),
    'Jihoafrická rep.': _label(14, 6, 'start'),
    'Havaj': _label(-14, 34, 'end'),
    'Argentina': _label(12, -14, 'start'),
}


TITLE = 'Mapa se středem nad Prahou – směry k otázkám c) 1–7'
DESC = ('Mapa v Mercatorově projekci (výřez od východního pobřeží Ameriky po Indii). Červené křivky jsou ortodromy – '
        'nejkratší cesty po povrchu Země („short path“, otázka c) 20) – vycházející z Prahy pod azimutem podle ČTÚ '
        '(0° = sever, 90° = východ, 180° = jih, 270° = západ). Mercatorova projekce zachovává úhly, proto v Praze svírá '
        'každá křivka se severem přesně uvedený azimut; dále se ale nejkratší cesta na této mapě jeví zakřivená. Proto '
        'se na USA míří na severozápad přes Island a Grónsko, ne „rovně na západ“, a na Havaj téměř na sever přes '
        'severní pól. Cíle mimo výřez (USA, Karibik, Argentina, Havaj, Japonsko, Austrálie) naznačuje šipka. Opačný '
        'směr (azimut + 180°) je dlouhá cesta („long path“). Pevniny jsou orientačně podbarveny podle podnebných pásů '
        '(tropy mezi obratníky zeleně, mírné pásmo, polární oblasti za polárním kruhem bíle); obrysy jsou zjednodušené.')


def generate():
    return TITLE, DESC, svg(), W, H
