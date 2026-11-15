# HAREC A – otázky ČTÚ s výňatky z předpisů

Výstup: `HAREC_A_otazky_s_predpisy.odt` – všechny otázky pro průkaz HAREC třídy A (verze ČTÚ 05/2026),
správná odpověď a doslovné výňatky z předpisů, které odpověď zdůvodňují. Sestaveno 11. 11. 2026, aktualizováno 15. 11. 2026 – obrázky k elektrotechnice c)–f), pásma v MHz; dříve 14. 11. 2026 (ověřena aktuálnost + seznam zkratek + příloha s výtahem z CEPT T/R 61-01/61-02).

## Struktura
- `zdroje/ctu/` – PDF otázek ČTÚ (`amaterske_zkousky_faq_05-2026.pdf`) a text (`pdftotext -layout`)
- `zdroje/predpisy_cz/` – zákon 127/2005, vyhlášky 155, 156, 157/2005 Sb. (HTML ze zakonyprolidi.cz + text)
- `zdroje/itu/` – Radio Regulations 2024 Vol. 1 a 2 (PDF + text), ITU-R M.1172 (Q kódy, zkratky)
- `zdroje/cept/` – T/R 61-01 (vyd. 10/2024), T/R 61-02 (vyd. 02/2024)
- `zdroje/iaru/` – IARU R1 HF band plan (2020), VHF Handbook v10.03 (02/2026)
- `skripty/parse_faq.py` – rozparsuje text ČTÚ (jen třída A) → `data/faq.json`
- `skripty/excerpts.py` – knihovna výňatků `X[klíč] = (zdroj, text, pracovní překlad|None)`
- `skripty/zkratky.py` – seznam zkratek podle oblastí (`AREAS`); význam `None` = doslovně z odpovědi ČTÚ
  (provoz d, e), `'+text'` = ČTÚ + doplněk; třídy vysílání (`EMISSIONS`) se dekódují z přílohy 2 vyhl. 156.
  Při sestavení vypíše VAROVÁNÍ, pokud některá zkratka ČTÚ není zařazena do oblasti.
  Digitální druhy provozu (`DIGITAL`) a třídy vysílání s 3. znakem B/D jsou v tabulkách podbarveny žlutě (`table(..., hl=)` v build.py).
- `skripty/cept_vytah.py` – stručný český výtah z T/R 61-01 a T/R 61-02 (příloha na konci dokumentu): srovnávací
  tabulka `COMPARE` + `DOCS` (bloky 'h', 'p', 'ul', 'tab'); odkazy `[→ b) n]` = otázky Předpisy b). Shrnutí, ne doslovný překlad.
- `skripty/spektra.py` – schematická spektra tříd vysílání (SVG bez externích knihoven, vkládá se do ODT za seznam
  zkratek jako kapitola „Druhy provozu ve spektru“); panely v `PANELS` (prvky car/sup/band/ln/curve/filt/bw).
- `skripty/sireni.py` – kapitola „Šíření rádiových vln“ za spektry: názorné scény (přímá viditelnost, odraz/ohyb/průchod
  překážkou, troposférický kanál, EME/MS/aurora/družice) a grafy (druhy šíření podle kmitočtu, vrstvy ionosféry,
  skok a pásmo ticha, MUF/LUF, sluneční cyklus, pokles pole 1/d); odkazy [→ g) n] na otázky elektrotechnika g).
  Texty v SVG se escapují (znak „<“ jinak rozbije obrázek).
- `skripty/azimut.py` – mapa v Mercatorově projekci se středem nad Prahou (výřez 62° z. d. – 91° v. d., tj. začátek
  Ameriky až Indie) se směry z otázek provoz c) 1–7 jako ortodromy s výchozím azimutem ČTÚ; cíle mimo výřez jen šipkou.
  Vkládá se za otázku c) 7. Obrysy pevnin ručně zjednodušené v `LAND`/`ISLANDS`/`WATER` (lon, lat); azimuty ČTÚ
  ověřeny výpočtem ortodromy (±5°). Uživatel zvolil Mercator místo azimutální projekce.
- `skripty/majaky.py` – tabulka nejznámějších majáků (max. 20: 18 NCDXF/IARU + DK0WCY + OZ7IGY) za otázkou provoz c) 25;
  zdroje a datum ověření v hlavičce modulu, české majáky podle seznamu ČRK.
- `skripty/praxe.py` – „Z praxe:“ krátká praktická vysvětlení ke všem 140 otázkám provoz e) (zkratky), `PRAXE_E[číslo]`.
- `skripty/praxe_q.py` – totéž pro provoz d) Q kódy (21 otázek), `PRAXE_D[číslo]`.
- `skripty/obrazky_elek.py` – názorné obrázky (SVG) ke všem otázkám elektrotechnika c)–f) (56 ks): schémata, grafy,
  spektra, blokové diagramy + popisek. `FIGS[(oddíl, pořadí)]`, pořadí = 0-based pozice v oddílu (c) má dvě otázky č. 1).
  Vkládá se za správnou odpověď (rámec 15 cm). Náhledy: `python3 -I skripty/obrazky_elek.py VÝST_SLOŽKA`.
  Osciloskop (průběhy v čase, tmavá obrazovka, CH1–CH4): funkce `scope(f, y0, [(popis, odečet, fn(t))], env=…, note=…)`,
  výška `scope_h(počet_kanálů)`. Použito u c) 6, 9; d) 3, 5, 6, 8, 9, 11; e) 3, 4, 5, 9 (průběhy počítané násobením
  signálů, časové měřítko schematické). Uživatel chce osciloskop u všech otázek o modulaci/směšování/přijímačích, kde dává smysl.
- `skripty/obrazky_sireni_q.py` – obrázky ke všem 17 otázkám elektrotechnika g) Šíření (`FIGS_G[('g', pořadí)]`), kreslicí
  pomůcky (F, freqaxis…) z `obrazky_elek`; `obrazky_elek.figure()` je pro oddíl g načítá odsud. Hodnoty orientační.
- `skripty/spektrum_pasma.py` – závěrečná příloha „Kmitočtové spektrum 0–6 GHz a radioamatérská pásma“ (7 grafů s
  lineární osou, `CHARTS`): amatérská pásma modře (`HAM_BANDS`, vyhl. 156; 630 m, 60 m, 4 m čárkovaně – ve vyhlášce nejsou),
  ostatní služby šedě (`OTHER`, orientačně podle RR čl. 5 R1 + běžné využití; hranice KV ověřeny v RR2024_Vol1.txt),
  překrývající se služby automaticky pod sebou, úzké sloupce se zkratkou (`CODES`) a legendou.
  Šedé služby mají v rámečku i rozsah kmitočtů (u úzkých svisle „zkratka rozsah“, výška řádku podle nejdelšího popisku).
  Amatérská pásma barevně podle šíření (`CAT`, `BAND_CAT`: přízemní vlna / odraz od ionosféry / odraz jen výjimečně /
  přímá viditelnost; pásmo se dvěma druhy je rozděleno), fialový pruh nahoře = aurora (`AURORA`). První graf `overview()`
  (log. osa) vysvětluje barvy.
- `skripty/pasma.py` – pásma v metrech → MHz (`MHZ`, podle přílohy 1 vyhl. 156/2005; 4 m tam není → „≈ 70 MHz“).
  `BAND_NOTES` = otázky ČTÚ zmiňující pásmo v m → „Vysvětlivka:“ za odpovědí (text ČTÚ se nemění).
  **Pravidlo uživatele (platí pro celý text):** všude, kde je pásmo v metrech, uvést i kmitočet v MHz – ve vlastních
  textech (praxe, spektra, šíření, obrázky, pracovní překlady) přímo v závorce; doslovné výňatky se nemění.
  Pozor: ČTÚ někdy píše pásmo slovem („20 metrů“, g) 10) – při kontrole hledat i „metr…/centimetr…“.
- Úvodní oddíl „Jak probíhá zkouška“ (v `build.py` před Úvodem) – podle vyhl. 157/2005, Zkušebního řádu ČTÚ
  03/2023 (`zdroje/ctu/zkusebni_rad/`) a webu ČTÚ (poplatek 600 Kč, ověřeno 14. 11. 2026).
- `skripty/build.py` – přiřazení výňatků k otázkám + seznam zkratek (za úvodem) + generování ODT (odfpy)

## Postup sestavení (opakovatelný)
```
cd ~/Desktop/HAREC
python3 -I skripty/parse_faq.py zdroje/ctu/faq.txt data/faq.json
python3 -I skripty/build.py ~/Desktop/HAREC ~/Desktop/HAREC/HAREC_A_otazky_s_predpisy.odt
soffice --headless --convert-to pdf HAREC_A_otazky_s_predpisy.odt   # PDF generovat vždy spolu s ODT
```
Nikdy needitovat ODT ručně, pokud se bude znovu generovat – měnit skripty.

## Jak upravovat
- **Přiřazení výňatků k otázce:** v `build.py` volání `m(ČÁST, oddíl, číslo, [klíče], 'poznámka')`.
  Části: `PRED` (předpisy), `PROV` (provoz), `ELEK` (elektrotechnika). Oddíl = písmeno.
- **Nový výňatek:** přidat do `excerpts.py` (text doslovně z `zdroje/…`, u EN předpisů přidat pracovní překlad).
- **Zkrácené výňatky tabulky přílohy 1 vyhl. 156:** `p1_sub('P1_xx', [podřetězce řádků])` v `build.py`.
- **Automatické výňatky:** Q kódy (oddíl d) a zkratky (e) z M.1172 – funkce `qcode()`, `abbr()`;
  prefixy (f) z RR dodatku 42 – `ap42_lookup()`; KV plán IARU – `hf_band()`;
  VKV plán je ručně přepsán v `BANDS` (automatický převod PDF byl nečitelný).
- **Opravy chyb extrakce PDF** (horní indexy, symboly Ω, λ, ∞): slovník `FIX` v `build.py`, mapování PUA
  znaků v `parse_faq.py` (`PUA`).
- **Poznámky k celým oddílům:** `NOTE_NOLAW` v `build.py`.

## Zjištění / zvláštnosti (důležité při úpravách)
- V PDF ČTÚ je v části „provoz“ oddíl Q kódů chybně označen jako „c)“ – skript ho přejmenovává na d).
- V oddílu elektrotechnika c) jsou v originále dvě otázky s číslem 1 – ponecháno.
- Vyhl. 156/2005 Sb. nebyla novelizována (znění od 1. 5. 2005). V tabulce přílohy 1 je pro
  3 500–3 800, 7 000–7 100 a 7 100–7 200 kHz jedna společná buňka „P S VII)“; pozn. VII: od 30. 3. 2009 status P.
- Otázka předpisy c) 16 (7 105 kHz, závod → 750 W) vs. § 4 odst. 4 (1 500 W jen na *mezinárodním* závodě) – vysvětleno poznámkou.
- QRJ: ČTÚ uvádí historický amatérský význam; M.1172 má dnes jiný význam – poznámka v dokumentu.
- Odpovědi ČTÚ k rozdělení pásem se místy liší od aktuálních plánů IARU (např. EME 144,110–144,160 MHz
  v aktuálním plánu vs. „úsek není určen“ u ČTÚ). Pro zkoušku platí odpověď ČTÚ, v úvodu dokumentu je upozornění.
- Elektrotechnika: bez výňatků (nelze zdůvodnit předpisy) – jen otázka + odpověď.
- Aktuálnost ověřena 14. 11. 2026: ČTÚ 05/2026 stále platná (stránka ctu.gov.cz/prukazy-zkousky ještě odkazuje
  na starší 06-2025, novější je ve složce /obsah/Prukazy/); zákon 127/2005 znění od 1. 11. 2026 (v53), vyhl. 155 a 157
  znění od 23. 8. 2023, vyhl. 156 bez novel – vše shodné se staženými zdroji.
- Průběžně kontrolovat aktuálnost: nová verze otázek ČTÚ (stránka „Průkazy“ na ctu.gov.cz), znění vyhlášek na zakonyprolidi.cz.

## Preference uživatele
- Komunikace česky. Výstupní formát ODT. Vše (zdroje, skripty, výstup, poznámky) držet v `~/Desktop/HAREC`.
