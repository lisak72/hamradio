# -*- coding: utf-8 -*-
"""Seznam nejznámějších radioamatérských majáků (k otázce provoz c) 25). Max. 20 položek.

Zdroje (ověřeno 14. 11. 2026):
- NCDXF/IARU International Beacon Project: https://www.ncdxf.org/beacon/beaconlocations.html
- OZ7IGY: https://en.wikipedia.org/wiki/OZ7IGY
- DK0WCY: https://cq.sk/en/majak-dk0wcy
- České VKV majáky: https://ceskyradioklub.cz/aktuality/vkv-majaky-v-ok (stav k 3. 8. 2026)
"""

TITLE = 'Nejznámější radioamatérské majáky'

INTRO = ('Majáky (beacons) vysílají nepřetržitě svou volací značku, obvykle telegrafií (CW), na pevném kmitočtu a se '
         'známým výkonem. Podle toho, které majáky jsou slyšet a jak silně, lze rychle posoudit, kam je pásmo „otevřené“. '
         'Nejznámější je síť 18 majáků projektu NCDXF/IARU (International Beacon Project) na kmitočtech 14,100 – 18,110 – '
         '21,150 – 24,930 – 28,200 MHz. Každý maják vysílá 10 s na každém pásmu a majáky se pravidelně střídají v '
         'tříminutovém cyklu, takže na jednom kmitočtu vždy vysílá jen jeden. Maják vysílá volací značku a pak čtyři '
         'čárky s klesajícím výkonem 100 W, 10 W, 1 W a 0,1 W.')

IBP = '14,100 / 18,110 / 21,150 / 24,930 / 28,200'

ROWS = [  # (volací značka, umístění, kmitočty MHz, poznámka)
    ('4U1UN', 'New York – sídlo OSN (USA)', IBP, 'NCDXF/IARU, pořadí 1 v cyklu'),
    ('VE8AT', 'Inuvik (Kanada, severozápadní teritoria)', IBP, 'NCDXF/IARU – polární trasa'),
    ('W6WX', 'Mt. Umunhum, Kalifornie (USA)', IBP, 'NCDXF/IARU'),
    ('KH6RS', 'Maui, Havaj', IBP, 'NCDXF/IARU'),
    ('ZL6B', 'Masterton (Nový Zéland)', IBP, 'NCDXF/IARU – téměř protinožec Prahy'),
    ('VK6RBP', 'Roleystone u Perthu (Austrálie)', IBP, 'NCDXF/IARU'),
    ('JA2IGY', 'Mt. Asama (Japonsko)', IBP, 'NCDXF/IARU'),
    ('RR9O', 'Novosibirsk (Rusko)', IBP, 'NCDXF/IARU'),
    ('VR2B', 'Hongkong', IBP, 'NCDXF/IARU'),
    ('4S7B', 'Colombo (Srí Lanka)', IBP, 'NCDXF/IARU'),
    ('ZS6DN', 'Pretoria (Jihoafrická rep.)', IBP, 'NCDXF/IARU'),
    ('5Z4B', 'Kikuyu (Keňa)', IBP, 'NCDXF/IARU'),
    ('4X6TU', 'Tel Aviv (Izrael)', IBP, 'NCDXF/IARU'),
    ('OH2B', 'Lohja (Finsko)', IBP, 'NCDXF/IARU – nejbližší maják sítě k ČR'),
    ('CS3B', 'São Jorge, Madeira', IBP, 'NCDXF/IARU'),
    ('LU4AA', 'Buenos Aires (Argentina)', IBP, 'NCDXF/IARU'),
    ('OA4B', 'Lima (Peru)', IBP, 'NCDXF/IARU'),
    ('YV5B', 'Caracas (Venezuela)', IBP, 'NCDXF/IARU'),
    ('DK0WCY', 'Scheggerott u Flensburgu (Německo)', '10,144 (omezeně i 3,579)',
     'nepřetržitě vysílá údaje o geomagnetické aktivitě a výstrahy před polární září'),
    ('OZ7IGY', 'Jystrup (Dánsko), JO55WM', '28,271 / 40,071 / 50,471 / 70,021 / 144,471 / 432,471 / 1296,930 … 24 048,930',
     'nejstarší VKV/UKV maják na světě (od Mezinárodního geofyzikálního roku 1957), 12 pásem'),
]

NOTE = ('Stav jednotlivých majáků se mění (výpadky, přesuny). Aktuální stav sítě NCDXF/IARU ukazuje tabulka na '
        'ncdxf.org. České majáky jsou hlavně na VKV a UKV (značky OK0E…, seznam vede Český radioklub). Například '
        'OK0EA Janské Lázně (432,466 MHz a pásma 1,3–76 GHz), OK0EB České Budějovice / Kleť (144,446 MHz a další), '
        'OK0EK Kelčský Javorník a OK0EKL Klínovec (pásma od 1 296 MHz). Majáky se v kmitočtových plánech IARU '
        'umisťují do vyhrazených úseků, které mají ostatní stanice ponechat volné.')
