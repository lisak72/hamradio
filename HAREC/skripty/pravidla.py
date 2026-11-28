# -*- coding: utf-8 -*-
"""Poslední oddíl dokumentu: „Pravidla a souvislosti pro snadnější zapamatování“.

Pravidla jsou odvozena z odpovědí ČTÚ (verze 05/2026); u každého pravidla jsou odkazy na otázky
(Př = předpisy, P = provoz, E = elektrotechnika). Kde pravidlo neplatí beze zbytku, je výjimka uvedena.
Opory mimo ČTÚ: plán IARU R1 HF (majáky IBP 14 099–14 101 kHz apod., nejnižší nastavení LSB 1 843 / 3 603 /
7 053 kHz, USB nejvýše 3 kHz pod horním okrajem), vyhl. 156/2005 Sb. (§ 4, § 9, příloha 1).
Pravidlo uživatele: u pásma v metrech vždy i kmitočet v MHz.
"""

TITLE = 'Pravidla a souvislosti pro snadnější zapamatování'

INTRO = ('Mnoho odpovědí ČTÚ se dá místo biflování odvodit z několika jednoduchých pravidel. Tento oddíl je shrnuje '
         'po oblastech; v posledním sloupci jsou odkazy na otázky (Př = předpisy, P = provoz, E = elektrotechnika). '
         'Pravidla jsou pomůcky, nikoli předpisy: kde mají výjimku, je uvedena, a u zkoušky vždy platí přesné znění '
         'odpovědi ČTÚ. Vzorce k výpočtovým otázkám jsou v předchozím taháku.')

HEADER = ['Pravidlo', 'Jak ho použít – příklady a výjimky', 'Otázky']

# Přehled KV pásem: jak se opakuje pořadí CW → digi → (maják) → FONE (vše kHz, podle odpovědí ČTÚ provoz a)).
BAND_TITLE = 'Přehled: pořadí úseků v KV pásmech (kHz, podle odpovědí ČTÚ)'
BAND_HEADER = ['Pásmo', 'CW', 'Digitální provozy', 'Maják IBP', 'FONE']
BAND_ROWS = [
    ('160 m (1,8 MHz)', '1 810 – 1 838', '1 838 – 1 843', '–', '1 840 – 2 000'),
    ('80 m (3,5 MHz)', '3 500 – 3 580 (DX 3 500 – 3 510)', '3 580 – 3 620', '–', '3 600 – 3 800'),
    ('40 m (7 MHz)', '7 000 – 7 040', '7 040 – 7 060', '–', '7 050 – 7 200'),
    ('30 m (10 MHz)', '10 100 – 10 140 (vyhl. 156)', '10 140 – 10 150', '–', 'není povolen'),
    ('20 m (14 MHz)', '14 000 – 14 070', '14 070 – 14 099', '14 100', '14 101 – 14 350'),
    ('17 m (18 MHz)', '18 068 – 18 095', '18 095 – 18 109', '18 110', '18 111 – 18 168'),
    ('15 m (21 MHz)', '21 000 – 21 070', '21 070 – 21 120', '21 150', '21 151 – 21 450'),
    ('12 m (24 MHz)', '24 890 – 24 915', '24 915 – 24 929', '24 930', '24 931 – 24 990'),
    ('10 m (28 MHz)', '28 000 – 28 070', '28 070 – 28 190', '28 200', '28 225 – 29 300 (pak družice 29 300 – 29 510)'),
]
BAND_NOTE = ('Čtěte tabulku zleva doprava jako pásmo zdola nahoru: CW začíná na spodním okraji pásma, digitální provozy '
             'navazují přesně tam, kde CW končí, a FONE sahá až k hornímu okraji pásma. Na pásmech 14 až 28 MHz je mezi '
             'digi a FONE maják mezinárodní sítě NCDXF/IARU (IBP); na 160, 80 a 40 m (1,8, 3,5 a 7 MHz) se digi a FONE '
             'naopak o několik kHz překrývají. Kmitočty majáků podle plánu IARU R1, ostatní podle odpovědí ČTÚ (P a) 2–29). '
             'Grafy všech pásem jsou v příloze „Radioamatérská pásma podle druhů provozu“.')

# (skupina, [(pravidlo, příklady a výjimky, otázky)])
GROUPS = [
    ('Rozdělení KV pásem (provoz a)', [
        ('Zdola nahoru vždy CW → digitální provozy → FONE.',
         'CW začíná na spodním okraji pásma: 1 810, 3 500, 7 000, 14 000, 18 068, 21 000, 24 890, 28 000 kHz\n'
         'Digi navazuje přesně na konec CW.\n'
         'FONE končí na horním okraji pásma: 2 000, 3 800, 7 200, 14 350, 18 168, 21 450, 24 990 kHz\n'
         '  → výjimka 10 m (28 MHz): FONE jen do 29 300 kHz, nad ním družicový down-link\n'
         '  → nejcennější DX úsek je úplně dole: CW DX na 80 m (3,5 MHz) = 3 500–3 510 kHz',
         'P a) 2–29'),
        ('Na 20, 15 a 10 m (14, 21, 28 MHz) končí CW na „…070 kHz“.',
         '14 070, 21 070, 28 070 kHz – konec CW a zároveň začátek digi (proslulý FT8 je na 14 074 kHz)\n'
         '7 040, 3 580, 1 838 kHz – na nižších pásmech je CW kratší\n'
         '18 095, 24 915 kHz – konec CW na 17 a 12 m (18 a 24 MHz)',
         'P a) 7, 10, 14, 16, 17, 19, 20, 22, 24, 25, 27, 28'),
        ('Mezera mezi digi a FONE patří majákům IBP (14 100, 18 110, 21 150, 24 930, 28 200 kHz).',
         'FONE začíná 1 kHz nad majákem: 14 101, 18 111, 21 151, 24 931 kHz\n'
         'Digi končí 1 kHz pod majákem: 14 099, 18 109, 24 929 kHz\n'
         '  → výjimka 15 m (21 MHz): digi podle ČTÚ končí už na 21 120 kHz\n'
         '  → výjimka 10 m (28 MHz): majáky zabírají 28 190–28 225 kHz, FONE začíná až na 28 225 kHz\n'
         'Majáky slouží k rychlému určení podmínek šíření.',
         'P a) 15, 16, 18, 19, 21, 23, 25, 26, 28; P c) 25'),
        ('Na 160, 80 a 40 m (1,8, 3,5 a 7 MHz) se digi a FONE překrývají.',
         '160 m: FONE od 1 840, digi do 1 843 kHz (FONE 1 840–2 000 kHz)\n'
         '80 m: FONE od 3 600, digi do 3 620 kHz (FONE 3 600–3 800 kHz)\n'
         '40 m: FONE od 7 050, digi do 7 060 kHz (FONE 7 050–7 200 kHz)',
         'P a) 2, 4, 5, 8, 9, 11'),
        ('30 m (10 MHz) je pásmo bez FONE – jen CW a úzkopásmová data.',
         'Digi 10 140–10 150 kHz\n'
         '  → proto „LSB nelze na 10,14 MHz“\n'
         '  → proto „na 10 145 kHz jen úzkopásmové datové provozy“\n'
         'Vyhl. 156 zde povoluje jen:\n'
         '10 100–10 140 kHz – A1A, F1A, G1A, J2A\n'
         '10 140–10 150 kHz – J1D, J2D, F1D, G1D',
         'P a) 12, 13; Př c) 25, 36'),
        ('Pásma WARC = 30, 17 a 12 m (10, 18, 24 MHz) – ta „nepravidelná“.',
         'Klasická KV pásma jsou násobky 3,5 MHz: 3,5 – 7 – 14 – 21 – 28 MHz\n'
         'Pásma WARC (přidělena konferencí WARC 1979) mezi ně nezapadají.\n'
         '  → na pásmech WARC se nekonají závody',
         'P a) 41; P c) 24'),
        ('Pod 10 MHz LSB, nad 10 MHz USB – a SSB signál nesmí vyčnívat z úseku ani z pásma.',
         'LSB leží asi 3 kHz pod nastaveným kmitočtem, USB asi 3 kHz nad ním.\n'
         '1 840 kHz – SSB nelze: LSB by zasáhlo pod začátek FONE úseku (IARU: LSB nejníže 1 843, 3 603, 7 053 kHz)\n'
         '14,35 MHz – USB nelze: signál by přesáhl horní okraj pásma 14 350 kHz (IARU: USB nejvýše 3 kHz pod okrajem)',
         'Př c) 25, 26, 35'),
    ]),
    ('VKV pásma (provoz a)', [
        ('I na VKV je CW na začátku.',
         '6 m (50 MHz): 50,0–50,1 MHz\n'
         '2 m (144 MHz): 144,000–144,110 MHz\n'
         '70 cm (430–440 MHz): CW přednostně 432,025–432,1 MHz, nad ním CW i SSB 432,1–432,4 MHz',
         'P a) 32, 33, 39, 40'),
        ('Majáky na 2 m a 70 cm mají stejné číslice za čárkou: ,400 – ,490.',
         '2 m (144 MHz): 144,400–144,490 MHz\n'
         '70 cm (432 MHz): 432,400–432,490 MHz\n'
         '  → hned nad majáky na 70 cm jsou povoleny všechny druhy provozu: 432,5–432,975 MHz',
         'P a) 36, 37, 38'),
        ('Družice bývají u horního konce pásma.',
         '10 m (28 MHz): down-link 29 300–29 510 kHz\n'
         '2 m (144 MHz): 145,806–146,0 MHz',
         'P a) 29, 35'),
        ('6 m (50 MHz): dole CW, nad ním všechno úzkopásmové, FM jen úzký úsek.',
         '50–50,1 MHz – CW\n'
         '50,1–52 MHz – všechny úzkopásmové provozy\n'
         '51,410–51,590 MHz – přímý FM FONE\n'
         '  → chyták: pro EME CW na 2 m (144 MHz) ČTÚ uvádí „úsek není určen“',
         'P a) 30, 31, 32, 34'),
    ]),
    ('Výkony a nežádoucí vyzařování (předpisy c)', [
        ('Třída A: 750 W všude, kde vyhláška neříká jinak – méně jen v pásmech NIB.',
         '750 W v pásmech přednostních (P) i podružných (S):\n'
         '  1 820 kHz, 24 950 kHz, 7 105 kHz i během běžného (ne mezinárodního) závodu\n'
         'Snížený výkon jen v pásmech na neinterferenční bázi (NIB):\n'
         '  1 850–1 890 kHz – 75 W\n'
         '  1 890–2 000 kHz – 10 W\n'
         '  50–52 MHz – 25 W (také 3 400–3 410 MHz – 25 W)\n'
         '  → proto 1 850–2 000 kHz „nepatří mezi přednostní pásma“',
         'Př c) 16–20, 47, 48'),
        ('Víc než 750 W jen na mezinárodním závodě nebo při EME.',
         '1 500 W – v intravilánu (zastavěném území)\n'
         '3 000 W – mimo něj\n'
         'Výkony více zesilovačů na stejném kmitočtu se sčítají.',
         'Př c) 12, 27'),
        ('Ostatní „výkonová“ čísla: 50 W – 10 W – 6 W.',
         '50 W – neobsluhovaná stanice (převáděč, maják, paketový uzel)\n'
         '10 W – třída N\n'
         '6 W – nad tento výkon musí mít vysílač nesymetrický výstup 50–100 Ω\n'
         'Pro kontrolu musí být na stanici konektor N nebo BNC (či redukce).',
         'Př c) 24, 41, 44'),
        ('Nežádoucí vyzařování: silnější vysílač musí víc potlačit.',
         'do 30 MHz – 40 dB, nejvýše 50 mW\n'
         '2 m (144 MHz) nad 25 W – 60 dB, nejvýše 1 mW\n'
         '70 cm (430–440 MHz) nad 25 W – 60 dB, nejvýše 20 mW\n'
         'VKV do 25 W – 40 dB, nejvýše 25 µW\n'
         '  → 6 m (50 MHz) smí mít nejvýše 25 W, patří tedy vždy do kategorie „do 25 W“: 40 dB a 25 µW',
         'Př c) 31–34'),
    ]),
    ('Kdo co určuje (předpisy a, b, c)', [
        ('ITU (Radiokomunikační řád) = to, co musí být stejné na celém světě.',
         'tvar volací značky\n'
         'série volacích značek pro státy\n'
         'status pásem\n'
         'označení druhů (tříd) vysílání\n'
         'ČR leží v Regionu 1 ITU.',
         'Př a) 6, 10, 12, 13; Př c) 23'),
        ('Národní povolovací orgán (u nás ČTÚ) = výkon, zkoušky, oprávnění.',
         'maximální výkon\n'
         'požadavky na zkoušky\n'
         'vydání oprávnění (zpravidla na 5 let) i průkazu HAREC\n'
         '  → v cizině platí předpisy a povolovací orgán navštívené země',
         'Př a) 4, 5, 9; Př b) 4, 14; Př c) 1, 21'),
        ('IARU (Region 1) = rozdělení pásem na úseky pro druhy provozu.',
         'Doporučení IARU převzala vyhláška 156 (§ 4 odst. 3).\n'
         '  → ITU určuje status pásma, IARU jeho vnitřní dělení',
         'Př c) 9; P a) 1'),
        ('CEPT: T/R 61-01 = licence (vysílání v cizině), T/R 61-02 = HAREC (zkouška).',
         'T/R 61-01 (1985, starší – řeší, co radioamatér potřeboval dřív):\n'
         '  krátkodobé vysílání v cizině, nejvýše 3 měsíce nepřetržitě\n'
         '  neplatí pro klubové stanice\n'
         '  seznam zemí je přímo v doporučení\n'
         'T/R 61-02 (1990, přidalo společnou zkoušku):\n'
         '  požadavky na zkoušky\n'
         '  přehled zemí vyžadujících telegrafii\n'
         '  oprávnění v cizině bez další zkoušky\n'
         'CEPT zná jen jednu třídu.',
         'Př b) 1–16'),
    ]),
    ('Volací značky a provozní pravidla (předpisy, provoz c)', [
        ('Značka v cizině: kde jsem / kdo jsem / jak vysílám.',
         'FK/DL1YD/p – DL1YD vysílá přechodně z Nové Kaledonie\n'
         'OK/vlastní značka – cizinec u nás\n'
         '/p (portable) – jiné pevné stanoviště\n'
         '/m (mobile) – pohyblivé stanoviště\n'
         '/mm – loď, /am – letadlo (se souhlasem majitele či provozovatele)\n'
         '  → v závodech /p a /m nejsou povinné',
         'Př b) 2, 6; Př c) 5–8; P c) 10'),
        ('Klubová stanice: OK1/OK2 + 3 písmena začínající K, O nebo R. Neobsluhovaná: OK0 + 1 až 3 písmena.',
         'Nula = nikdo ji neobsluhuje.\n'
         'Neobsluhované stanice: převáděč, maják, paketový uzel\n'
         '  → nepatří sem pozemní stanice družicové služby\n'
         'převáděč – přenáší signály jiných stanic\n'
         'maják – jen vysílá (jednocestná komunikace)',
         'Př c) 13, 14, 43, 45, 46'),
        ('Třípísmenný sufix nesmí začínat písmenem Q.',
         'Zaměnil by se s Q kódy.\n'
         'ČR má série OKA–OKZ a OLA–OLZ, tedy prefixy OK a OL.',
         'Př a) 11, 14; P f) 1'),
        ('Čísla k zapamatování: 10 minut – 3 měsíce – 5 let.',
         '10 minut – vlastní značka na začátku a konci spojení a při delším spojení každých 10 minut\n'
         '3 měsíce – podle CEPT lze z ciziny vysílat nepřetržitě 3 měsíce\n'
         '5 let – obvyklá platnost oprávnění',
         'Př b) 3; Př c) 21, 38, 39'),
        ('Typická odpověď: zákaz s jedinou úzkou výjimkou.',
         'změna kmitočtu – žádné vyzařování, kromě družic\n'
         'zkušební vysílání – jen do umělé zátěže, kromě nastavení antén\n'
         'zprávy pro třetí osoby – jen při ohrožení života, zdraví a majetku (katastrofy), pak v libovolném pásmu\n'
         'kódované zprávy – nikdy\n'
         'telegrafní zkouška – pro HAREC se neskládá',
         'Př a) 8; Př c) 3, 4, 15, 30, 40'),
        ('Klubová stanice: deník, dozor a třída N.',
         'staniční deník – povinný jen u klubových stanic, zapisuje ho operátor\n'
         'za obsluhu odpovídá – dozírající operátor\n'
         'bez HAREC i NOVICE – jen ve třídě N pod dozorem',
         'Př c) 2, 11, 28, 37'),
        ('Orientační běh (ARDF): MO + E, I, S, H, 5 = jedna až pět teček.',
         'MOE – ·\n'
         'MOI – ··\n'
         'MOS – ···\n'
         'MOH – ····\n'
         'MO5 – ·····\n'
         '  → počet teček = číslo vysílače („lišky“); samotné MO vysílá maják v cíli',
         'Př c) 22'),
    ]),
    ('Provozní dovednosti (provoz c)', [
        ('Azimuty z Prahy po směru hodinových ručiček.',
         ' 45° – Japonsko\n'
         ' 85° – Austrálie\n'
         '175° – Jihoafrická republika\n'
         '240° – Argentina\n'
         '280° – Karibik\n'
         '315° – USA\n'
         '355° – Havaj\n'
         '  → nejkratší cesta (ortodroma) vede přes vysoké zeměpisné šířky: USA i Havaj leží „severněji“, než by '
         'se zdálo z mapy (Havaj téměř na sever přes pól), Austrálie téměř na východ; viz mapa za otázkou c) 7',
         'P c) 1–7'),
        ('CQ + upřesnění říká, koho stanice volá.',
         'CQ DX – mimo vlastní kontinent\n'
         'CQ SA – Jižní Amerika (obdobně EU, AF, AS, NA, OC)\n'
         'UP 5 – volejte o 5 kHz výš (split = příjem a vysílání na různých kmitočtech)\n'
         '10 DWN – o 10 kHz níž\n'
         'Prefix určí zemi: TU = Pobřeží Slonoviny.',
         'P c) 11, 14, 15, 16, 23'),
        ('RST: čitelnost 1–5, síla 1–9, tón 1–9; 599 = nejlepší.',
         'S9 na KV – 50 µV\n'
         'S9 na VKV – 5 µV\n'
         '1 stupeň S = 6 dB = poloviční napětí → S8 na KV = 25 µV\n'
         'Podrobně viz S-metr za otázkou c) 18.',
         'P c) 12, 17, 18'),
        ('Tísňové volání.',
         'SOS – telegraficky\n'
         'MAYDAY – fonicky',
         'P c) 8, 9'),
        ('QRL? = „Is this frequency in use?“ – stejná odpověď.',
         'Před výzvou se stanice ptá, zda je kmitočet volný.\n'
         '  → dvě otázky v oddílu c) a jedna v Q kódech',
         'P c) 13, 21; P d) 12'),
    ]),
    ('Q kódy (provoz d)', [
        ('Dotaz ↔ otazník.',
         'Je-li text otázky dotaz, správný Q kód má otazník:\n'
         '  QRO?, QRV?, QRL?, QRN?, QSO?, QSY?, QSK?, QRK?\n'
         'Oznámení a pokyny jsou bez otazníku:\n'
         '  QRM, QRZ, QRX, QSB, QRS, QRT, QRP, QRU, QSL, QTH …',
         'P d) 1–21'),
        ('Dvojice a „mluvící“ písmena.',
         'QRM – rušení interferencí (M jako man-made, lidmi)\n'
         'QRN – atmosférické rušení (N jako nature)\n'
         'QRO – zvýšit výkon\n'
         'QRP – snížit výkon (QRP = provoz malým výkonem)\n'
         'QRS – vysílejte pomaleji (slow)\n'
         'QSL – potvrzuji (QSL lístek potvrzuje spojení)\n'
         'QSO – spojení\n'
         'QSY – změna kmitočtu\n'
         'QTH – poloha',
         'P d) 1, 2, 5, 6, 8, 11, 13–16'),
    ]),
    ('Zkratky (provoz e)', [
        ('Anglické slovo bez samohlásek.',
         'TNX, TKS – thanks (děkuji)\n'
         'PSE – please\n'
         'AGN – again\n'
         'ABT – about\n'
         'RCVD – received\n'
         'PWR – power\n'
         'HR – here\n'
         'SN – soon\n'
         'SRI, SRY – sorry\n'
         'WKD – worked\n'
         'HPE – hope, HPY – happy\n'
         'CFM – confirm\n'
         'RPT – repeat\n'
         'STN – station, SIGS – signals\n'
         'MTR – meter\n'
         'DR – dear, GLD – glad, VY – very\n'
         'BK – break',
         'P e) 4, 16, 18, 26, 42, 53, 87, 88, 95, 100, 102, 110, 111, 114, 116, 118, 122, 127, 130, 131, 134'),
        ('Zkratka čtená nahlas zní jako anglické slovo.',
         'UR – your (váš)\n'
         'CUL – see you later (později na shledanou)\n'
         'CUAGN – see you again (znovu)\n'
         'FER – for (za)\n'
         'R – roger (správně přijato)\n'
         'HI – smích\n'
         'ES – and (a)',
         'P e) 12, 56, 59, 70, 106, 119, 124'),
        ('G + písmeno = pozdrav (Good …).',
         'GM – dobré ráno\n'
         'GD – dobrý den\n'
         'GA – dobré odpoledne\n'
         'GE – dobrý večer\n'
         'GN – dobrou noc\n'
         'GB – sbohem\n'
         'GL – hodně štěstí\n'
         '  → pozor: GA je u ČTÚ také „pokračujte“ (go ahead) – obě odpovědi jsou správně',
         'P e) 66, 67, 68, 69, 90, 93, 101, 117'),
        ('Zařízení s X a „lidé“.',
         'TX – vysílač\n'
         'RX – přijímač\n'
         'TRX – transceiver\n'
         'WX – počasí (weather)\n'
         'OM – přítel (old man)\n'
         'YL – slečna (young lady)\n'
         'XYL – manželka (ex-young lady)',
         'P e) 7, 46, 65, 73, 92, 97, 99'),
        ('…I = rušení (interference); A…C = automatické řízení (automatic … control).',
         'BCI – rušení rozhlasu (broadcast)\n'
         'TVI – rušení televize\n'
         'RFI – rušení rádiového kmitočtu\n'
         'AGC – řízení zisku (gain)\n'
         'ALC – řízení úrovně (level)\n'
         'AVC – řízení hlasitosti (volume)',
         'P e) 6, 10, 25, 43, 112, 139'),
        ('Pásma podle předpony: LF < (MF) < HF < VHF < UHF < SHF.',
         'VHF – very (velmi) vysoký kmitočet, 30–300 MHz\n'
         'UHF – ultra vysoký kmitočet, 300–3 000 MHz\n'
         'SHF – super vysoký kmitočet, 3–30 GHz\n'
         '  → každé o dekádu výš\n'
         'SW – krátké vlny; LW – dlouhé vlny i dlouhý drát\n'
         'SSB – single (jedno postranní pásmo)\n'
         'LSB – lower (spodní), USB – upper (horní)',
         'P e) 14, 27, 32, 33, 44, 49, 75, 82, 138'),
        ('Zápor: UN… a …N.',
         'LIS – koncesovaný × UNLIS – nekoncesovaný\n'
         'QSLN – staniční lístek nezašlu\n'
         'NIL – nic',
         'P e) 71, 72, 108, 126'),
        ('Začátek a konec: KA – AR – K / KN – SK.',
         'KA – začátek relace\n'
         'AR – konec relace\n'
         'K – vysílejte (kdokoli)\n'
         'KN – přecházím na poslech jen pro určitou stanici\n'
         'SK – konec vysílání\n'
         'Čísla: 73 – srdečný pozdrav, 88 – polibek, 99 – zmiz!',
         'P e) 20, 30, 103, 104, 107, 109, 125, 140'),
        ('Pozor – stejná písmena, jiný význam podle oddílu.',
         'OM – přítel × prefix Slovenska\n'
         'YL – slečna × prefix Lotyšska\n'
         'ES – „a“ × prefix Estonska\n'
         'DR – milý × část prefixů Německa (DA–DR)\n'
         '  → v oddílu e) jde vždy o zkratku, v oddílu f) o prefix',
         'P e) 53, 65, 99, 119; P f) 3, 7, 23, 27'),
    ]),
    ('Prefixy (provoz f)', [
        ('Mnoho prefixů připomíná název země v jejím vlastním jazyce.',
         'D – Deutschland, Německo (DA–DR)\n'
         'F – France, Francie (F–FZ)\n'
         'I – Italia, Itálie (I, IA–IZ)\n'
         'EA – España, Španělsko (EA–EH)\n'
         'G – Great Britain, Anglie (G, GX)\n'
         'HB – Helvetia, latinský název Švýcarska (HB, HE)\n'
         'OE – Österreich, Rakousko\n'
         'HA – Hungary, Maďarsko (HA, HG)\n'
         'EI – Éire, irsky Irsko (EI, EJ)\n'
         'ES – Eesti, Estonsko\n'
         'LY – Lietuva, Litva\n'
         'LX – Luxembourg, Lucembursko\n'
         'TA – Türkiye, Turecko (TA–TC, YM)\n'
         'JA – Japan, Japonsko (JA–JS)\n'
         'HS – Siam, starý název Thajska\n'
         'HZ – Hidžáz, historické království, dnes Saúdská Arábie (HZ, 7Z)\n'
         'HV – Vatikán\n'
         'Jde o pomůcku k zapamatování, ne o původ přidělení.',
         'P f) 3, 5, 11–13, 17, 23, 25, 28, 31, 37, 44, 47, 54, 66, 79, 80'),
        ('Britské ostrovy: G + písmeno části země (a souběžná řada s M).',
         'G, GX – Anglie (England)\n'
         'GM, GS – Skotsko (Scotland)\n'
         'GW, GC, MW – Wales (W = Wales)\n'
         'GI, GN, MI – Severní Irsko (I = Ireland, N = Northern)\n'
         'GJ, GH, MJ – Jersey (J = Jersey)\n'
         'GU, GP, MU – Guernsey (U = gUernsey)\n'
         'GD, GT, MD – Ostrov Man (D = Douglas, hlavní město ostrova)\n'
         'Druhé písmeno řady M je vždy stejné jako u řady G.',
         'P f) 38, 47–52'),
        ('Ostrov nebo zvláštní území = prefix mateřské země + číslice.',
         'EA6–EH6 – Baleáry (Španělsko EA–EH)\n'
         'EA8–EH8 – Kanárské ostrovy (Španělsko EA–EH)\n'
         'EA9–EH9 – Ceuta a Melilla (Španělsko EA–EH)\n'
         '  → čím dál od Madridu, tím vyšší číslice: Středomoří 6 → Atlantik 8 → Afrika 9\n'
         'IS0, IM0 – Sardinie (Itálie I)\n'
         'SV5–SZ5 – Dodekanés (Řecko SV–SZ)\n'
         'SV9–SZ9 – Kréta (Řecko SV–SZ)\n'
         'CQ2, CR2, CS2, CT2, CU2 – Azory (Portugalsko CQ–CU)\n'
         'OH0 – Alandy (Finsko OF–OJ)\n'
         'OJ0 – Market Reef, ostrůvek na hranici se Švédskem (Finsko OF–OJ)\n'
         'HB0 – Lichtenštejnsko, samostatný stát s prefixem Švýcarska (HB)\n'
         'Číslice 0 často značí ostrov nebo malé území.',
         'P f) 6, 12–14, 20, 37, 39, 41–43, 53, 55, 58, 59, 62, 63'),
        ('Ostrov může mít i vlastní písmena mateřské řady.',
         'TK – Korsika (Francie: F–FZ, F1–F0, HW, TH, TK, TM, TO, TV)\n'
         'JW – Špicberky (Norsko: LA–LN, 3Y)\n'
         'JX – Jan Mayen (Norsko: LA–LN, 3Y)\n'
         'OX – Grónsko (Dánsko: OU–OZ, XP, 5P, 5Q)\n'
         'OY – Faerské ostrovy (Dánsko: OU–OZ, XP, 5P, 5Q)\n'
         'Dánská autonomní území mají stejné první písmeno O jako Dánsko.',
         'P f) 8, 10, 11, 56, 57, 60, 61, 68'),
        ('Severské země.',
         'SA–SM, 7S, 8S – Švédsko (S jako Sverige)\n'
         'LA–LN, 3Y – Norsko\n'
         'OU–OZ, XP, 5P, 5Q – Dánsko (nejznámější OZ)\n'
         'OF–OJ – Finsko (nejznámější OH)\n'
         'TF – Island\n'
         'Dánsko, Finsko i jejich území začínají písmenem O (OX, OY, OH0, OJ0).',
         'P f) 4, 6, 8, 10, 58–61, 67'),
        ('Pobaltí: pozor na zrcadlové YL a LY.',
         'ES – Estonsko\n'
         'YL – Lotyšsko\n'
         'LY – Litva (L jako Lietuva; Lotyšsko má písmena obráceně)\n'
         'ES a YL jsou zároveň zkratky („a“, „slečna“) – v oddílu f) jde vždy o prefix.',
         'P f) 23, 25, 27'),
        ('Bývalé Československo a bývalý SSSR.',
         'OK, OL – Česká republika (série OKA–OKZ, OLA–OLZ)\n'
         'OM – Slovensko\n'
         '  → obě začínají O jako dřív společné Československo\n'
         'UA–UI – Rusko\n'
         'UR–UZ, EM–EO – Ukrajina\n'
         'EU–EW – Bělorusko\n'
         'ER – Moldavsko\n'
         'EK – Arménie\n'
         'ES – Estonsko\n'
         '  → bývalý SSSR má řady U a E; výjimkou je 4L Gruzie',
         'P f) 1, 7, 19, 21, 23, 45, 46, 76, 84'),
        ('Bývalá Jugoslávie: nástupnické státy mají nové, krátké prefixy s číslicí.',
         '9A – Chorvatsko\n'
         'S5 – Slovinsko (S jako Slovenija)\n'
         'E7 – Bosna a Hercegovina\n'
         'Z3 – Makedonie\n'
         '4O – Černá Hora\n'
         'YT–YU – Srbsko (jediné zůstalo u původního jugoslávského YU)',
         'P f) 15, 33, 35, 65, 69, 83'),
        ('Malé státy mají krátký prefix, často s číslicí.',
         '3A – Monako\n'
         '9H – Malta\n'
         'T7 – San Marino\n'
         'C3 – Andorra\n'
         'HV – Vatikán\n'
         'HB0 – Lichtenštejnsko (Švýcarsko HB)\n'
         'LX – Lucembursko\n'
         'ZA – Albánie',
         'P f) 31, 40, 53, 54, 64, 70–72'),
        ('V… a Z… = bývalá britská dominia.',
         'VA–VE, VO, VY (a CF–CK, CY–CZ, VX, XJ–XO) – Kanada\n'
         'VK – Austrálie\n'
         'VU – Indie\n'
         'ZL–ZM – Nový Zéland\n'
         'ZR–ZU – Jihoafrická republika\n'
         'Výjimky v Evropě: ZA Albánie, Z3 Makedonie.',
         'P f) 24, 26, 32, 35, 36, 70, 82'),
        ('Velké státy mají celé písmeno nebo dlouhou řadu.',
         'K, N, W, AA–AK – USA\n'
         'UA–UI – Rusko\n'
         'BA–BZ, B1–B0 – Čína\n'
         'BV – Tchaj-wan\n'
         'JA–JS, 7J–7N, 8J–8N – Japonsko\n'
         'F – Francie\n'
         'I – Itálie\n'
         'G – Anglie',
         'P f) 11, 13, 21, 22, 28, 47, 73, 74'),
        ('Další mimoevropské státy z otázek.',
         'XE–XI – Mexiko\n'
         'CL, CM, CO, T4 – Kuba\n'
         'PP–PY – Brazílie\n'
         'LO–LW – Argentina\n'
         'HL, DS–DT, D7–D9 – Jižní Korea\n'
         'P5–P9 – Severní Korea\n'
         '4X, 4Z – Izrael',
         'P f) 30, 34, 75, 77, 78, 81, 85'),
        ('Ostatní evropské státy z otázek.',
         'PA–PI – Nizozemsko\n'
         'ON–OT – Belgie\n'
         'HF, SN–SR, 3Z – Polsko (nejznámější SP)\n'
         'LZ – Bulharsko\n'
         'YO–YR – Rumunsko\n'
         'Mapy všech prefixů z otázek podle kontinentů jsou před oddílem f).',
         'P f) 2, 9, 16, 18, 29'),
    ]),
    ('Elektrotechnika (a–f, h)', [
        ('Jednotky nesou jména fyziků.',
         'ampér – proud\n'
         'ohm – odpor\n'
         'watt – výkon\n'
         'hertz – kmitočet\n'
         'henry – indukčnost\n'
         'farad – kapacita',
         'E a) 1–4; E b) 1, 2'),
        ('Cívka a kondenzátor se chovají opačně.',
         'cívka – reaktance s kmitočtem roste; napětí předbíhá proud\n'
         'kondenzátor – reaktance s kmitočtem klesá; proud předbíhá napětí\n'
         '  → pomůcka ELI–ICE: u L je E (napětí) před I (proudem), u C je I před E\n'
         'Kondenzátory se paralelně sčítají (jako odpory sériově).',
         'E b) 8–11; E c) 2–4'),
        ('Rezonance: sériový obvod = zkrat (0 Ω), paralelní = rozpojeno (∞).',
         'Větší L nebo C → nižší rezonanční kmitočet\n'
         '  → např. paralelně přidaný kondenzátor kmitočet sníží',
         'E c) 1, 12, 13'),
        ('Filtr podle jména: propust propouští, zádrž zadržuje; dolno-/horno- = nízké/vysoké kmitočty.',
         'KV vysílač vyrábí harmonické (vyšší kmitočty) → hornofrekvenční zádrž mezi vysílač a anténu\n'
         'televizi ruší KV (nižší kmitočet než TV) → dolnofrekvenční zádrž před televizor\n'
         'π filtr (C – L – C) – dolní propust\n'
         'tranzistorový koncový stupeň – na výstupu pásmové propusti\n'
         'elektronkový koncový stupeň – na výstupu laděné obvody',
         'E c) 5; E e) 7, 8; E i) 1, 3'),
        ('Měřicí přístroj nesmí měřený obvod ovlivnit.',
         'ampérmetr – do série, malý odpor; rozsah zvětší bočník (paralelní odpor)\n'
         'voltmetr – paralelně, velký vstupní odpor\n'
         'umělá zátěž – čistě ohmická',
         'E h) 1, 2, 3, 6'),
        ('Všechno nežádoucí v přijímači vzniká směšováním.',
         'Směšovač dává součet i rozdíl:\n'
         '  mf = rozdíl, 14,255 − 13,8 = 0,455 MHz\n'
         '  nežádoucí součet 14,255 + 13,8 = 28,055 MHz\n'
         'zrcadlový kmitočet – produkt směšování\n'
         'intermodulace – směšování více silných signálů',
         'E d) 5, 6, 8, 11'),
        ('Rozepište zkratku – odpověď bývá v názvu.',
         'RIT – Receiver Incremental Tuning (rozladění jen přijímače)\n'
         'PLL – Phase-Locked Loop (porovnávání fáze)\n'
         'SDR – Software Defined Radio (digitální zpracování)\n'
         'AD – analog → digital\n'
         'BFO – Beat Frequency Oscillator (záznějový, pro SSB a CW)\n'
         'PEP – Peak Envelope Power (výkon ve špičce obálky)\n'
         'balun – BALanced–UNbalanced (symetrické ↔ nesymetrické)\n'
         'GP – ground plane (svislá anténa s „umělou zemí“, vertikální polarizace)',
         'E a) 18; E c) 9, 14; E d) 1, 3, 15; E e) 6; E f) 8, 9'),
        ('SSB = AM bez nosné a bez jednoho postranního pásma.',
         'nejužší fonický provoz\n'
         'informace je v kterémkoli postranním pásmu\n'
         'nežádoucí pásmo odstraní pásmový filtr\n'
         'k příjmu je nutný záznějový oscilátor (BFO)\n'
         'přemodulovaný SSB je zkreslený a širší',
         'E a) 14, 17; E c) 6, 9; E d) 3; E e) 2, 3, 9'),
        ('Nejvíc výkonu přejde, když se impedance rovnají.',
         'PSV = 1 – ideální přizpůsobení\n'
         'měří se PSV metrem či reflektometrem\n'
         'bez antény nebo umělé zátěže hrozí zničení koncového stupně',
         'E e) 10, 11; E f) 4, 12; E h) 5, 8'),
    ]),
    ('Šíření rádiových vln (elektrotechnika g)', [
        ('Vrstvy ionosféry abecedně zdola: D, E, F1, F2.',
         'E – ve výšce asi 100 km\n'
         'F2 – nejvyšší, a proto nejdůležitější pro dálková spojení',
         'E g) 1, 13, 14'),
        ('Noc = nízká pásma, hodně slunečních skvrn = vysoká pásma.',
         'v noci – 160, 80, 40 m (1,8, 3,5, 7 MHz)\n'
         'při maximu slunečního cyklu (11 let) – i nad 40 MHz\n'
         'geomagnetická bouře – šíření KV zhorší\n'
         'slunce ovlivňuje vše kromě přízemní vlny a přímého paprsku',
         'E g) 2, 3, 5, 6, 8'),
        ('MUF: zvolte nejvyšší pásmo pod MUF.',
         'MUF 17 MHz → 20 m (14 MHz)\n'
         'Vlna pod MUF se (zčásti) vrátí k Zemi.',
         'E g) 7, 10'),
        ('VKV/UKV = přímá viditelnost; pohyb = Dopplerův jev.',
         '70 cm (430–440 MHz) – běžně přímou viditelností\n'
         'EME – v pásmech 6 m až 3 cm (50 MHz až 10 GHz)\n'
         'Dopplerův jev – u družic, které se rychle pohybují',
         'E g) 4, 16, 17'),
    ]),
    ('Bezpečnost a rušení (elektrotechnika i, j)', [
        ('Střídavý proud je nebezpečnější – pro střídavý platí vždy nižší limit.',
         'bezpečné napětí – stejnosměrné do 60 V, střídavé do 25 V\n'
         'bezpečný proud – stejnosměrný do 10 mA, střídavý do 3,5 mA',
         'E j) 1, 6'),
        ('Anténa: uzemnit, dál od lidí, dál od přijímačů.',
         'venkovní antény – řádně uzemnit a spojit s hromosvodem (jímací tyč ale není držák antény)\n'
         'GP – tak, aby se jí nikdo nemohl dotknout\n'
         'vnitřní anténa – co nejdál od pracoviště\n'
         'vysílací anténa – co nejdál od TV a rozhlasových antén\n'
         'uzemňovací vodič – co nejkratší',
         'E i) 5, 7; E j) 7, 8, 10, 11, 12'),
    ]),
    ('Jak číst testové otázky', [
        ('Pozor na zápor v otázce.',
         'nepovoluje, nepatří, nelze, nevztahuje, není nutno, nemá vliv, neslouží …\n'
         '  → hledá se ta jediná odpověď, která do skupiny nepatří',
         'Př a) 11; Př b) 10, 16; Př c) 25, 26, 30, 35, 43, 47; E d) 3; E f) 15; E g) 9; E h) 7'),
        ('Některé otázky se opakují – se stejnou odpovědí.',
         'E a) 12 = E e) 4 – „malý zdvih“: výkon dostatečný, modulace slabá\n'
         'P c) 13 = P c) 21 – QRL? / „Is this frequency in use?“\n'
         'Př a) 4, 9 – národní povolovací orgán\n'
         'Př a) 10, 13 – Radiokomunikační řád ITU\n'
         'Př c) 16, 17, 19 – 750 W PEP\n'
         'P e) 27, E a) 17 – SSB',
         ''),
    ]),
]
