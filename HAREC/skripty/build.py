# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from excerpts import X, IARU_HF, IARU_VHF, M1172, RR
from odf.opendocument import OpenDocumentText
from odf.style import (Style, TextProperties, ParagraphProperties, GraphicProperties,
                       PageLayout, PageLayoutProperties, MasterPage, FontFace, TableColumnProperties)
from odf.text import H, P, Span, LineBreak, S as Spc, A
from odf import teletype
from odf.table import Table, TableColumn, TableRow, TableCell, TableHeaderRows
from odf.style import TableProperties, TableCellProperties
import zkratky
import cept_vytah
import spektra
import sireni
import azimut
import majaky
import praxe
import praxe_q
import obrazky_elek
import pasma
import spektrum_pasma
import pasma_provoz
import mapy_prefixu
import doplnky
from odf.draw import Frame, Image as DImage

SP = sys.argv[1]  # kořen projektu (~/Desktop/HAREC)
OUT = sys.argv[2]

faq = json.load(open(f'{SP}/data/faq.json', encoding='utf-8'))

# ---------------------------------------------------------------- fixes of pdf extraction
FIX = {
    ('elektrotechnika a radiotechnika', 'a', 5): (None, '10⁶'),
    ('elektrotechnika a radiotechnika', 'a', 8): (None, 'P = I² · R'),
    ('elektrotechnika a radiotechnika', 'a', 10): (None, '5 Ω'),
    ('elektrotechnika a radiotechnika', 'a', 20): (None, '2 A'),
    ('elektrotechnika a radiotechnika', 'c', 12): (None, '0 Ω'),
    ('radiokomunikační provoz', 'f', 1): ('Česká republika:', 'OL, OK'),
}

# ---------------------------------------------------------------- source texts for automatic lookups
def readlines(p):
    return open(p, encoding='utf-8').read().split('\n')

hf = readlines(f'{SP}/zdroje/iaru/IARU_R1_HF_bandplan.txt')
vhf = readlines(f'{SP}/zdroje/iaru/IARU_R1_VHF_Handbook_V10_03.txt')
m1172 = readlines(f'{SP}/zdroje/itu/ITU-R_M.1172.txt')
ap42 = readlines(f'{SP}/zdroje/itu/RR2024_Vol2.txt')


def hf_band(lo, hi):
    """Raw lines of the IARU HF plan for segments with start freq in [lo, hi)."""
    rows = []
    for i, l in enumerate(hf):
        m = re.match(r'^\s*([\d,]+)\s+-\s+([\d,]+)\s', l)
        if m:
            f = float(m.group(1).replace(',', '.'))
            rows.append((i, f))
    idx = [i for i, f in rows if lo <= f < hi]
    a, b = min(idx), max(idx)
    # include note line immediately above first row and trailing continuation lines
    if hf[a - 1].strip() and not re.match(r'^\s*[\d,]+\s+-', hf[a - 1]):
        a -= 1
    nxt = [i for i, f in rows if i > b]
    end = nxt[0] if nxt else b + 1
    seg = hf[a:end]
    out = [l.rstrip() for l in seg if l.strip() and not re.fullmatch(r'\s*\d+(,\d)?\s*MHz\s*', l)
           and 'IARU Region 1 HF Band Plan' not in l and 'Effective from' not in l
           and 'FREQUENCY SEGMENT' not in l and 'MAX. BANDWIDTH' not in l and l.strip() != '(kHz)'
           and not re.fullmatch(r'\s*(\d+|MHz)\s*', l)]
    # drop trailing lines that belong to the next block header
    while out and re.match(r'^\s*(CW contest preferred|SSB contest preferred)\s*$', out[-1]):
        out.pop()
    return dedent(out)


def dedent(lines):
    lines = [re.sub(r'^\s*(\d+(,\d)?\s*MHz|\d+\s*$|MHz)\s{2,}', '', l) for l in lines]
    ind = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return '\n'.join(l[ind:] for l in lines)


def vhf_slice(a, b):
    out = [l.rstrip() for l in vhf[a - 1:b] if l.strip() and 'VHF Handbook' not in l and l.strip() != 'IARU-R1']
    return dedent(out)


HF_HEAD = 'FREQUENCY SEGMENT (kHz) | MAX. BANDWIDTH (Hz) | PREFERRED MODE AND USAGE'
BANDS = {
    '1.8': (IARU_HF + ' – pásmo 1,8 MHz', HF_HEAD + '\n' + hf_band(1800, 2001)),
    '3.5': (IARU_HF + ' – pásmo 3,5 MHz', HF_HEAD + '\n' + hf_band(3500, 3801)),
    '7': (IARU_HF + ' – pásmo 7 MHz', HF_HEAD + '\n' + hf_band(7000, 7201)),
    '10': (IARU_HF + ' – pásmo 10 MHz', HF_HEAD + '\n' + hf_band(10100, 10151)),
    '14': (IARU_HF + ' – pásmo 14 MHz', HF_HEAD + '\n' + hf_band(14000, 14351)),
    '18': (IARU_HF + ' – pásmo 18 MHz', HF_HEAD + '\n' + hf_band(18068, 18169)),
    '21': (IARU_HF + ' – pásmo 21 MHz', HF_HEAD + '\n' + hf_band(21000, 21451)),
    '24': (IARU_HF + ' – pásmo 24 MHz', HF_HEAD + '\n' + hf_band(24890, 24991)),
    '28': (IARU_HF + ' – pásmo 28 MHz', HF_HEAD + '\n' + hf_band(28000, 29701)),
    '50': (IARU_VHF + ' – 50–54 MHz (přepis tabulky)',
           'Frequency | Max. bandwidth | Mode | Usage\n'
           '50.000–50.100 | 500 Hz | Telegraphy exclusive (except Beacon Project) | 50.000–50.030 Synchronised Beacon Project; 50.050 CW future international centre of activity; 50.090 CW intercontinental centre of activity\n'
           '50.100–50.200 | 2700 Hz | SSB, Telegraphy | International preferred: 50.100–130 intercontinental section, 50.110 intercontinental centre of activity, 50.130–200 international section, 50.150 international centre of activity\n'
           '50.200–50.300 | 2700 Hz | SSB, Telegraphy | General usage, 50.285 for crossband\n'
           '50.300–50.400 | 2700 Hz | MGM, Narrowband, Telegraphy | 50.305 PSK centre of activity, 50.310–320 EME centre of activity, 50.320–380 MS centre of activity\n'
           '50.400–50.500 | 1000 Hz | MGM, Telegraphy | Beacons exclusive\n'
           '50.500–50.700 | – | All modes | 50.540–580 simplex FM/DV Internet voice gateways; 50.600–50.700 digital communications, 50.630 DV calling\n'
           '50.700–50.900 | 12 kHz | FM / Digital voice | 50.710–50.890 FM/DV repeater output channels\n'
           '50.900–51.200 | – | All modes | For wideband digital experiments\n'
           '51.200–51.400 | 12 kHz | FM / Digital voice | 51.210–390 FM/DV repeater input channels\n'
           '51.400–52.000 | – | All modes | 51.410–590 FM/DV simplex, 51.510 FM calling frequency, 51.810–990 FM/DV repeater output channels\n'
           '52.000–54.000 | 500 kHz | All modes | (f) where allocated nationally'),
    '144lo': (IARU_VHF + ' – 144–146 MHz, výňatek 144,000–144,500 (přepis tabulky)',
           'Frequency | Max. bandwidth | Mode | Usage\n'
           '144.000–144.025 | 2700 Hz | All mode | Satellites (downlinks only)\n'
           '144.025–144.100 | 500 Hz | Telegraphy | 144.050 centre of activity, 144.100 random MS\n'
           '144.100–144.150 | 500 Hz | Telegraphy & MGM | 144.110–144.160 CW and MGM EME\n'
           '144.150–144.400 | 2700 Hz | Telegraphy & SSB & MGM | 144.300 SSB centre of activity\n'
           '144.400–144.490 | 500 Hz | Telegraphy, MGM | Beacons exclusive\n'
           '144.491–144.493 | 500 Hz | Personal weak signal MGM beacons | Experimental MGM\n'
           '144.500– | 20 kHz | All mode | 144.500 image mode centre (SSTV, Fax), 144.600 data centre of activity, 144.750 ATV talk back'),
    '144sat': (IARU_VHF + ' – 144–146 MHz, výňatek 145,575–146,000 (přepis tabulky)',
           'Frequency | Max. bandwidth | Mode | Usage\n'
           '145.575–145.7935 | 12 kHz | FM / Digital voice | Repeater output exclusive\n'
           '145.794–145.806 | 12 kHz | FM / Digital voice | Space communication\n'
           '145.806–146.000 | 12 kHz | All mode | Satellite exclusive'),
    '432': (IARU_VHF + ' – 430–440 MHz, výňatek 432,000–433,000 (přepis tabulky)',
           'Frequency | Max. bandwidth | Mode | Usage\n'
           '432.000–432.400 | 2700 Hz | All mode | 432.050 telegraphy centre of activity, 432.200 SSB centre of activity, 432.350 microwave talkback centre of activity, 432.370 meteor scatter centre of activity\n'
           '432.400–432.490 | 500 Hz | Telegraphy, MGM | Beacons exclusive\n'
           '432.491–432.493 | 500 Hz | EMGM | Experimental MGM\n'
           '432.500–432.975 | no limit | All modes | 432.500 APRS; 432.600–432.9875 repeater input Region 1 (25 kHz spacing, 2 MHz shift)'),
}
for k, (src, txt) in BANDS.items():
    X['BAND_' + k] = (src, txt, None)


# ----- Q codes (M.1172 section I)
def qcode(code):
    code = code.strip().rstrip('?')
    end = next(i for i, l in enumerate(m1172) if 'Section II' in l)
    for i, l in enumerate(m1172[:end]):
        if re.match(r'^\s*' + code + r'\s{2,}', l):
            q, a = [], []
            for j in range(i, min(i + 14, end)):
                ln = m1172[j]
                if j > i and (re.match(r'^\s*Q[A-Z]{2}\*?\s{2,}', ln) or not ln.strip() and j > i + 1 and not m1172[j + 1].strip()):
                    break
                if not ln.strip() or 'Rec. ITU-R' in ln or re.fullmatch(r'\s*\d+\s*', ln):
                    continue
                body = re.sub(r'^\s*' + code + r'\s{2,}', ' ' * 12, ln) if j == i else ln
                ind = len(body) - len(body.lstrip())
                parts = re.split(r'\s{2,}', body.strip())
                if ind < 30 and len(parts) >= 2:
                    q.append(parts[0]); a.append(' '.join(parts[1:]))
                elif ind < 30:
                    q.append(parts[0])
                else:
                    a.append(' '.join(parts))
            join = lambda xs: re.sub(r'-\s+(?=[a-z])', '', ' '.join(xs)).replace('  ', ' ')
            return (M1172 + ', příloha 1, oddíl I – Q kód ' + code,
                    f'{code}  Question: {join(q)}\n{code}  Answer or Advice: {join(a)}', None)
    return None


# ----- miscellaneous abbreviations (M.1172 section II)
def abbr(code):
    start = next(i for i, l in enumerate(m1172) if 'Section II' in l)
    for i in range(start, len(m1172)):
        m = re.match(r'^\s*(\S+)\s{2,}(.+)$', m1172[i])
        if m and m.group(1) == code:
            txt = m.group(2).strip()
            k = i + 1
            while k < len(m1172) and 'Rec. ITU-R' not in m1172[k] and re.match(r'^\s{8,}\S', m1172[k]) and not re.match(r'^\s*\S+\s{2,}\S', m1172[k].strip() + '  x'):
                txt += ' ' + m1172[k].strip(); k += 1
            return (M1172 + ', příloha 1, oddíl II – Miscellaneous abbreviations and signals', f'{code}  {txt}', None)
    return None


# ----- Appendix 42 call sign series
ORD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
def okey(s):
    return [ORD.index(c) for c in s]

AP42 = []
st = next(i for i, l in enumerate(ap42) if 'Table of allocation of international call sign series' in l and i > 40000)
for l in ap42[st:st + 700]:
    m = re.match(r'^\s*\*?([A-Z0-9]{3})-([A-Z0-9]{3})\s+(.+?)(?:\s{2,}\(WRC.*\))?\s*$', l)
    if m:
        AP42.append((m.group(1), m.group(2), re.sub(r'\d+$', '', m.group(3)).strip()))


def ap42_lookup(answer):
    toks = re.findall(r'[A-Z0-9]{1,3}(?:\s*[–-]\s*[A-Z0-9]{1,3})?', answer.replace('vč,', ''))
    hits = []
    for t in toks:
        ab = re.split(r'\s*[–-]\s*', t)
        a, b = ab[0], ab[-1]
        cands = []
        if len(a) == 1:
            cands = [(a + 'A', a + 'Z')]
        elif a[1].isdigit() and a[0].isalpha() and not any(r[0][:2] == a[:2] for r in AP42):
            cands = [(a[0] + 'A', a[0] + 'Z')]
        else:
            cands = [(a[:2], b[:2])]
        for lo, hi in cands:
            for r in AP42:
                if okey(r[0][:2]) <= okey(hi) and okey(lo) <= okey(r[1][:2]):
                    if r not in hits:
                        hits.append(r)
    if not hits:
        return None
    return (RR + ', dodatek 42 – Table of allocation of international call sign series (výňatek)',
            '\n'.join(f'{r[0]}-{r[1]}   {r[2]}' for r in hits), None)



def p1_sub(name, subs):
    s, txt, _ = X['156_P1']
    lines = txt.split('\n')
    rows = [l for l in lines[1:-2] if any(x in l for x in subs)]
    X[name] = (s + ' (výňatek)', '\n'.join([lines[0]] + rows + lines[-2:]), None)

p1_sub('P1_7', ['7 100 – 7 200'])
p1_sub('P1_24', ['24,89'])
p1_sub('P1_50', ['50 – 52'])
p1_sub('P1_18', ['1 810', '1 850 – 1 890', '1 890 – 2 000'])
p1_sub('P1_10', ['10 100', '10 140'])
p1_sub('P1_14', ['14 000'])

# ---------------------------------------------------------------- mapping question -> excerpts / notes
PRED = 'radiokomunikační předpisy'
PROV = 'radiokomunikační provoz'
ELEK = 'elektrotechnika a radiotechnika'

M = {}   # (part, sec, n) -> list of keys
N = {}   # (part, sec, n) -> note text

def m(part, sec, n, keys, note=None):
    M[(part, sec, n)] = keys
    if note:
        N[(part, sec, n)] = note

# --- předpisy a) ITU
m(PRED, 'a', 1, ['RR1_56', '156_1a', '157_1l'])
m(PRED, 'a', 2, ['RR1_61', '156_1b'])
m(PRED, 'a', 3, ['RR25_8'])
m(PRED, 'a', 4, ['RR25_7', '156_4_2'])
m(PRED, 'a', 5, ['RR25_9B', '156_2_2'])
m(PRED, 'a', 6, ['RR5_2'])
m(PRED, 'a', 7, ['RR5_24', 'RR5_table', '156_P1'])
m(PRED, 'a', 8, ['RR25_3', '156_8_2'])
m(PRED, 'a', 9, ['RR25_5', '157_4'])
m(PRED, 'a', 10, ['RR19_68', 'RR19_29'])
m(PRED, 'a', 11, ['RR19_46', '155_4_2', '155_1p'])
m(PRED, 'a', 12, ['RR19_29', 'RR19_33'])
m(PRED, 'a', 13, ['RR5_24', 'RR5_28'])
m(PRED, 'a', 14, ['RR_AP42_OK', '155_9_2'],
  'Dodatek 42 RR uvádí pro ČR souvislou sérii OKA–OLZ, tj. OKA až OKZ a OLA až OLZ.')
m(PRED, 'a', 15, ['RR25_10', 'RR1_56'])
m(PRED, 'a', 16, ['RR5_28', '156_P1'])
# --- předpisy b) CEPT
m(PRED, 'b', 1, ['T6102_intro', 'T6102_A1'])
m(PRED, 'b', 2, ['T6101_A1_2', '156_3_1'])
m(PRED, 'b', 3, ['156_2_2', 'T6102_rec'],
  'Doporučení T/R 61-01 samo konkrétní lhůtu neuvádí („temporary stays“); tříměsíční hranici stanoví § 2 odst. 2 písm. b) vyhl. 156/2005 Sb. a od ní se odvíjí i bod 3 doporučení T/R 61-02 (pobyt delší než tři měsíce → národní oprávnění na základě HAREC).')
m(PRED, 'b', 4, ['T6101_A1_2'])
m(PRED, 'b', 5, ['T6101_rec'])
m(PRED, 'b', 6, ['T6101_A1_2'])
m(PRED, 'b', 7, ['T6101_A1_1'])
m(PRED, 'b', 8, ['T6102_intro', 'T6102_morse'],
  'Přehled zemí, které stále vyžadují znalost telegrafie, je uveden v poznámkách k tabulkám přílohy 2 a 4 doporučení T/R 61-02.')
m(PRED, 'b', 9, ['T6102_rec'])
m(PRED, 'b', 10, ['T6101_A1_1'])
m(PRED, 'b', 11, ['T6101_A1_1'])
m(PRED, 'b', 12, ['T6101_rec', 'T6101_A1_1'])
m(PRED, 'b', 13, ['T6102_intro', 'T6102_rec'])
m(PRED, 'b', 14, ['T6102_A1', '157_7', 'Z26_4'])
m(PRED, 'b', 15, ['T6101_A1_3', 'T6101_A2_CZ'])
m(PRED, 'b', 16, ['T6101_A1_1', '156_1p'],
  'Doporučení výslovně o klubových stanicích nehovoří. Licence CEPT je vázána na konkrétního držitele (jméno a adresa, „non-residents only“), proto ji nelze uplatnit pro klubovou stanici, kterou podle § 1 písm. p) vyhl. 156/2005 Sb. používá více osob – jde o výklad ČTÚ.')
# --- předpisy c) ČR
m(PRED, 'c', 1, ['Z17_1', 'Z26_12', '156_2_1'])
m(PRED, 'c', 2, ['156_5_2'],
  'Povinnost vést staniční deník stanoví vyhláška pouze pro klubové stanice (§ 5 odst. 2); pro stanice jednotlivců ji neukládá.')
m(PRED, 'c', 3, ['156_9_3'])
m(PRED, 'c', 4, ['156_3_2'])
m(PRED, 'c', 5, ['156_7_2'])
m(PRED, 'c', 6, ['156_7_2'])
m(PRED, 'c', 7, ['156_7_2'])
m(PRED, 'c', 8, ['156_7_3'])
m(PRED, 'c', 9, ['156_4_3'])
m(PRED, 'c', 10, ['156_8_1', '155_1p', 'RR25_1'])
m(PRED, 'c', 11, ['156_1j', '156_5_1', '156_1h'])
m(PRED, 'c', 12, ['156_4_4'])
m(PRED, 'c', 13, ['156_1k'])
m(PRED, 'c', 14, ['156_1l'])
m(PRED, 'c', 15, ['RR25_1'])
m(PRED, 'c', 16, ['156_4_2', 'P1_7', '156_4_4'],
  'Kmitočet 7 105 kHz leží v pásmu 7 100–7 200 kHz, kde od 30. 3. 2009 platí status P (pozn. VII). Odpověď 750 W odpovídá obecnému limitu třídy A dle § 4 odst. 2 písm. a); zvýšený výkon podle § 4 odst. 4 se vztahuje jen na mezinárodní radioamatérský závod (srov. otázku c) 12).')
m(PRED, 'c', 17, ['156_4_2', 'P1_24'])
m(PRED, 'c', 18, ['P1_50', '156_4_2'],
  'Pásmo 50–52 MHz má status NIB s poznámkou V) – povolený výstupní výkon 25 W; nižší výkon daný statusem má přednost (§ 4 odst. 2 písm. a): „pokud status uvedený v tabulce nestanoví výkon nižší“), a to i během závodu.')
m(PRED, 'c', 19, ['156_4_2', 'P1_18'], 'Kmitočet 1 820 kHz leží v pásmu 1 810–1 850 kHz se statusem P → platí obecný limit 750 W.')
m(PRED, 'c', 20, ['P1_18'], 'Kmitočet 1 900 kHz leží v pásmu 1 890–2 000 kHz se statusem NIB a poznámkou VI) – povolený výstupní výkon 10 W.')
m(PRED, 'c', 21, ['Z18_3'])
m(PRED, 'c', 22, ['156_8_3'])
m(PRED, 'c', 23, ['156_P2_1', 'RR_AP1'])
m(PRED, 'c', 24, ['156_9_4'])
m(PRED, 'c', 25, ['P1_10', 'BAND_10', 'IARU_HF_sideband'],
  'Úsek 10 140–10 150 kHz připouští pouze druhy provozu J1D, J2D, F1D, G1D (pozn. III) – tedy žádný fonický provoz; v pásmu 10 MHz fone vůbec není.')
m(PRED, 'c', 26, ['P1_14', 'IARU_HF_sideband'],
  '14,35 MHz je horní okraj pásma 14 000–14 350 kHz. Signál USB leží nad nastaveným kmitočtem, takže by vysílání zasahovalo mimo pásmo.')
m(PRED, 'c', 27, ['156_4_5'])
m(PRED, 'c', 28, ['156_5_1'])
m(PRED, 'c', 29, ['156_8_1', 'RR25_1', '155_1p'])
m(PRED, 'c', 30, ['157_4', 'RR25_5', 'T6102_intro'],
  'Zkouška z telegrafie se v rámci HAREC/NOVICE koná jen na žádost žadatele (§ 4 odst. 3 písm. c) vyhl. 157/2005 Sb.).')
m(PRED, 'c', 31, ['156_9_1'], 'Pásmo 6 m (50–52 MHz) spadá do rozsahu 30–235 MHz; výkon je omezen na 25 W (NIB V), proto platí řádek „≤ 25 W“.')
m(PRED, 'c', 32, ['156_9_1'])
m(PRED, 'c', 33, ['156_9_1'])
m(PRED, 'c', 34, ['156_9_1'])
m(PRED, 'c', 35, ['BAND_1.8', 'IARU_HF_sideband'],
  'Nejnižší doporučené nastavení pro LSB je 1 843 kHz; při LSB na 1 840 kHz by signál zasahoval do úzkopásmového úseku pod 1 840 kHz.')
m(PRED, 'c', 36, ['P1_10', 'BAND_10'])
m(PRED, 'c', 37, ['156_5_2'])
m(PRED, 'c', 38, ['155_5_2', 'RR25_8'])
m(PRED, 'c', 39, ['155_5_2'])
m(PRED, 'c', 40, ['156_8_2'])
m(PRED, 'c', 41, ['156_9_4'])
m(PRED, 'c', 42, ['156_P2_1'])
m(PRED, 'c', 43, ['156_6'])
m(PRED, 'c', 44, ['156_4_6'])
m(PRED, 'c', 45, ['155_9_3j'])
m(PRED, 'c', 46, ['155_9_3j'])
m(PRED, 'c', 47, ['P1_18'])
m(PRED, 'c', 48, ['P1_50'])

# --- provoz a) band plans
m(PROV, 'a', 1, ['156_4_3'])
for n, b in [(2, '1.8'), (3, '1.8'), (4, '1.8'), (5, '3.5'), (6, '3.5'), (7, '3.5'), (8, '3.5'),
             (9, '7'), (10, '7'), (11, '7'), (12, '10'), (13, '10'), (14, '14'), (15, '14'), (16, '14'),
             (17, '18'), (18, '18'), (19, '18'), (20, '21'), (21, '21'), (22, '21'), (23, '24'), (24, '24'),
             (25, '24'), (26, '28'), (27, '28'), (28, '28'), (29, '28'), (30, '50'), (31, '50'), (32, '50'),
             (33, '144lo'), (34, '144lo'), (35, '144sat'), (36, '144lo'), (37, '432'), (38, '432'), (39, '432'), (40, '432')]:
    m(PROV, 'a', n, ['BAND_' + b, '156_4_3'])
m(PROV, 'a', 12, ['BAND_10', 'P1_10'])
m(PROV, 'a', 41, ['IARU_HF_contest'],
  'Pásma 30, 17 a 12 m (10, 18 a 24 MHz) byla amatérské službě přidělena Světovou administrativní radiokomunikační konferencí WARC-79 – odtud název.')

# --- provoz c) operating skills
m(PROV, 'c', 8, ['155_4_2'])
m(PROV, 'f', 73, [], 'Dodatek 42 RR přiděluje celou sérii BAA–BZZ Čínské lidové republice; prefix BV se v radioamatérském provozu používá pro Tchaj-wan.')
m(PROV, 'c', 9, ['RR32', '155_4_2'])
m(PROV, 'c', 10, ['T6101_A1_2', 'T6101_A2_CZ', '156_7_2'])
m(PROV, 'c', 13, [], None)
m(PROV, 'c', 24, ['IARU_HF_contest'])
m(PROV, 'c', 25, ['156_1l'])
m(PROV, 'c', 26, ['IARU_HF_def'])
m(PROV, 'c', 28, ['IARU_HF_def'])

NOTE_NOLAW = {
    (PROV, 'c'): 'Otázky na azimuty, reporty, provozní zvyklosti a techniku provozu vycházejí z radioamatérské praxe; právní předpis je výslovně neupravuje. U otázek, kde existuje opora v předpisu, je výňatek uveden.',
    (PROV, 'e'): 'Většina těchto zkratek je radioamatérský „jargon“, který není upraven právním předpisem. Kde se zkratka vyskytuje v doporučení ITU-R M.1172 (oddíl II – Miscellaneous abbreviations and signals), je uveden výňatek.',
    (PROV, 'd'): 'Q kódy jsou mezinárodně definovány v doporučení ITU-R M.1172 (na něj odkazuje RR č. 19.48). Definici Q-kódu obsahuje též § 1 písm. p) vyhl. 155/2005 Sb. U každého kódu je uveden výňatek z M.1172 (anglicky: otázka / odpověď).',
    (PROV, 'f'): 'Série mezinárodních volacích značek přiděluje ITU v dodatku 42 Radiokomunikačního řádu (RR č. 19.29). Dodatek 42 uvádí bloky přidělené státům; konkrétní prefixy pro jednotlivá území (např. Skotsko GM, Korsika TK) určují národní správy v rámci svého bloku. U každé otázky je uveden příslušný řádek dodatku 42.',
    (ELEK, None): 'Otázky z elektrotechniky a radiotechniky ověřují technické znalosti (fyzika, elektronika, šíření vln, bezpečnost). Nejsou zdůvodnitelné výňatky ze zákonů a vyhlášek, proto jsou uvedeny pouze otázky a správné odpovědi. (Bezpečnostní otázky v oddílu j) vycházejí z technických norem ČSN, ne z předpisů o elektronických komunikacích.)',
}

QRJ_NOTE = 'Pozor: v aktuálním znění doporučení ITU-R M.1172 má QRJ jiný (námořní) význam. Význam „Nemohu vás přijímat, vaše signály jsou velmi slabé“ je historický význam používaný v radioamatérské praxi.'

# ---------------------------------------------------------------- ODT
doc = OpenDocumentText()
doc.fontfacedecls.addElement(FontFace(name='Liberation Serif', fontfamily='Liberation Serif', fontfamilygeneric='roman'))
doc.fontfacedecls.addElement(FontFace(name='Liberation Sans', fontfamily='Liberation Sans', fontfamilygeneric='swiss'))
doc.fontfacedecls.addElement(FontFace(name='Liberation Mono', fontfamily='Liberation Mono', fontfamilygeneric='modern', fontpitch='fixed'))

pl = PageLayout(name='pl')
pl.addElement(PageLayoutProperties(pagewidth='21cm', pageheight='29.7cm', margintop='1.8cm', marginbottom='1.8cm', marginleft='2cm', marginright='2cm'))
doc.automaticstyles.addElement(pl)
doc.masterstyles.addElement(MasterPage(name='Standard', pagelayoutname=pl))


def pstyle(name, parent=None, family='paragraph', tp=None, pp=None, cls=None, **kw):
    s = Style(name=name, family=family, **({'parentstylename': parent} if parent else {}), **kw)
    if tp: s.addElement(TextProperties(**tp))
    if pp: s.addElement(ParagraphProperties(**pp))
    doc.styles.addElement(s)
    return s

std = pstyle('Standard', tp={'fontname': 'Liberation Serif', 'fontsize': '10.5pt'}, pp={'margintop': '0cm', 'marginbottom': '0.12cm'})
h1 = pstyle('Heading 1', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '18pt', 'fontweight': 'bold', 'color': '#1f3864'},
            pp={'margintop': '0.6cm', 'marginbottom': '0.3cm', 'breakbefore': 'page', 'keepwithnext': 'always'}, defaultoutlinelevel='1')
h2 = pstyle('Heading 2', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '14pt', 'fontweight': 'bold', 'color': '#2e5597'},
            pp={'margintop': '0.5cm', 'marginbottom': '0.2cm', 'keepwithnext': 'always'}, defaultoutlinelevel='2')
title = pstyle('Title', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '24pt', 'fontweight': 'bold', 'color': '#1f3864'},
               pp={'textalign': 'center', 'margintop': '4cm', 'marginbottom': '0.5cm'})
subtitle = pstyle('Subtitle', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '13pt', 'color': '#444444'},
                  pp={'textalign': 'center', 'marginbottom': '0.3cm'})
qst = pstyle('Otazka', 'Standard', tp={'fontweight': 'bold', 'fontsize': '11pt'},
             pp={'margintop': '0.35cm', 'marginbottom': '0.08cm', 'keepwithnext': 'always', 'bordertop': '0.5pt solid #b4c6e7', 'paddingtop': '0.15cm'})
ans = pstyle('Odpoved', 'Standard', tp={'color': '#1e6b1e', 'fontsize': '10.5pt'},
             pp={'marginleft': '0.4cm', 'marginbottom': '0.12cm', 'keepwithnext': 'always'})
src = pstyle('Zdroj', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '8.5pt', 'fontweight': 'bold', 'color': '#7f4f00'},
             pp={'marginleft': '0.8cm', 'margintop': '0.12cm', 'marginbottom': '0.02cm', 'keepwithnext': 'always'})
exc = pstyle('Vynatek', 'Standard', tp={'fontsize': '9.5pt', 'color': '#333333'},
             pp={'marginleft': '0.8cm', 'marginbottom': '0.05cm', 'backgroundcolor': '#f6f3ea', 'borderleft': '2pt solid #c9a85c', 'paddingleft': '0.2cm'})
mono = pstyle('VynatekMono', 'Standard', tp={'fontname': 'Liberation Mono', 'fontsize': '7pt', 'color': '#333333'},
              pp={'marginleft': '0.8cm', 'marginbottom': '0.05cm', 'backgroundcolor': '#f6f3ea', 'borderleft': '2pt solid #c9a85c', 'paddingleft': '0.2cm'})
trn = pstyle('Preklad', 'Standard', tp={'fontsize': '9pt', 'fontstyle': 'italic', 'color': '#555555'},
             pp={'marginleft': '0.8cm', 'marginbottom': '0.05cm', 'paddingleft': '0.25cm'})
note = pstyle('Poznamka', 'Standard', tp={'fontsize': '9.5pt', 'color': '#7a1f1f'},
              pp={'marginleft': '0.8cm', 'margintop': '0.1cm', 'marginbottom': '0.1cm'})
info = pstyle('Info', 'Standard', tp={'fontsize': '10pt', 'fontstyle': 'italic', 'color': '#444444'},
              pp={'marginbottom': '0.2cm', 'backgroundcolor': '#eef3fb', 'padding': '0.2cm'})
bold = Style(name='B', family='text'); bold.addElement(TextProperties(fontweight='bold')); doc.styles.addElement(bold)
lbl = Style(name='Lbl', family='text'); lbl.addElement(TextProperties(fontweight='bold', color='#1e6b1e')); doc.styles.addElement(lbl)


def para(style, text, label=None):
    p = P(stylename=style)
    if label:
        p.addElement(Span(stylename=lbl, text=label))
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        if i:
            p.addElement(LineBreak())
        teletype.addTextToElement(p, ln)
    doc.text.addElement(p)


def add_excerpt(key):
    e = X[key]
    s, t, tr = e
    para(src, '§ ' + s if False else s)
    if key.startswith('BAND_'):
        t = '\n'.join(' | '.join(re.split(r'\s{2,}', l.strip())) if re.match(r'^\s*([\d,]+\s+-\s+[\d,]+|\d{2,3}[.,]\d{3,4})(\s|$)', l) or '|' in l
                      else '      ' + re.sub(r'\s{2,}', ' · ', l.strip()) for l in t.split('\n'))
    para(exc, t)
    if tr:
        para(trn, 'Pracovní překlad (neoficiální): ' + tr)


# ---- title page
doc.text.addElement(P(stylename=title, text='Zkušební otázky HAREC – třída A'))
doc.text.addElement(P(stylename=subtitle, text='Otázky a správné odpovědi ČTÚ s výňatky z předpisů, které je zdůvodňují'))
doc.text.addElement(P(stylename=subtitle, text='Sestaveno 11. 11. 2026, aktualizováno 27. 11. 2026'))

doc.text.addElement(H(outlinelevel=1, stylename=h1, text='Jak probíhá zkouška'))
para(std, 'Zkoušku pořádá zkušební komise Českého telekomunikačního úřadu pro amatérskou radiokomunikační službu se sídlem v Praze '
     '(komise má nejméně tři členy – předsedu, místopředsedu a tajemníka; § 5 vyhl. 157/2005 Sb., čl. 2 a 3 Zkušebního řádu ČTÚ). '
     'Přihláška se podává elektronicky přes ePortál ČTÚ (nebo na tištěném formuláři) nejpozději 20 dní před požadovaným termínem; '
     'správní poplatek za zkoušku včetně vydání průkazu je 600 Kč a platí se předem. Fotografie se u radioamatérských průkazů '
     'nepožaduje, uchazeč mladší 18 let přikládá souhlas zákonných zástupců. Termíny vyhlašuje ČTÚ na svém webu nejméně 30 dní '
     'předem; písemnou pozvánku s datem, časem a místem pošle nejméně 14 dní před zkouškou (nejpozději do 3 měsíců od podání '
     'přihlášky). Zkouška se koná zpravidla v sídle ČTÚ v Praze a je neveřejná.')
for t in [
    'Na začátku tajemník ověří totožnost (vzít s sebou průkaz totožnosti) a předseda seznámí uchazeče s průběhem a hodnocením zkoušky. '
    'Na pozdní příchod (nejvýše 15 minut) se hledí individuálně.',
    'Písemný test je papírový, všichni uchazeči jej píší současně pod dozorem. Obsahuje 80 otázek: 20 z radiokomunikačních předpisů, '
    '40 z radiokomunikačního provozu a 20 z elektrotechniky a radiotechniky. Ke každé otázce jsou 3 odpovědi, správná je vždy jedna; '
    'otázka se počítá jako správná, je-li označena jen jedna – ta správná odpověď.',
    'Na test je nejvýše 60 minut. Povoleny jsou pouze psací potřeby – žádná kalkulačka, mobilní telefon ani jiné pomůcky; při jejich '
    'použití nebo opisování je test odebrán a hodnocen „neprospěl“.',
    'Každý předmět se hodnotí zvlášť: pro „prospěl“ je třeba alespoň 16 správných odpovědí z 20 (předpisy, elektrotechnika) a 32 ze 40 '
    '(provoz), tj. 80 %. Kdo neprospěje byť z jednoho předmětu, neprospěl celkově.',
    'Zkouška z telegrafie se pro HAREC nevyžaduje; na vlastní žádost lze po písemném testu vykonat i praktickou zkoušku z telegrafie.',
    'Test komise vyhodnotí ještě týž den a výsledek zapíše do protokolu. Při úspěchu tajemník vyhotoví průkaz HAREC operátora třídy A '
    'hned na místě; jeho platnost je neomezená. Při neúspěchu lze na žádost (bez nového poplatku) opakovat písemný test nejdříve po '
    '60 dnech, znovu ze všech předmětů; zkoušku je nutné složit do 6 měsíců od prvního písemného testu.',
    'Průkaz sám k vysílání neopravňuje: potom se podává žádost o individuální oprávnění k provozu stanice (formulář 13N na ePortálu ČTÚ, '
    'za správní poplatek), v níž lze navrhnout volací značku – ČTÚ ji přidělí, pokud je volná.',
]:
    para(std, '• ' + t)
para(info, 'Zdroje: vyhláška č. 157/2005 Sb. (§ 3, 5 a 6), Zkušební řád ČTÚ čj. ČTÚ-8 805/2023-613 účinný od 1. 4. 2023 '
     '(čl. 2–15), materiál ČTÚ k otázkám 05/2026 (vyhodnocení písemné zkoušky), stránky ČTÚ „Přihláška ke zkoušce“ '
     'a „Amatérská radiokomunikační služba“ (ověřeno 14. 11. 2026). Postup se může změnit – před přihlášením ověřte aktuální '
     'informace na ctu.gov.cz.')

intro = H(outlinelevel=1, stylename=h1, text='Úvod a použité zdroje')
doc.text.addElement(intro)
for t in [
    'Dokument obsahuje kompletní soubor otázek pro písemný test k průkazu HAREC operátora třídy A (podle § 2 písm. h) vyhl. č. 157/2005 Sb.), jak je zveřejňuje Český telekomunikační úřad – vložka č. 1 k čj. 26 273/2025-613, soubor „amaterske_zkousky_faq_05-2026.pdf“. U každé otázky je uvedena správná odpověď a – kde je to možné – doslovný výňatek z předpisu, který odpověď zdůvodňuje.',
    'Ve zkušebním testu jsou ke každé otázce nabídnuty tři odpovědi, z nichž jedna je správná (§ 5 odst. 3 vyhl. 157/2005 Sb.). Zde je uvedena jen ta správná.',
    'Výňatky z mezinárodních předpisů (ITU, CEPT, IARU) jsou ponechány v anglickém originálu; u předpisů ITU a CEPT je připojen pracovní (neoficiální) překlad. Poznámky označené „Poznámka“ jsou vysvětlující komentáře sestavitele, nejsou součástí předpisů ani materiálu ČTÚ.',
    'Na konci dokumentu je příloha se stručným českým výtahem z doporučení CEPT T/R 61-01 (licence CEPT) a T/R 61-02 (HAREC) a jako poslední příloha tahák vzorců a čísel k výpočtovým otázkám.',
    'Upozornění: Rozdělení kmitočtových úseků v otázkách oddílu „Rozvrh kmitočtů“ formuloval ČTÚ; aktuální kmitočtové plány IARU Region 1 se v některých detailech mohou lišit (plány se průběžně aktualizují). Pro zkoušku platí odpovědi ČTÚ.',
]:
    para(std, t)
doc.text.addElement(H(outlinelevel=2, stylename=h2, text='Zdroje (staženo 11. 11. 2026, aktuálnost ověřena 14. 11. 2026)'))
for t in [
    'ČTÚ: Otázky včetně správných odpovědí pro písemné testy zkoušek … amatérské radiokomunikační služby, verze 05/2026 – https://ctu.gov.cz/sites/default/files/obsah/Prukazy/amaterske_zkousky_faq_05-2026.pdf',
    'Zákon č. 127/2005 Sb., o elektronických komunikacích, v aktuálním znění – https://www.zakonyprolidi.cz/cs/2005-127',
    'Vyhláška č. 155/2005 Sb., o způsobu tvorby volacích značek, identifikačních čísel a kódů …, aktuální znění od 23. 8. 2023 – https://www.zakonyprolidi.cz/cs/2005-155',
    'Vyhláška č. 156/2005 Sb., o technických a provozních podmínkách amatérské radiokomunikační služby (bez novel, znění od 1. 5. 2005) – https://www.zakonyprolidi.cz/cs/2005-156',
    'Vyhláška č. 157/2005 Sb., o náležitostech přihlášky ke zkoušce … a druzích průkazů odborné způsobilosti, aktuální znění od 23. 8. 2023 – https://www.zakonyprolidi.cz/cs/2005-157',
    'ITU Radio Regulations, edition 2024 (Vol. 1 – Articles, Vol. 2 – Appendices) – https://www.itu.int/pub/R-REG-RR-2024',
    'Recommendation ITU-R M.1172 – Miscellaneous abbreviations and signals – https://www.itu.int/rec/R-REC-M.1172',
    'Zkušební řád ČTÚ, čj. ČTÚ-8 805/2023-613, účinný od 1. 4. 2023 – https://ctu.gov.cz/sites/default/files/obsah/zkusebni-rad-komisi-03-2023.pdf',
    'ČTÚ – Přihláška ke zkoušce (poplatek, termíny, místo) – https://ctu.gov.cz/ziskani-prukazu-odborne-zpusobilosti-na-zaklade-zkousky',
    'CEPT Recommendation T/R 61-01 (CEPT Radio Amateur Licence), edition 18 October 2024 – https://docdb.cept.org/document/925',
    'CEPT Recommendation T/R 61-02 (HAREC), edition 16 February 2024 – https://docdb.cept.org/document/926',
    'IARU Region 1 HF Band Plan, effective from 16 Oct 2020 – https://www.iaru-r1.org/reference/band-plans/',
    'IARU Region 1 VHF Managers Handbook v10.03 (02/2026) – https://www.iaru-r1.org/wp-content/uploads/2026/02/VHF_Handbook_V10_03_final.pdf',
]:
    para(std, '• ' + t)

# ---- styly obrázků; mapy prefixů (add_prefix_maps) se vkládají před oddíl provoz f)
fig = pstyle('Obrazek', 'Standard', pp={'textalign': 'center', 'margintop': '0.05cm', 'marginbottom': '0.05cm', 'keepwithnext': 'always'})
h2p = pstyle('Heading 2 nova strana', 'Heading 2', pp={'breakbefore': 'page'})


def add_prefix_maps(fsec, h3, h3p):
    """Kapitola s mapami prefixů – vkládá se těsně před oddíl provoz f)."""
    doc.text.addElement(H(outlinelevel=2, stylename=h2p, text=mapy_prefixu.TITLE))
    para(info, mapy_prefixu.INTRO)
    fqs = []
    for it in fsec['items']:
        fq, fa = FIX.get((PROV, 'f', it['n']), (None, None))
        fqs.append((it['n'], fq or it['q'], fa or it['a']))
    for j, (mtitle, mdata, mw, mh) in enumerate(mapy_prefixu.generate(fqs, f'{SP}/zdroje/geo/ne_50m_admin_0_countries.geojson'), 1):
        doc.text.addElement(H(outlinelevel=3, stylename=h3 if j == 1 else h3p, text=mtitle))
        href = doc.addPicture(f'Pictures/mapa_prefixu{j}.svg', 'image/svg+xml', mdata)
        p = P(stylename=fig)
        fr = Frame(width='17cm', height=f'{17 * mh / mw:.2f}cm', anchortype='as-char', name=f'mapa_prefixu{j}')
        fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
        p.addElement(fr); doc.text.addElement(p)

# ---- seznam zkratek
def tstyle(name, family, **props):
    st = Style(name=name, family=family)
    if family == 'table': st.addElement(TableProperties(**props))
    elif family == 'table-column': st.addElement(TableColumnProperties(**props))
    else: st.addElement(TableCellProperties(**props))
    doc.automaticstyles.addElement(st)
    return st

tab_s = tstyle('TabZkr', 'table', width='17cm', align='left', margintop='0.1cm', marginbottom='0.3cm')
cell_s = tstyle('TabZkrCell', 'table-cell', padding='0.06cm', border='0.5pt solid #b4c6e7')
cell_dig = tstyle('TabZkrCellDig', 'table-cell', padding='0.06cm', border='0.5pt solid #b4c6e7', backgroundcolor='#fff59d')
head_s = tstyle('TabZkrHead', 'table-cell', padding='0.06cm', border='0.5pt solid #b4c6e7', backgroundcolor='#dfe8f6')
tcell = pstyle('TabText', 'Standard', tp={'fontsize': '9pt'}, pp={'marginbottom': '0cm'})
tcode = pstyle('TabZkratka', 'Standard', tp={'fontsize': '9pt', 'fontweight': 'bold', 'fontname': 'Liberation Sans'}, pp={'marginbottom': '0cm'})
thead = pstyle('TabHlavicka', 'Standard', tp={'fontsize': '9pt', 'fontweight': 'bold', 'fontname': 'Liberation Sans'}, pp={'marginbottom': '0cm'})
h3 = pstyle('Heading 3', 'Standard', tp={'fontname': 'Liberation Sans', 'fontsize': '11.5pt', 'fontweight': 'bold', 'color': '#2e5597'},
            pp={'margintop': '0.35cm', 'marginbottom': '0.15cm', 'keepwithnext': 'always'}, defaultoutlinelevel='3')
h3p = pstyle('Heading 3 nova strana', 'Heading 3', pp={'breakbefore': 'page'})
_ncol = [0]
praxe_s = pstyle('Praxe', 'Standard', tp={'fontsize': '9.5pt', 'color': '#1f3864'}, pp={'marginleft': '0.8cm', 'margintop': '0.08cm', 'marginbottom': '0.1cm', 'backgroundcolor': '#eef3fb', 'padding': '0.12cm'})
lblp = Style(name='LblPraxe', family='text'); lblp.addElement(TextProperties(fontweight='bold', color='#2e5597')); doc.styles.addElement(lblp)
bullet = pstyle('Odrazka', 'Standard', pp={'marginleft': '0.5cm', 'textindent': '-0.3cm', 'marginbottom': '0.08cm'})


def table(widths, header, rows, styles, hl=None):
    _ncol[0] += 1
    t = Table(name=f'Zkratky{_ncol[0]}', stylename=tab_s)
    for i, w in enumerate(widths):
        cs = tstyle(f'TabZkr{_ncol[0]}c{i}', 'table-column', columnwidth=w)
        t.addElement(TableColumn(stylename=cs))
    hr = TableHeaderRows(); r = TableRow()
    for h in header:
        c = TableCell(stylename=head_s); c.addElement(P(stylename=thead, text=h)); r.addElement(c)
    hr.addElement(r); t.addElement(hr)
    for row in rows:
        r = TableRow()
        cst = cell_dig if hl and hl(row) else cell_s
        for val, ps in zip(row, styles):
            c = TableCell(stylename=cst); p = P(stylename=ps); teletype.addTextToElement(p, val); c.addElement(p); r.addElement(c)
        t.addElement(r)
    doc.text.addElement(t)


doc.text.addElement(H(outlinelevel=1, stylename=h1, text='Seznam zkratek'))
para(std, zkratky.INTRO)
for i, (atitle, anote, arows, emis) in enumerate(zkratky.build_rows(faq), 1):
    doc.text.addElement(H(outlinelevel=2, stylename=h2, text=f'{i}. {atitle}'))
    if anote and not emis:
        para(info, anote)
    table(['2.6cm', '12.0cm', '2.4cm'], ['Zkratka', 'Význam', 'Otázka'], arows, [tcode, tcell, tcell],
          hl=(lambda r: r[0] in zkratky.DIGITAL) if emis else None)
    if emis:
        para(info, zkratky.DIGITAL_NOTE)
    if emis:
        etabs = zkratky.emission_table(f'{SP}/zdroje/predpisy_cz/2005-156.txt')
        doc.text.addElement(H(outlinelevel=3, stylename=h3, text='Označení tříd vysílání'))
        para(info, zkratky.EMISSION_NOTE)
        table(['1.6cm', '15.4cm'], ['Třída', 'Rozpis znaků (příloha 2 vyhl. 156/2005 Sb.) – typické použití'],
              [(c, zkratky.decode(c, etabs) + (' – ' + u if u else '')) for c, u in zkratky.EMISSIONS], [tcode, tcell],
              hl=lambda r: r[0][2] in 'BD')

# ---- spektra druhů provozu (za seznamem zkratek)
cap = pstyle('Popisek', 'Standard', tp={'fontsize': '9.5pt', 'color': '#333333'}, pp={'marginbottom': '0.35cm'})
doc.text.addElement(H(outlinelevel=2, stylename=h2p, text=f'{i + 1}. Druhy provozu ve spektru – kde leží modulace vzhledem k nosné'))
para(info, spektra.INTRO)
for j, (stitle, sdesc, sdata) in enumerate(spektra.generate(), 1):
    doc.text.addElement(H(outlinelevel=3, stylename=h3, text=stitle))
    href = doc.addPicture(f'Pictures/spektrum{j:02d}.svg', 'image/svg+xml', sdata)
    p = P(stylename=fig)
    fr = Frame(width='17cm', height=f'{17 * spektra.H / spektra.W:.2f}cm', anchortype='as-char', name=f'spektrum{j}')
    fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
    p.addElement(fr); doc.text.addElement(p)
    para(cap, sdesc)

# ---- šíření rádiových vln (za spektry)
doc.text.addElement(H(outlinelevel=2, stylename=h2p, text=f'{i + 2}. Šíření rádiových vln'))
para(info, sireni.INTRO)
for j, (stitle, sdesc, sdata, sw, sh) in enumerate(sireni.generate(), 1):
    doc.text.addElement(H(outlinelevel=3, stylename=h3, text=stitle))
    href = doc.addPicture(f'Pictures/sireni{j:02d}.svg', 'image/svg+xml', sdata)
    p = P(stylename=fig)
    fr = Frame(width='17cm', height=f'{17 * sh / sw:.2f}cm', anchortype='as-char', name=f'sireni{j}')
    fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
    p.addElement(fr); doc.text.addElement(p)
    para(cap, sdesc)

PART_TITLES = {PRED: 'Část 1 – Radiokomunikační předpisy', PROV: 'Část 2 – Radiokomunikační provoz', ELEK: 'Část 3 – Elektrotechnika a radiotechnika'}

stats = {'q': 0, 'with': 0}
for part in faq:
    pt = part['title']
    doc.text.addElement(H(outlinelevel=1, stylename=h1, text=PART_TITLES[pt]))
    if part['dist']:
        para(info, 'Test z této části obsahuje celkem ' + str(part['total']) + ' otázek, vybraných z oddílů takto: ' +
             ', '.join(f'{l}) {c}' for l, c in part['dist']) + '.')
    if (pt, None) in NOTE_NOLAW:
        para(info, NOTE_NOLAW[(pt, None)])
    seen = set()
    for sec in part['sections']:
        lab = sec['label']
        if pt == PROV and lab == 'c' and lab in seen:
            lab = 'd'   # second "c)" in the ČTÚ text is in fact section d)
        seen.add(lab)
        sec['label2'] = lab
        if pt == PROV and lab == 'f':
            add_prefix_maps(sec, h3, h3p)
        doc.text.addElement(H(outlinelevel=2, stylename=h2p if (pt == PROV and lab == 'f') else h2, text=f'{lab}) {sec["title"]}'))
        if pt == PROV and lab == 'd' and sec['label'] == 'c':
            para(info, 'V originálu ČTÚ je tento oddíl chybně označen jako c); podle rozpisu počtu otázek jde o oddíl d).')
        if (pt, lab) in NOTE_NOLAW:
            para(info, NOTE_NOLAW[(pt, lab)])
        if not sec['items'] and sec['raw']:
            # spelling alphabet
            para(std, 'Hláskovací abeceda podle ČTÚ (česká / mezinárodní):')
            para(mono, '\n'.join(sec['raw']))
            add_excerpt('155_6_3'); add_excerpt('155_P1'); add_excerpt('RR_AP14')
            continue
        for pos, it in enumerate(sec['items']):
            key = (pt, sec['label'], it['n'])
            q, a = it['q'], it['a']
            if key in FIX:
                fq, fa = FIX[key]
                q = fq or q; a = fa or a
            if pt == PROV and lab == 'd':
                key = (pt, 'd', it['n'])
            stats['q'] += 1
            para(qst, f'{lab}) {it["n"]}. {q}')
            para(ans, a, label='Správná odpověď: ')
            vt = pasma.note((pt, lab, it['n']))
            if vt:
                p = P(stylename=note); p.addElement(Span(stylename=bold, text='Vysvětlivka: ')); teletype.addTextToElement(p, vt); doc.text.addElement(p)
            vt = doplnky.VYSV_I.get(it['n']) if pt == ELEK and lab == 'i' else None
            if vt:
                p = P(stylename=note); p.addElement(Span(stylename=bold, text='Vysvětlivka: ')); teletype.addTextToElement(p, vt); doc.text.addElement(p)
            if pt == ELEK and lab in 'cdefg':
                ob = obrazky_elek.figure(lab, pos)
                if ob:
                    odata, ow, oh, ocap = ob
                    href = doc.addPicture(f'Pictures/elek_{lab}{pos:02d}.svg', 'image/svg+xml', odata)
                    p = P(stylename=fig)
                    fr = Frame(width='15cm', height=f'{15 * oh / ow:.2f}cm', anchortype='as-char', name=f'elek_{lab}{pos:02d}')
                    fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
                    p.addElement(fr); doc.text.addElement(p)
                    para(cap, ocap)
            keys = list(M.get((pt, lab, it['n']), []))
            extra = []
            if pt == PROV and lab == 'd':
                for c in re.findall(r'Q[A-Z]{2}', a):
                    r = qcode(c)
                    if r: extra.append(r)
            if pt == PROV and lab == 'e':
                for c in [x.strip() for x in a.split(',')]:
                    r = abbr(c)
                    if r: extra.append(r)
            if pt == PROV and lab == 'f':
                r = ap42_lookup(a)
                if r: extra.append(r)
            if pt == PROV and lab == 'c' and it['n'] in (13, 21):
                r = qcode('QRL')
                if r: extra.append(r)
            if keys or extra:
                stats['with'] += 1
            for k in keys:
                add_excerpt(k)
            for e in extra:
                para(src, e[0]); para(exc, e[1])
            nt = N.get((pt, lab, it['n']))
            if pt == PROV and lab == 'd' and 'QRJ' in a:
                nt = QRJ_NOTE
            if nt:
                para(note, nt, label=None) if False else None
                p = P(stylename=note); p.addElement(Span(stylename=bold, text='Poznámka: ')); teletype.addTextToElement(p, nt); doc.text.addElement(p)
            ptxt = (praxe.PRAXE_E.get(it['n']) if pt == PROV and lab == 'e' else
                    praxe_q.PRAXE_D.get(it['n']) if pt == PROV and lab == 'd' else
                    doplnky.PRAXE_C.get(it['n']) if pt == PROV and lab == 'c' else None)
            if ptxt:
                p = P(stylename=praxe_s); p.addElement(Span(stylename=lblp, text='Z praxe: ')); teletype.addTextToElement(p, ptxt); doc.text.addElement(p)
            if pt == PROV and lab == 'c' and it['n'] == 25:
                doc.text.addElement(H(outlinelevel=3, stylename=h3, text=majaky.TITLE))
                para(cap, majaky.INTRO)
                table(['2.2cm', '5.2cm', '4.4cm', '5.2cm'], ['Značka', 'Umístění', 'Kmitočty (MHz)', 'Poznámka'],
                      majaky.ROWS, [tcode, tcell, tcell, tcell])
                para(cap, majaky.NOTE)
            if pt == PROV and lab == 'c' and it['n'] == 18:
                doc.text.addElement(H(outlinelevel=3, stylename=h3, text=doplnky.SM_TITLE))
                para(cap, doplnky.SM_INTRO)
                sdata, sw, sh = doplnky.smeter_figure()
                href = doc.addPicture('Pictures/smetr.svg', 'image/svg+xml', sdata)
                p = P(stylename=fig)
                fr = Frame(width='16cm', height=f'{16 * sh / sw:.2f}cm', anchortype='as-char', name='smetr')
                fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
                p.addElement(fr); doc.text.addElement(p)
                para(cap, doplnky.SM_CAPTION)
                table(['2.6cm', '4.4cm', '2.4cm', '4.4cm', '3.2cm'], doplnky.S_HEADER, doplnky.S_ROWS,
                      [tcode, tcell, tcell, tcell, tcell], hl=lambda r: r[0] in ('S9', 'S8'))
                para(cap, doplnky.S_NOTE)
                table(['4.0cm', '13.0cm'], doplnky.RST_HEADER, doplnky.RST_ROWS, [tcode, tcell])
                para(cap, doplnky.RST_NOTE)
            if pt == PROV and lab == 'c' and it['n'] == 7:
                atitle, adesc, adata, aw, ah = azimut.generate()
                doc.text.addElement(H(outlinelevel=3, stylename=h3, text=atitle))
                href = doc.addPicture('Pictures/azimut.svg', 'image/svg+xml', adata)
                p = P(stylename=fig)
                fr = Frame(width='16cm', height=f'{16 * ah / aw:.2f}cm', anchortype='as-char', name='azimut')
                fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
                p.addElement(fr); doc.text.addElement(p)
                para(cap, adesc)

# ---- příloha: výtah z doporučení CEPT
doc.text.addElement(H(outlinelevel=1, stylename=h1, text=cept_vytah.TITLE))
para(info, cept_vytah.INTRO)
doc.text.addElement(H(outlinelevel=2, stylename=h2, text='Srovnání obou doporučení'))
w, hd, rows = cept_vytah.COMPARE
table(w, hd, rows, [tcode] + [tcell] * (len(w) - 1))
for dtitle, dinfo, blocks in cept_vytah.DOCS:
    doc.text.addElement(H(outlinelevel=2, stylename=h2, text=dtitle))
    para(info, dinfo)
    for b in blocks:
        if b[0] == 'h':
            doc.text.addElement(H(outlinelevel=3, stylename=h3, text=b[1]))
        elif b[0] == 'p':
            para(std, b[1])
        elif b[0] == 'ul':
            for it in b[1]:
                para(bullet, '• ' + it)
        elif b[0] == 'tab':
            table(b[1], b[2], b[3], [tcode] + [tcell] * (len(b[1]) - 1))

# ---- příloha: kmitočtové spektrum a radioamatérská pásma
doc.text.addElement(H(outlinelevel=1, stylename=h1, text=spektrum_pasma.TITLE))
para(info, spektrum_pasma.INTRO)
for j, (stitle, sdesc, sdata, sw, sh) in enumerate(spektrum_pasma.generate(), 1):
    href = doc.addPicture(f'Pictures/spektrum_pasma{j:02d}.svg', 'image/svg+xml', sdata)
    p = P(stylename=fig)
    fr = Frame(width='17cm', height=f'{17 * sh / sw:.2f}cm', anchortype='as-char', name=f'spektrum_pasma{j}')
    fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
    p.addElement(fr); doc.text.addElement(p)
    if sdesc:
        para(cap, sdesc)

# ---- příloha: radioamatérská pásma podle druhů provozu (plán IARU R1 + úseky z odpovědí ČTÚ provoz a)
doc.text.addElement(H(outlinelevel=1, stylename=h1, text=pasma_provoz.TITLE))
para(info, pasma_provoz.INTRO)
for j, (ptitle, pdesc, pdata, pw, ph) in enumerate(pasma_provoz.generate(), 1):
    href = doc.addPicture(f'Pictures/pasma_provoz{j:02d}.svg', 'image/svg+xml', pdata)
    p = P(stylename=fig)
    fr = Frame(width='17cm', height=f'{17 * ph / pw:.2f}cm', anchortype='as-char', name=f'pasma_provoz{j}')
    fr.addElement(DImage(href=href, type='simple', show='embed', actuate='onLoad'))
    p.addElement(fr); doc.text.addElement(p)
    if pdesc:
        para(cap, pdesc)

# ---- příloha: tahák vzorců k výpočtovým otázkám
doc.text.addElement(H(outlinelevel=1, stylename=h1, text=doplnky.TAHAK_TITLE))
para(info, doplnky.TAHAK_INTRO)
for gtitle, grows in doplnky.TAHAK:
    doc.text.addElement(H(outlinelevel=3, stylename=h3, text=gtitle))
    table(['7.0cm', '7.0cm', '3.0cm'], doplnky.TAHAK_HEADER, grows, [tcode, tcell, tcell])

doc.save(OUT)
print('questions', stats['q'], 'with excerpts', stats['with'])
