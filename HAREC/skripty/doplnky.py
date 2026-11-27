# -*- coding: utf-8 -*-
"""Doplňky inspirované e-booky „Radioamatér – vizuální průvodce“ (ebooks/), ale přepracované podle otázek ČTÚ.

Zásada: odpovědi ČTÚ mají vždy přednost. Z e-booků se nepřejímá nic, co je s ČTÚ v rozporu
(např. „bezpečné střídavé napětí do 50 V“ – ČTÚ j) 1: 25 V; deník u každé stanice – ČTÚ předpisy c) 2:
jen klubové stanice; fonie na 20 m (14 MHz) až od 14 112 kHz – ČTÚ provoz a) 15: 14 101–14 350 kHz).
Obrázky e-booků se nekopírují, vše je nakresleno znovu.

- S-metr a report RST: obrázek + tabulky za otázkou provoz c) 18 (`smeter_figure`, `S_ROWS`, `RST_ROWS`)
- PRAXE_C[číslo] – „Z praxe:“ k otázkám provoz c) (reporty, dotaz na volný kmitočet, průběh spojení)
- VYSV_I[číslo] – „Vysvětlivka:“ k otázkám elektrotechnika i) (názvy filtrů zádrž/propust)
- TAHAK – příloha „Tahák: vzorce a čísla k výpočtovým otázkám“ (jen to, co potřebují otázky ČTÚ)

Hodnoty S-metru podle IARU Region 1 Technical Recommendation R.1 (S9 = −73 dBm na KV, −93 dBm na VKV,
1 stupeň S = 6 dB) – shodné s odpověďmi ČTÚ provoz c) 17 a 18.
"""
import math
from obrazky_elek import F, BL, RED, GR, TX, GRN

# ---------------------------------------------------------------- S-metr
SM_TITLE = 'S-metr a report RST – kolik mikrovoltů je „S9“'
SM_INTRO = ('Otázky c) 17 a 18 vyžadují převod stupně S na napětí na vstupu přijímače. Stupnice S-metru je podle doporučení '
            'IARU Region 1 (Technical Recommendation R.1) logaritmická: S9 odpovídá na KV (pod 30 MHz) napětí 50 µV na 50 Ω '
            '(−73 dBm), na VKV (nad 30 MHz) desetkrát menšímu napětí 5 µV (−93 dBm). Každý stupeň S je 6 dB, tj. dvojnásobek '
            '(polovina) napětí. Silnější signály než S9 se udávají v decibelech nad S9 (např. „S9 + 20 dB“).')


def smeter_figure():
    f = F(400)
    cx, cy, R = 250, 300, 200
    lo, hi = -121, -13                      # S1 … S9+60 dB (KV, dBm)
    a0, a1 = math.radians(155), math.radians(25)

    def ang(dbm):
        return a0 + (a1 - a0) * (dbm - lo) / (hi - lo)

    def pt(dbm, r):
        a = ang(dbm)
        return cx + r * math.cos(a), cy - r * math.sin(a)

    f.rect(30, 40, 440, 300, fill='#fbf8ee', stroke=TX, rx=14)
    f.path([pt(lo + (hi - lo) * i / 120, R) for i in range(0, 121) if lo + (hi - lo) * i / 120 <= -73], c=TX, w=2.5)
    f.path([pt(d, R) for d in range(-73, hi + 1)], c=RED, w=5)
    for s in range(1, 10):
        d = -73 - 6 * (9 - s)
        x1, y1 = pt(d, R); x2, y2 = pt(d, R - (18 if s % 2 else 12))
        f.l(x1, y1, x2, y2, w=2)
        if s % 2 or s in (8,):
            x, y = pt(d, R + 20); f.t(x, y + 5, str(s), size=15, w='bold')
    for p in (10, 20, 40, 60):
        d = -73 + p
        x1, y1 = pt(d, R); x2, y2 = pt(d, R - 16)
        f.l(x1, y1, x2, y2, c=RED, w=2)
        x, y = pt(d, R + 22); f.t(x, y + 5, f'+{p}', size=14, c=RED, w='bold')
    # ručka na S8 (report „588“, otázka c 17)
    x, y = pt(-79, R - 30)
    f.arrow([(cx, cy), (x, y)], c=BL, w=3)
    f.circle(cx, cy, 7, fill=TX)
    f.t(cx, cy + 28, 'S', size=20, w='bold')
    f.t(cx - 150, cy + 28, '1 S = 6 dB', size=13, c=GR)
    f.t(cx + 150, cy + 28, 'dB nad S9', size=13, c=RED)
    # popisky vpravo
    x0 = 500
    f.t(x0, 60, 'KV (pod 30 MHz)', size=16, w='bold', anchor='start', c=BL)
    f.t(x0, 86, 'S9 = 50 µV na 50 Ω (−73 dBm)', size=14, anchor='start')
    f.t(x0, 108, 'S8 = 25 µV  → report 588, c) 17', size=14, anchor='start', c=BL, w='bold')
    f.t(x0, 150, 'VKV (nad 30 MHz)', size=16, w='bold', anchor='start', c=GRN)
    f.t(x0, 176, 'S9 = 5 µV na 50 Ω (−93 dBm)', size=14, anchor='start')
    f.t(x0, 198, '→ report 599, c) 18', size=14, anchor='start', c=GRN, w='bold')
    f.t(x0, 240, 'o 1 stupeň níž = ½ napětí', size=14, anchor='start')
    f.t(x0, 262, '(¼ výkonu, −6 dB)', size=14, anchor='start', c=GR)
    f.t(x0, 296, 'S9 + 20 dB = 10× napětí', size=14, anchor='start', c=RED)
    f.t(x0, 318, '(KV: 500 µV)', size=14, anchor='start', c=GR)
    f.t(380, 380, 'Ručka ukazuje S8 – v reportu RST „588“ je to druhá číslice (síla signálu).', size=13, c=GR)
    return f.done(), f.w, f.h


SM_CAPTION = ('Stupnice S-metru podle IARU R.1. Skutečné S-metry bývají často nepřesné (zejména pod S5 a nad S9), proto se report '
              'má dávat podle skutečného dojmu ze signálu – automatické „59“ nic neříká.')

# (stupeň, KV µV, KV dBm, VKV µV, VKV dBm)
S_ROWS = [
    ('S9 + 40 dB', '5 000 µV (5 mV)', '−33', '500 µV', '−53'),
    ('S9 + 20 dB', '500 µV', '−53', '50 µV', '−73'),
    ('S9 + 10 dB', '158 µV', '−63', '15,8 µV', '−83'),
    ('S9', '50 µV', '−73', '5 µV', '−93'),
    ('S8', '25 µV', '−79', '2,5 µV', '−99'),
    ('S7', '12,6 µV', '−85', '1,26 µV', '−105'),
    ('S6', '6,3 µV', '−91', '0,63 µV', '−111'),
    ('S5', '3,2 µV', '−97', '0,32 µV', '−117'),
    ('S4', '1,6 µV', '−103', '0,16 µV', '−123'),
    ('S3', '0,8 µV', '−109', '0,08 µV', '−129'),
    ('S2', '0,4 µV', '−115', '0,04 µV', '−135'),
    ('S1', '0,2 µV', '−121', '0,02 µV', '−141'),
]
S_HEADER = ['Stupeň', 'KV – napětí na 50 Ω', 'KV dBm', 'VKV – napětí na 50 Ω', 'VKV dBm']
S_NOTE = ('Podbarvené řádky jsou z otázek ČTÚ: c) 17 – report 588 na KV → S8 = 25 µV; c) 18 – report 599 na VKV → S9 = 5 µV. '
          'Pamatovat stačí S9 (KV 50 µV, VKV 5 µV) a pravidlo „o stupeň níž = poloviční napětí“.')

RST_ROWS = [
    ('R – čitelnost (1–5)', '1 nečitelný · 2 čitelný jen chvílemi · 3 čitelný se značnými obtížemi · 4 čitelný prakticky bez obtíží · '
     '5 dokonale čitelný'),
    ('S – síla (1–9)', '1 sotva slyšitelný · 2 velmi slabý · 3 slabý · 4 dostatečný · 5 docela dobrý · 6 dobrý · 7 středně silný · '
     '8 silný · 9 velmi silný'),
    ('T – tón (1–9, jen CW a digitální provoz)', '1 velmi drsný, chraptivý · 2–4 drsný střídavý tón (od nehudebního po trochu '
     'hudební) · 5 hudebně modulovaný · 6 modulovaný s nádechem pískání · 7 téměř čistý, s jemným zvlněním · '
     '8 čistý tón s nádechem střídavé složky (ČTÚ c) 17) · 9 zcela čistý tón (ČTÚ c) 18)'),
]
RST_HEADER = ['Číslice', 'Význam jednotlivých stupňů']
RST_NOTE = ('Při fonickém provozu (SSB, FM) se tón nehodnotí – report má jen dvě číslice (např. 59), při telegrafii tři (např. 599). '
            'ČTÚ c) 12: RST = čitelnost, síla signálu a tón.')

# ---------------------------------------------------------------- Z praxe k provozu c)
PRAXE_C = {
    12: 'Report se dává hned v první relaci po navázání spojení: fonicky „you are 5 9“ (dvě číslice, tón se nehodnotí), '
        'telegraficky „UR RST 599“. Podrobná tabulka stupňů R, S a T je za otázkou c) 18.',
    13: 'Než zavoláte výzvu, chvíli poslouchejte a pak se zeptejte, zda je kmitočet volný – telegraficky „QRL?“, fonicky '
        '„Is this frequency in use?“ (česky „Je kmitočet volný?“). Ticho nestačí: probíhající spojení můžete slyšet jen '
        'jednu stranu, nebo vůbec ne (pásmo ticha), a protistanice přesto slyší vás. Odpověď „QRL“ / „yes“ / „occupied“ '
        'znamená obsazeno – přelaďte jinam.',
    17: 'Druhá číslice reportu je síla podle S-metru. Na KV je S9 = 50 µV na 50 Ω a každý stupeň S je 6 dB (polovina napětí): '
        'S8 = 25 µV. Třetí číslice 8 = „čistý tón s nádechem střídavé složky“. Tabulka hodnot je za otázkou c) 18.',
    18: 'Na VKV (nad 30 MHz) je S9 = 5 µV na 50 Ω, tedy desetkrát méně než na KV – VKV přijímače jsou citlivější a šum '
        'pásma je nižší. Report 599 = čitelnost 5 (dokonale čitelné), síla 9, tón 9 (zcela čistý).',
    21: 'Typický průběh spojení: 1) poslech a dotaz „Is this frequency in use?“ (CW „QRL?“); 2) výzva „CQ CQ CQ de OK1ABC '
        'OK1ABC …“ (fonicky značku hláskovat mezinárodní abecedou: Oscar Kilo One Alfa Bravo Charlie); 3) odpověď protistanice, '
        'výměna reportu RST, jména (OP) a stanoviště (QTH); 4) poděkování, „73“ a rozloučení se značkami obou stanic. '
        'Čas spojení se uvádí v UTC (SEČ = UTC + 1 h, SELČ = UTC + 2 h). Staniční deník je podle ČTÚ (předpisy c) 2) '
        'povinný jen u klubových stanic; vlastní deník se ale vyplatí vést i jinak (QSL lístky, závody, řešení rušení).',
}

# ---------------------------------------------------------------- vysvětlivky k elektrotechnice i)
VYSV_I = {
    1: 'Názvy filtrů podle toho, co filtr zadrží: „hornofrekvenční zádrž“ zadrží vysoké kmitočty (harmonické) a propustí nízké '
       '– jde tedy o dolní propust (DP). Zařazuje se na výstup vysílače mezi vysílač a anténu; např. při vysílání na 7 MHz '
       'utlumí 2. a 3. harmonickou na 14 a 21 MHz.',
    3: 'Názvy filtrů podle toho, co filtr zadrží: „dolnofrekvenční zádrž“ zadrží nízké (krátkovlnné) kmitočty a propustí vyšší '
       'kmitočty televizního příjmu – jde tedy o horní propust (HP), jak ji označují jiné příručky. Zařazuje se na anténní vstup '
       'televizoru, často spolu s feritovým kroužkem na kabelu. U zkoušky platí název podle ČTÚ: dolnofrekvenční zádrž.',
}

# ---------------------------------------------------------------- tahák
TAHAK_TITLE = 'Tahák: vzorce a čísla k výpočtovým otázkám'
TAHAK_INTRO = ('Přehled vzorců a hodnot, které potřebují otázky ČTÚ (odkazy v posledním sloupci: E = elektrotechnika, '
               'P = provoz, Př = předpisy). U písemného testu není povolena kalkulačka, proto jsou příklady voleny tak, '
               'aby šly spočítat zpaměti – zaokrouhlujte. Hodnoty u bezpečnosti jsou přesně podle odpovědí ČTÚ; jiné příručky '
               'někdy uvádějí odlišná čísla (např. „bezpečné střídavé napětí do 50 V“), u zkoušky platí ČTÚ.')

# (skupina, [(vzorec / hodnota, použití – příklad, otázky ČTÚ)])
TAHAK = [
    ('Jednotky a předpony', [
        ('p 10⁻¹² · n 10⁻⁹ · µ 10⁻⁶ · m 10⁻³ · k 10³ · M 10⁶ · G 10⁹',
         'mezi sousedními předponami je krok 1 000: 1 833 kHz = 1,833 MHz; 1,5 nF = 1 500 pF', 'E a) 5, 6; E b) 3'),
        ('kód 1M2, 4k7, 2R2', 'písmeno nahrazuje desetinnou čárku a určuje násobek: 1M2 = 1,2 MΩ = 1 200 000 Ω', 'E b) 4'),
    ]),
    ('Ohmův zákon a výkon', [
        ('U = R · I · I = U / R · R = U / I', '10 V / 2 A = 5 Ω (mA převeďte na A!)', 'E a) 10, 21'),
        ('P = U · I = I² · R = U² / R', '12 V · 12 A = 144 W; I = P / U = 24 W / 12 V = 2 A', 'E a) 8, 11, 20'),
        ('t = Q / I (kapacita akumulátoru v Ah)', '4 Ah / 0,4 A = 10 h', 'E a) 9'),
    ]),
    ('Zapojení součástek', [
        ('odpory: sériově R = R1 + R2; paralelně R = R1 · R2 / (R1 + R2)',
         '2 kΩ ∥ 3 kΩ = 6 / 5 = 1,2 kΩ (výsledek je vždy menší než menší z odporů)', 'E c) 2, 4'),
        ('kondenzátory: paralelně C = C1 + C2 + …; sériově 1/C = 1/C1 + 1/C2', '3 × 10 nF paralelně = 30 nF (opačně než odpory)', 'E c) 3'),
        ('X_L = 2π · f · L; X_C = 1 / (2π · f · C)', 'reaktance cívky s kmitočtem roste, kondenzátoru klesá', 'E b) 8, 9'),
        ('rezonance f₀ = 1 / (2π · √(L · C)); prakticky f [MHz] = 159 / √(L [µH] · C [pF])',
         'větší C nebo L → nižší f₀; ideální sériový obvod má na f₀ impedanci 0 Ω, paralelní ∞', 'E c) 1, 12, 13'),
        ('křemíková dioda: prahové napětí ≈ 0,6 V', 'Graetzův můstek = dvoucestný usměrňovač (ze sítě 50 Hz pulzuje 100 Hz)', 'E b) 7; E c) 1'),
    ]),
    ('Kmitočet a vlnová délka', [
        ('c = f · λ; prakticky λ [m] = 300 / f [MHz]', '3,5 MHz → 86 m (pásmo 80 m, 3,5 MHz); 145 MHz → 2,07 m (pásmo 2 m, 144–146 MHz)', 'E a) 7'),
        ('f = 1 / T', 'perioda 20 ms → 1 / 0,02 s = 50 Hz', 'E h) 4'),
        ('vzorkovací kmitočet f_vz ≥ 2 · f_max', 'signál do 3 kHz → vzorkovat aspoň 6 kHz', 'E a) 19'),
        ('harmonické: n · f', 'vysílání na 7,05 MHz → 2. harmonická 14,1 MHz, 3. harmonická 21,15 MHz', 'Př c) 31–34; E i) 1'),
    ]),
    ('Decibely', [
        ('dB = 10 · log(P₂ / P₁)', '+3 dB = 2× · +6 dB = 4× · +10 dB = 10× · +20 dB = 100× výkonu; −3 dB = polovina', 'E a) 22'),
        ('útlumy a zisky se sčítají', 'kabel 12 dB / 100 m, délka 25 m → 3 dB → ze 100 W dojde 50 W', 'E a) 13'),
        ('napětí: 6 dB = 2× napětí, 20 dB = 10× napětí', '1 stupeň S-metru = 6 dB', 'P c) 17, 18; E d) 7'),
    ]),
    ('Přijímač (superhet)', [
        ('f_osc = f_sig ± f_mf', '3,750 MHz + 0,455 MHz = 4,205 MHz (oscilátor nad signálem)', 'E d) 4'),
        ('směšovač dává součet i rozdíl: f_sig ± f_osc', '14,255 − 13,8 = 0,455 MHz (mf); nežádoucí součet 14,255 + 13,8 = 28,055 MHz', 'E d) 6'),
        ('zrcadlový kmitočet f_z = f_sig ± 2 · f_mf', 'oscilátor 4,205 MHz → zrcadlo 3,750 + 2 · 0,455 = 4,660 MHz', 'E d) 8'),
    ]),
    ('Antény a napáječe', [
        ('půlvlnný dipól: celková délka ≈ 0,95 · λ/2 = 142,5 / f [MHz]; rameno ≈ 71 / f [MHz]',
         '3,5 MHz: 71 / 3,5 ≈ 20 m na rameno (celkem ≈ 41 m)', 'E f) 2'),
        ('PSV = Z_větší / Z_menší (čistě odporová zátěž); Γ = (PSV − 1) / (PSV + 1); odražený podíl výkonu = Γ²',
         'PSV 3 → Γ = 0,5 → odrazí se 25 %, do antény přejde ≈ 75 %; PSV 1 = dokonalé přizpůsobení', 'E f) 1, 4'),
        ('pole ve vzdálené zóně: intenzita E ~ 1 / d; hustota výkonu ~ 1 / d²',
         'dvojnásobná vzdálenost → poloviční intenzita pole (ČTÚ: „lineárně“), čtvrtinová hustota výkonu', 'E g) 15'),
        ('S-metr: S9 KV = 50 µV (−73 dBm), S9 VKV = 5 µV (−93 dBm), 1 S = 6 dB', 'S8 na KV = 25 µV', 'P c) 17, 18'),
    ]),
    ('Bezpečnost (čísla přesně podle ČTÚ)', [
        ('bezpečné napětí živých částí: stejnosměrné do 60 V, střídavé do 25 V', 'pro prostředí, které nezvyšuje nebezpečí úrazu', 'E j) 1'),
        ('bezpečný ustálený proud: stejnosměrný do 10 mA, střídavý do 3,5 mA', '', 'E j) 6'),
        ('ochranný vodič: žluto-zelený; prodlužovací přívod pro třídu ochrany I: 3 vodiče', '', 'E j) 2, 9'),
    ]),
    ('Čas', [
        ('UTC; SEČ = UTC + 1 h; SELČ = UTC + 2 h', 'spojení v létě ve 20:15 SELČ → do deníku 18:15 UTC', 'P e) 81'),
    ]),
]
TAHAK_HEADER = ['Vzorec / hodnota', 'Použití – příklad', 'Otázky']
