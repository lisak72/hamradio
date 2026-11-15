# -*- coding: utf-8 -*-
"""Stručný český výtah z doporučení CEPT T/R 61-01 a T/R 61-02 (příloha na konci dokumentu).

Zdroj: zdroje/cept/TR6101.txt (vydání 18. 10. 2024) a zdroje/cept/TR6102.txt (vydání 16. 2. 2024).
Jde o shrnutí (ne doslovný překlad). Odkazy „→ b) n“ = otázka ČTÚ v části Předpisy, oddíl b).

Struktura: DOCS = [(nadpis, info, [blok, ...])], blok je
  ('h', 'podnadpis')            – nadpis 3. úrovně
  ('p', 'text')                 – odstavec
  ('ul', ['bod', ...])          – odrážky
  ('tab', šířky, hlavička, řádky) – tabulka
"""

TITLE = 'Příloha – Stručný výtah z doporučení CEPT T/R 61-01 a T/R 61-02'

INTRO = ('Shrnutí obsahu obou doporučení CEPT, na která se odkazují otázky oddílu „Předpisy CEPT“. Nejde o úřední '
         'překlad. Závazné je anglické znění (docdb.cept.org). Údaje v hranatých závorkách [→ b) n] odkazují na '
         'otázku ČTÚ v části 1, oddíl b), kterou daný bod zdůvodňuje.')

COMPARE = (['4.2cm', '6.4cm', '6.4cm'], ['', 'T/R 61-01 – licence CEPT', 'T/R 61-02 – HAREC'], [
    ('Co to je', 'Oprávnění (licence) k provozu stanice', 'Osvědčení o složení zkoušky (průkaz odborné způsobilosti)'),
    ('K čemu slouží', 'Krátkodobý provoz při návštěvě jiné země bez žádosti o dočasné povolení',
     'Získání národního oprávnění v jiné zemi bez další zkoušky (dlouhodobý pobyt) nebo po návratu domů'),
    ('Doba pobytu', 'Dočasný pobyt („temporary stays“); v ČR do 3 měsíců (§ 2 odst. 2 písm. b) vyhl. 156/2005 Sb.)',
     'Pobyt delší než 3 měsíce → národní oprávnění odpovídající úrovni CEPT'),
    ('Kdo ho vydává', 'Orgán, který vydal národní oprávnění (v ČR ČTÚ)', 'Povolovací orgán po úspěšné zkoušce (v ČR ČTÚ)'),
    ('Jazyky dokladu', 'Národní jazyk + němčina, angličtina, francouzština', 'Jazyk země vydání + angličtina, francouzština, němčina'),
    ('Volací značka', 'Prefix navštívené země / vlastní značka', '– (značku přidělí země, která vydá oprávnění)'),
    ('Telegrafie', 'Nevyžaduje se', 'Od roku 2003 se nevyžaduje (některé země ji dosud požadují)'),
    ('Nečlenské země CEPT', 'Mohou přistoupit (přílohy 3–5, prohlášení o shodě SOC)', 'Mohou přistoupit (přílohy 3 a 4)'),
    ('Odpovídající třída v ČR', 'Oprávnění třídy A', 'Průkaz HAREC třídy A → oprávnění třídy A'),
])

DOCS = [
    ('Doporučení T/R 61-01 – Licence CEPT pro radioamatéry',
     'Schváleno v Nice 1985, revize 1992 (otevření nečlenským zemím) a 2016 (prohlášení o shodě). Výchozí vydání 18. 10. 2024 '
     '(příloha 2 aktualizována 02/2024, příloha 4 10/2024).', [
        ('h', 'Účel a hlavní zásady (preambule a doporučující část)'),
        ('ul', [
            'Radioamatér ze země, která doporučení uplatňuje, může při krátké návštěvě jiné takové země vysílat bez '
            'individuálního dočasného povolení této země.',
            'Navštívená země za provoz na základě licence CEPT nevybírá správní poplatky ani poplatky za využívání kmitočtů. [→ b) 12]',
            'K systému mohou přistoupit i země, které nejsou členy CEPT (přílohy 3 a 4). Od roku 2016 k tomu podávají '
            'prohlášení o shodě (SOC, příloha 5), že jejich národní třídy odpovídají osnově HAREC. [→ b) 5]',
            'Znalost telegrafie (Morseovy abecedy) se pro účely doporučení nevyžaduje.',
            'Doporučení se netýká dovozu a vývozu radioamatérských zařízení – ten upravují jen celní předpisy.',
            'Správy si i nadále mohou vyhradit samostatné dvoustranné dohody.',
        ]),
        ('h', 'Příloha 1 – Obecné podmínky licence CEPT'),
        ('ul', [
            'Licence CEPT může být součástí národního oprávnění, nebo samostatným dokladem téhož orgánu; vyhotovuje se '
            'v národním jazyce a v němčině, angličtině a francouzštině.',
            'Platí jen pro osoby, které v navštívené zemi nemají trvalý pobyt („non-residents“), po dobu dočasného pobytu '
            'a v mezích platnosti národního oprávnění. [→ b) 11]',
            'Na držitele dočasného oprávnění vydaného v cizí zemi se doporučení nevztahuje. Licence je vázána na konkrétní '
            'osobu – podle výkladu ČTÚ ji proto nelze použít pro klubovou stanici. [→ b) 16]',
            'Minimální náležitosti: označení, že jde o licenci CEPT; prohlášení, že držitel smí podle doporučení provozovat '
            'stanici v zemích, které je uplatňují; jméno a adresa držitele; volací značka; doba platnosti; vydávající orgán. '
            'Datum narození ani rodné číslo mezi náležitostmi nejsou. [→ b) 10]',
            'Licence CEPT je jen jedna (jedna třída). Opravňuje k užívání všech pásem přidělených amatérské a amatérské '
            'družicové službě, která jsou povolena v zemi provozu. [→ b) 7]',
        ]),
        ('h', 'Příloha 1 – Podmínky užívání'),
        ('ul', [
            '2.1 Držitel na požádání předloží licenci CEPT příslušným orgánům navštívené země.',
            '2.2 Držitel dodržuje Radiokomunikační řád ITU, toto doporučení a předpisy navštívené země, včetně místních '
            'technických a jiných omezení. Pozor na rozdílné přidělení pásem ve třech regionech ITU. [→ b) 4]',
            '2.3 Volací značka = prefix navštívené země (podle přílohy 2 nebo 4) + „/“ + vlastní národní volací značka. '
            'V telegrafii se odděluje znakem „/“, v telefonii slovem „stroke“. Příklad: OK1ABC v Rakousku vysílá jako OE/OK1ABC. [→ b) 2, b) 6]',
            '2.4 Držitel nemůže požadovat ochranu před škodlivým rušením.',
            '3 Rovnocennost licence CEPT a národních oprávnění je uvedena v příloze 2 (země CEPT) a v příloze 4 (nečlenské '
            'země) – tam se také zjistí, ze kterých zemí lze podle doporučení vysílat. [→ b) 15]',
        ]),
        ('h', 'Příloha 2 – Výběr ze zemí CEPT (prefix pro hostující stanice / národní třída rovnocenná licenci CEPT)'),
        ('tab', ['5.0cm', '4.5cm', '7.5cm'], ['Země', 'Prefix', 'Rovnocenná národní třída'], [
            ('Česká republika', 'OK', 'A'),
            ('Slovenská republika', 'OM', 'E (dříve A, B, C)'),
            ('Rakousko', 'OE', '1 (dříve i 2)'),
            ('Německo', 'DL', '1, 2 a A'),
            ('Polsko', 'HF, SN, SO, SQ, SP, 3Z', '1'),
            ('Maďarsko', 'HA, HG', 'CEPT; dříve RB, RC, UB, UC'),
            ('Chorvatsko', '9A', 'CEPT (národní a CEPT licence jsou zatím oddělené)'),
            ('Itálie', 'I', 'A'),
            ('Francie', 'F (Korsika TK, zámořská území FG, FM, FR …)', 'HAREC, dříve třídy 1 a 2'),
            ('Spojené království', 'M (MD, MI, MJ, MM, MU, MW)', 'FULL'),
            ('Švýcarsko / Lichtenštejnsko', 'HB9 / HB0', '1, 2, CEPT / CEPT'),
            ('Estonsko', 'ES + číslice oblasti', 'A a B; hosté mají práva třídy B, pobyt do 3 měsíců'),
            ('Lotyšsko', 'YL', 'A; pobyt do 3 měsíců'),
        ]),
        ('p', 'Úplná tabulka obsahuje všechny země, které doporučení uplatňují (od Albánie po Ukrajinu, včetně Faerských '
              'ostrovů OY, Grónska OX, Alandských ostrovů OH0, Svalbardu JW, Azor CT8 a Madeiry CT9).'),
        ('h', 'Příloha 4 – Nečlenské země CEPT, které se k systému připojily'),
        ('tab', ['5.0cm', '4.5cm', '7.5cm'], ['Země', 'Prefix', 'Poznámka'], [
            ('USA', 'podle státu, např. W1–W0, KH6, KL7, KP4', 'Hostující držitel licence CEPT má práva třídy Amateur Extra'),
            ('Kanada', 'podle provincie VE1–VE9, VO1, VO2, VY0–VY2, CY0, CY9', 'Práva Advanced'),
            ('Austrálie', 'VK', 'Provoz až 365 dní bez další registrace'),
            ('Nový Zéland', 'ZL', 'Provoz až 90 dní bez povolení'),
            ('Izrael', '4X, 4Z', 'Práva třídy B (General)'),
            ('Jihoafrická republika', 'ZS', 'Práva Unrestricted'),
            ('Peru', 'OA + číslice zóny jako přípona za vlastní značkou', 'Rovnocennost se znovu stanovuje'),
            ('Kajmanské ostrovy; Aruba, Curaçao, Bonaire, St. Eustatius, Saba, St. Maarten', 'ZF; P4, PJ2, PJ4, PJ5, PJ6, PJ7', ''),
        ]),
    ]),
    ('Doporučení T/R 61-02 – Harmonizované osvědčení o radioamatérské zkoušce (HAREC)',
     'Schváleno v Chesteru 1990, revize 1994 (nečlenské země), 2001 (telegrafie snížena z 12 na 5 slov/min), 2003 '
     '(požadavek telegrafie zrušen), Vilnius 2004. Výchozí vydání 16. 2. 2024 (příloha 6 – osnova – aktualizována 02/2018).', [
        ('h', 'Účel a doporučující část'),
        ('ul', [
            'HAREC je doklad o úspěšném složení radioamatérské zkoušky podle harmonizované osnovy (příloha 6). Doporučení tedy '
            'stanoví požadavky na zkoušky pro získání průkazu odborné způsobilosti. [→ b) 1]',
            'Usnadňuje vydání individuálního oprávnění radioamatérovi, který v zemi pobývá déle, než umožňuje T/R 61-01, '
            'a radioamatérovi, který se vrací do vlasti s HAREC vydaným v cizině.',
            'Bod 1: Správy CEPT vydávají vzájemně uznávaný HAREC těm, kdo složili národní zkoušku odpovídající úrovni CEPT.',
            'Bod 2: Přistoupit mohou i nečlenské země CEPT (přílohy 3 a 4). [→ b) 9]',
            'Bod 3: Cizincům s HAREC, kteří v zemi pobývají déle než 3 měsíce, vydají správy (v souladu s národními předpisy) '
            'národní oprávnění odpovídající úrovni CEPT – bez další zkoušky. [→ b) 3, b) 9]',
            'Bod 4: Kdo získal HAREC v kterékoli zúčastněné zemi, má po návratu do vlastní země právo na oprávnění bez další zkoušky.',
            'HAREC sám o sobě neopravňuje k vysílání; opravňuje k podání žádosti o vydání oprávnění. [→ b) 13]',
            'Správy mohou požadovat samostatné dvoustranné dohody.',
        ]),
        ('h', 'Příloha 1 – Podmínky vydání HAREC'),
        ('ul', [
            'HAREC vydává správa (povolovací orgán) osobám, které složily národní zkoušku splňující kritéria doporučení; '
            'na žádost i těm, kdo příslušnou zkoušku složili před zavedením harmonizované osnovy. [→ b) 14]',
            'Oprávnění vydané na základě HAREC umožňuje užívat všechna pásma přidělená amatérské a amatérské družicové službě '
            'a povolená v zemi provozu.',
            'Zkouška musí pokrýt alespoň technické, provozní a předpisové znalosti potřebné pro zkoušky a provoz amatérské stanice.',
            'Doklad HAREC obsahuje v jazyce země vydání a v angličtině, francouzštině a němčině: prohlášení o složení zkoušky '
            'podle doporučení; jméno a datum narození držitele; datum vydání; vydávající orgán. Může být součástí národního '
            'průkazu nebo samostatným dokladem podle vzoru v příloze 5.',
        ]),
        ('h', 'Přílohy 2 a 4 – Rovnocenné národní třídy (výběr)'),
        ('tab', ['5.0cm', '5.5cm', '6.5cm'], ['Země', 'Třídy odpovídající HAREC', 'Oprávnění pro držitele cizího HAREC'], [
            ('Česká republika', 'A', 'A'),
            ('Slovenská republika', 'E (dříve A, B, C)', 'E'),
            ('Rakousko', '1 (dříve i 2)', '1'),
            ('Německo', '1, 2 a A', 'A'),
            ('Polsko', '1', '1'),
            ('Maďarsko', 'CEPT; dříve RB, RC, UB, UC', 'CEPT'),
            ('Estonsko', 'A, B', 'A (vyžaduje telegrafii min. 5 slov/min), B'),
            ('Irsko', 'CEPT 1 a CEPT 2', 'CEPT 1 (vyžaduje telegrafii min. 5 slov/min), CEPT 2'),
            ('Portugalsko', '1, A a B (A vyžaduje telegrafii min. 50 znaků/min)', '1'),
            ('Nečlenské země (příl. 4)', 'Austrálie, Curaçao, Hongkong, Izrael, Japonsko, Nový Zéland, Jihoafrická rep.', 'podle tabulky 2'),
        ]),
        ('p', 'Země, které dosud vyžadují znalost telegrafie, se zjistí z poznámek k tabulkám příloh 2 a 4 doporučení T/R 61-02. [→ b) 8]'),
        ('h', 'Příloha 6 – Osnova zkoušky HAREC'),
        ('p', 'Osnova je vodítkem pro správy při sestavování národních zkoušek. Uchazeč má znát jednotky veličin a jejich '
              'násobky, značky součástek a vzorce z osnovy (i jejich úpravy). Z matematiky: základní početní operace, zlomky, '
              'mocniny deseti, exponenty a logaritmy, druhá mocnina a odmocnina, převrácená hodnota, čtení lineárních '
              'a nelineárních grafů a dvojková soustava.'),
        ('tab', ['5.0cm', '12.0cm'], ['Část osnovy', 'Obsah'], [
            ('a) Technika', '1. Elektřina, elektromagnetismus a teorie rádia (vodivost, zdroje, elektrické a magnetické pole, '
                            'elektromagnetické pole, sinusové a nesinusové signály, šum, modulace, výkon a energie, DSP); '
                            '2. Součástky; 3. Obvody (filtry, napájecí zdroje, zesilovače, detektory, oscilátory, PLL, DSP); '
                            '4. Přijímače; 5. Vysílače; 6. Antény a napáječe; 7. Šíření vln; 8. Měření; '
                            '9. Rušení a odolnost; 10. Bezpečnost (lidské tělo, síťové napájení, vysoké napětí, blesk).'),
            ('b) Provozní pravidla a postupy', '1. Hláskovací abeceda (Alpha … Zulu); 2. Q kódy: QRK, QRM, QRN, QRO, QRP, QRT, QRZ, QRV, '
                            'QSB, QSL, QSO, QSY, QRX, QTH; 3. Provozní zkratky: BK, CQ, CW, DE, K, MSG, PSE, RST, R, RX, TX, UR; '
                            '4. Tísňové signály (radiotelegrafie SOS, radiotelefonie MAYDAY), tísňový provoz a spojení při '
                            'přírodních katastrofách; 5. Volací značky (identifikace, použití, skladba, národní prefixy); '
                            '6. Kmitočtové plány IARU a jejich účel; 7. Společenská odpovědnost (kodex radioamatéra, '
                            'samoregulace) a provozní postupy (navázání, vedení a ukončení spojení, kontrola kvality vysílání).'),
            ('c) Předpisy', '1. Radiokomunikační řád ITU (definice amatérské a amatérské družicové služby a amatérské '
                            'stanice, článek 25, status služeb, regiony ITU); 2. Předpisy CEPT (T/R 61-01, dočasný provoz '
                            've členských i nečlenských zemích CEPT); 3. Národní zákony, předpisy a podmínky oprávnění, '
                            'vedení staničního deníku (účel, zapisované údaje).'),
        ]),
    ]),
]
