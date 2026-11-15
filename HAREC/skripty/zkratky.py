# -*- coding: utf-8 -*-
"""Seznam zkratek setříděný podle oblastí.

Řádek oblasti: (zkratka, význam)
  význam None      -> převezme se doslovně z odpovědi ČTÚ (provoz d) Q kódy, e) zkratky)
  význam '+text'   -> význam ČTÚ + ' – ' + text
  jinak            -> vlastní vysvětlení sestavitele
Sloupec „Otázka“ se doplní automaticky, pokud zkratku vysvětluje otázka ČTÚ.
Třídy vysílání se dekódují z tabulky přílohy 2 vyhl. 156/2005 Sb. (zdroje/predpisy_cz/2005-156.txt).
"""
import re

PROV = 'radiokomunikační provoz'


def ctu_map(faq):
    """zkratka -> {'disp': zobrazení, 'mean': [významy], 'ref': [odkazy]} z oddílů provoz d), e)."""
    out = {}
    for part in faq:
        if part['title'] != PROV:
            continue
        for sec in part['sections']:
            if sec['title'].startswith('Zkratky používané pro'):
                lab = 'd'
            elif sec['title'].startswith('Zkratky používané v radioamatérské'):
                lab = 'e'
            else:
                continue
            for it in sec['items']:
                mean = it['q'].strip().rstrip(':').strip()
                for code in [c.strip() for c in it['a'].split(',')]:
                    key = code.rstrip('?')
                    e = out.setdefault(key, {'disp': code, 'mean': [], 'ref': []})
                    if mean not in e['mean']:
                        e['mean'].append(mean)
                    e['ref'].append(f'2{lab}) {it["n"]}')
    return out


# ------------------------------------------------------------- třídy vysílání (příloha 2 vyhl. 156/2005 Sb.)
AM_LETTERS = set('AHRJBC')


def emission_table(path):
    txt = open(path, encoding='utf-8').read()
    txt = txt[txt.index('Příloha č. 2 k vyhlášce'):]
    parts = re.split(r'\n[abc]\) (?:první|druhý|třetí) znak[^\n]*\n', txt)
    tabs = []
    for chunk in parts[1:4]:
        d = {}
        for ln in chunk.split('\n'):
            f = [x.strip() for x in ln.split('|')]
            while f and not f[-1]:
                f.pop()
            if len(f) >= 3 and re.fullmatch(r'[A-Z0-9]', f[-1]):
                d[f[-1]] = re.sub(r'\s+', ' ', f[-2]).replace('úhl ovou', 'úhlovou')
        tabs.append(d)
    return tabs


def decode(code, tabs):
    a, b, c = code
    m = tabs[0][a]
    m = ('amplitudová modulace – ' + m[0].lower() + m[1:]) if a in AM_LETTERS else m
    lo = lambda s: s[0].lower() + s[1:]
    return f'{a} = {lo(m)}; {b} = {lo(tabs[1][b])}; {c} = {lo(tabs[2][c])}'


EMISSIONS = [  # (třída, typické použití – doplněk sestavitele)
    ('N0N', 'nemodulovaná nosná'),
    ('A1A', 'telegrafie klíčováním nosné – CW'),
    ('A2A', 'tónová telegrafie (MCW), např. vysílače ROB v pásmu 2 m (144–146 MHz)'),
    ('A3E', 'telefonie AM'),
    ('C3F', 'amatérská televize (ATV) s amplitudovou modulací'),
    ('F1A', 'telegrafie kmitočtovým klíčováním'),
    ('F1B', 'dálnopis RTTY (FSK)'),
    ('F1D', 'přenos dat kmitočtovým klíčováním (např. paket rádio 9 600 Bd)'),
    ('F2A', 'tónová telegrafie na FM (např. identifikace převáděče)'),
    ('F2D', 'paket rádio 1 200 Bd, APRS (AFSK na FM)'),
    ('F3E', 'telefonie FM'),
    ('F3F', 'amatérská televize (ATV) s kmitočtovou modulací'),
    ('G1A', ''),
    ('G1D', ''),
    ('G3E', 'telefonie s fázovou modulací (většina „FM“ radiostanic)'),
    ('J1D', ''),
    ('J2A', 'telegrafie tónem přes SSB vysílač'),
    ('J2B', 'RTTY, PSK31 apod. přes SSB vysílač (AFSK)'),
    ('J2D', 'digitální provozy ze zvukové karty přes SSB vysílač (např. FT8)'),
    ('J3E', 'telefonie SSB (LSB/USB)'),
]

EMISSION_NOTE = ('Třídu vysílání tvoří tři znaky (příloha 2 vyhl. č. 156/2005 Sb., v souladu s RR dodatkem 1): '
                 '1. druh modulace hlavní nosné, 2. povaha modulujícího signálu, 3. druh přenášené informace. '
                 'Před ni lze uvést potřebnou šířku pásma (např. 2K70J3E = SSB telefonie o šířce 2,7 kHz); '
                 'u amatérské služby to není povinné. Rozpis znaků je převzat doslovně z přílohy 2, '
                 'typické použití (za pomlčkou) doplnil sestavitel.')

# ------------------------------------------------------------- oblasti
# digitální druhy provozu – v tabulce podbarveny žlutě
DIGITAL = {'APRS', 'DV', 'MFSK', 'MGM', 'PSK', 'RTTY'}
DIGITAL_NOTE = ('Žlutě podbarvené jsou digitální druhy provozu (informace se přenáší jako data, kóduje a dekóduje '
                'je počítač nebo modem). V tabulce tříd vysílání jsou žlutě třídy se třetím znakem B (telegrafie pro '
                'automatický příjem, např. RTTY) nebo D (přenos dat).')


AREAS = [
    ('Organizace, předpisy a průkazy', None, [
        ('ČTÚ', 'Český telekomunikační úřad – národní povolovací orgán (vydává průkazy a oprávnění)'),
        ('ITU', '+International Telecommunication Union; sídlo Ženeva'),
        ('UIT', '+Union internationale des télécommunications (francouzský název ITU)'),
        ('ITU-R', 'radiokomunikační sektor ITU (vydává Radiokomunikační řád a doporučení ITU-R)'),
        ('RR', 'Radiokomunikační řád ITU (Radio Regulations), aktuálně vydání 2024'),
        ('AP42', 'dodatek 42 Radiokomunikačního řádu – tabulka přidělení sérií volacích znaků státům'),
        ('M.1172', 'doporučení ITU-R M.1172 – mezinárodní zkratky, signály a Q kódy'),
        ('WRC', 'Světová radiokomunikační konference ITU (World Radiocommunication Conference) – mění RR'),
        ('CEPT', 'Evropská konference poštovních a telekomunikačních správ (Conférence européenne des administrations des postes et des télécommunications)'),
        ('T/R 61-01', 'doporučení CEPT o radioamatérském oprávnění CEPT – krátkodobý provoz v navštívených zemích'),
        ('T/R 61-02', 'doporučení CEPT o harmonizovaném průkazu odborné způsobilosti HAREC'),
        ('HAREC', 'Harmonised Amateur Radio Examination Certificate – harmonizovaný průkaz odborné způsobilosti podle T/R 61-02 (v ČR třída A)'),
        ('NOVICE', 'průkaz odborné způsobilosti pro začátečníky podle doporučení CEPT ECC/REC (05)06 (v ČR třída N)'),
        ('IARU', '+International Amateur Radio Union; ČR patří do Regionu 1'),
        ('ICAO', 'Mezinárodní organizace pro civilní letectví (International Civil Aviation Organization)'),
        ('IMO', 'Mezinárodní námořní organizace (International Maritime Organization)'),
        ('Sb.', 'Sbírka zákonů České republiky'),
    ]),
    ('Druhy provozu', 'EMISSIONS', [
        ('AM', '+telefonie s amplitudovou modulací a oběma postranními pásmy'),
        ('APRS', 'Automatic Packet Reporting System – paketový přenos polohy a krátkých zpráv'),
        ('ATV', 'amatérská televize (Amateur Television) – přenos pohyblivého obrazu'),
        ('CW', '+Continuous Wave; provoz Morseovou abecedou'),
        ('DV', 'digitální hlas (Digital Voice) – digitální hovorové provozy'),
        ('EME', 'spojení odrazem od Měsíce (Earth–Moon–Earth)'),
        ('FAX', 'faksimile – přenos nepohyblivého obrazu'),
        ('FM', None),
        ('FONE', '+hovorový (telefonní) provoz'),
        ('LSB', '+SSB s dolním postranním pásmem; běžně pod 10 MHz'),
        ('MFSK', 'vícetónové kmitočtové klíčování (Multiple Frequency Shift Keying) – skupina digitálních provozů'),
        ('MGM', 'strojově generované druhy provozu (Machine Generated Modes) – digitální provozy vysílané a dekódované počítačem'),
        ('MS', 'spojení odrazem od ionizovaných stop meteorů (Meteor Scatter)'),
        ('PSK', 'fázové klíčování (Phase Shift Keying), např. PSK31'),
        ('RTTY', 'rádiový dálnopis (Radio Teletype), kmitočtové klíčování FSK'),
        ('SSB', '+telefonie s potlačenou nosnou a jedním postranním pásmem'),
        ('SSTV', 'přenos obrazu s pomalým rozkladem (Slow Scan Television)'),
        ('USB', '+SSB s horním postranním pásmem; běžně od 10 MHz výše'),
    ]),
    ('Kmitočtová pásma, jejich status a šíření vln', None, [
        ('LF', '+30–300 kHz (Low Frequency)'),
        ('LW', '+Long Wire / Long Wave'),
        ('MF', 'střední kmitočty 300 kHz–3 MHz (Medium Frequency), střední vlny'),
        ('HF', 'vysoké kmitočty 3–30 MHz (High Frequency) = krátké vlny'),
        ('KV', 'krátké vlny (3–30 MHz)'),
        ('SW', '+Short Wave (3–30 MHz)'),
        ('VHF', '+30–300 MHz (Very High Frequency)'),
        ('VKV', 'velmi krátké vlny (30–300 MHz), v radioamatérské praxi často souhrnně pásma od 50 MHz výše'),
        ('UHF', '+300 MHz–3 GHz (Ultra High Frequency)'),
        ('SHF', '+3–30 GHz (Super High Frequency)'),
        ('WARC', 'pásma 10, 18 a 24 MHz přidělená amatérské službě Světovou administrativní radiokomunikační konferencí 1979 (WARC-79); nepořádají se v nich závody'),
        ('P', 'přednostní (primární) přidělení pásma – příloha 1 vyhl. č. 156/2005 Sb.'),
        ('S', 'podružné (sekundární) přidělení pásma – příloha 1 vyhl. č. 156/2005 Sb.'),
        ('NIB', 'na neinterferenční bázi – příloha 1 vyhl. č. 156/2005 Sb.'),
        ('MUF', 'nejvyšší použitelný kmitočet (Maximum Usable Frequency) pro odraz od ionosféry'),
        ('LUF', 'nejnižší použitelný kmitočet (Lowest Usable Frequency)'),
        ('UTC', '+Coordinated Universal Time; v ČR SEČ = UTC + 1 h, SELČ = UTC + 2 h'),
    ]),
    ('Zařízení, obvody a měření', None, [
        ('AC', None), ('DC', None),
        ('AD', 'analogově-číslicový (převodník), převod analogového signálu na digitální'),
        ('AER', None), ('ANT', None),
        ('AGC', None), ('AVC', None), ('ALC', None),
        ('BFO', 'záznějový oscilátor (Beat Frequency Oscillator) pro příjem CW a SSB'),
        ('BNC', 'typ koaxiálního konektoru (spolu s konektorem N předepsán pro účely státní kontroly)'),
        ('N', 'typ koaxiálního konektoru N'),
        ('BUG', None), ('ELBUG', None), ('KY', None),
        ('dB', '+logaritmická jednotka poměru výkonů, napětí apod.'),
        ('EL', None),
        ('GND', None),
        ('GP', 'anténa typu ground plane – vertikální čtvrtvlnný zářič s protiváhami'),
        ('GPS', 'družicový navigační systém (Global Positioning System)'),
        ('IF', None),
        ('LC', 'obvod z indukčnosti (L) a kapacity (C), rezonanční obvod'),
        ('LED', 'svítivá dioda (Light Emitting Diode)'),
        ('MTR', None),
        ('PA', None),
        ('PEP', '+výkon ve špičce modulační obálky (Peak Envelope Power)'),
        ('PLL', 'fázový závěs (Phase Locked Loop), základ kmitočtových syntezátorů'),
        ('PSV', '+poměr stojatých vln'), ('SWR', '+Standing Wave Ratio'),
        ('PWR', None),
        ('RF', None),
        ('RIG', None),
        ('RIT', 'jemné rozladění přijímače vůči vysílači (Receiver Incremental Tuning)'),
        ('RX', None), ('TX', None), ('TRX', None),
        ('S-metr', 'měřič síly přijímaného signálu ve stupních S'),
        ('SDR', 'softwarově definované rádio (Software Defined Radio) – signál zpracován digitálně'),
        ('TBS', None),
        ('VFO', '+Variable Frequency Oscillator'),
        ('WTTS', None),
    ]),
    ('Rušení a elektromagnetická kompatibilita', None, [
        ('BCI', '+Broadcast Interference'),
        ('TVI', '+Television Interference'),
        ('RFI', '+Radio Frequency Interference'),
        ('EMC', 'elektromagnetická kompatibilita (Electromagnetic Compatibility)'),
    ]),
    ('Stanice, operátoři a průběh spojení', None, [
        ('/p', 'doplněk volací značky při provozu z přechodného pevného stanoviště (vyhl. č. 156/2005 Sb.)'),
        ('/m', 'doplněk volací značky při mobilním provozu (vyhl. č. 156/2005 Sb.)'),
        ('AR', None), ('AS', None), ('AWARD', None), ('BK', None), ('CALL', None), ('CL', None),
        ('CQ', None), ('DE', None), ('DIRECT', None), ('DWN', None), ('DX', None),
        ('HAM', None), ('K', None), ('KA', None), ('KN', None), ('LID', None),
        ('LIS', None), ('UNLIS', None), ('LOG', None), ('NET', None), ('OP', None),
        ('OSCAR', '+Orbiting Satellite Carrying Amateur Radio'),
        ('QSLN', None), ('R', None),
        ('ROB', 'rádiový orientační běh (mezinárodně ARDF – Amateur Radio Direction Finding)'),
        ('RPRT', None),
        ('RST', '+R = čitelnost (1–5), S = síla (1–9), T = tón (1–9, jen telegrafie)'),
        ('SASE', None), ('SK', None), ('SKED', None),
        ('SOS', 'tísňový signál v telegrafii'),
        ('MAYDAY', 'tísňové volání v telefonii'),
        ('STN', None), ('SWL', None), ('TEST', None), ('UP', None), ('VIA', None),
    ]),
    ('Pozdravy a společenské zkratky', None, [
        ('73', None), ('88', None), ('99', None),
        ('CUAGN', None), ('CUL', None), ('DR', None), ('FB', None), ('UFB', None),
        ('GA', None), ('GB', None), ('GD', None), ('GE', None), ('GL', None), ('GLD', None),
        ('GM', None), ('GN', None), ('HI', None), ('HPE', None), ('HPY', None),
        ('OM', None), ('YL', None), ('XYL', None), ('PSE', None),
        ('SRI', None), ('SRY', None), ('TKS', None), ('TNX', None), ('XMAS', None),
    ]),
    ('Běžná slova ve spojení', None, [
        ('ABT', None), ('AGN', None), ('ALL', None), ('CFM', None), ('CPI', None), ('CPY', None),
        ('ES', None), ('FER', None), ('HR', None), ('HRD', None), ('HW', None), ('I', None),
        ('INFO', None), ('my', None), ('NEAR', None), ('NIL', None), ('NO', None), ('NR', None),
        ('OK', None), ('ONLY', None), ('RCVD', None), ('RPT', None), ('SEND', None),
        ('SIGS', None), ('SN', None), ('SURE', None), ('TO', None), ('UR', None), ('VY', None), ('WKD', None),
    ]),
    ('Počasí a podmínky šíření', None, [
        ('CLOUDY', None), ('CONDS', None), ('CONDX', None), ('OVERCAST', None),
        ('SUNNY', None), ('TEMP', None), ('WX', None),
    ]),
    ('Q kódy', 'Významy podle ČTÚ. Otazník za kódem značí otázku; bez otazníku jde o sdělení (odpověď). '
                'Úplné znění obsahuje doporučení ITU-R M.1172.', 'QCODES'),
]

KEEP_ORDER = {'Kmitočtová pásma, jejich status a šíření vln'}  # řazeno podle kmitočtu, ne abecedně

INTRO = ('Zkratky jsou seřazeny podle oblastí, v rámci oblasti abecedně (pásma podle kmitočtu). U zkratek, které jsou předmětem '
         'otázek ČTÚ (část 2, oddíly d) Q kódy a e) zkratky), je význam převzat doslovně z odpovědi ČTÚ a ve sloupci '
         '„Otázka“ je odkaz na otázku (např. 2e) 27 = část 2, oddíl e), otázka 27). Doplňky za pomlčkou '
         'a vysvětlení ostatních zkratek doplnil sestavitel podle předpisů a radioamatérské praxe.')


def sort_key(s):
    k = s.lstrip('/').upper()
    return (0 if k[0].isalpha() else 1, k)


def build_rows(faq):
    """Vrátí [(název oblasti, poznámka, [(zkratka, význam, odkaz)], [(třída, rozpis, použití)] | None)].
    Zároveň vypíše zkratky ČTÚ, které nejsou zařazeny do žádné oblasti."""
    ctu = ctu_map(faq)
    used = set()
    res = []
    for title, note, rows in AREAS:
        out = []
        if rows == 'QCODES':
            for k in sorted(c for c in ctu if re.fullmatch(r'Q[A-Z]{2}', c)):
                e = ctu[k]
                out.append((e['disp'], '; '.join(e['mean']), ', '.join(e['ref'])))
                used.add(k)
            res.append((title, note, out, None))
            continue
        for k, mean in rows:
            e = ctu.get(k)
            if e:
                used.add(k)
                cm = '; '.join(e['mean'])
                mean = cm if mean is None else (cm + ' – ' + mean[1:] if mean.startswith('+') else mean)
                out.append((e['disp'], mean, ', '.join(e['ref'])))
            else:
                if mean is None or mean.startswith('+'):
                    raise SystemExit(f'zkratka {k}: chybí význam ČTÚ')
                out.append((k, mean, ''))
        if title not in KEEP_ORDER:
            out.sort(key=lambda r: sort_key(r[0]))
        res.append((title, note, out, note == 'EMISSIONS'))
    missing = sorted(set(ctu) - used)
    if missing:
        print('VAROVÁNÍ: nezařazené zkratky ČTÚ:', ', '.join(missing))
    return res
