# HAREC A – otázky ČTÚ s výňatky z předpisů

Výstup: `HAREC_A_otazky_s_predpisy.odt` – všechny otázky pro průkaz HAREC třídy A (verze ČTÚ 05/2026),
správná odpověď a doslovné výňatky z předpisů, které odpověď zdůvodňují. Sestaveno 11. 11. 2026, aktualizováno 27. 11. 2026 – doplňky podle e-booků (S-metr, Z praxe c), vysvětlivky i), tahák vzorců), ověřena aktuálnost ČTÚ; 20. 11. 2026 – příloha pásma podle druhů provozu; 16. 11. 2026 – mapy prefixů podle kontinentů; 15. 11. 2026 – obrázky k elektrotechnice c)–f), pásma v MHz; dříve 14. 11. 2026 (ověřena aktuálnost + seznam zkratek + příloha s výtahem z CEPT T/R 61-01/61-02).

## Struktura
- `zdroje/ctu/` – PDF otázek ČTÚ (`amaterske_zkousky_faq_05-2026.pdf`) a text (`pdftotext -layout`)
- `zdroje/predpisy_cz/` – zákon 127/2005, vyhlášky 155, 156, 157/2005 Sb. (HTML ze zakonyprolidi.cz + text)
- `zdroje/itu/` – Radio Regulations 2024 Vol. 1 a 2 (PDF + text), ITU-R M.1172 (Q kódy, zkratky)
- `zdroje/cept/` – T/R 61-01 (vyd. 10/2024), T/R 61-02 (vyd. 02/2024)
- `zdroje/geo/` – Natural Earth 1:50m Admin 0 Countries v5.1.2 (GeoJSON, volné dílo) pro mapy prefixů
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
- `skripty/mapy_prefixu.py` – kapitola „Mapy prefixů podle kontinentů“ (6 map, každá na 1 stranu A4: Evropa, Asie, Afrika,
  S. a Stř. Amerika, J. Amerika, Austrálie a Oceánie), vkládá se těsně před oddíl provoz f) (`add_prefix_maps` v build.py).
  **Uživatel chce jen prefixy z otázek ČTÚ** (provoz f), text přesně podle odpovědi ČTÚ; ostatní státy šedé bez popisku.
  `ENTRIES[č. otázky] = (ADM0_A3 | None, kotva)` – None = bodové území (ostrov, část UK…); `ON_MAPS` = na které mapě
  (výchozí Evropa); `ANCHOR_MAP` kotvy pro konkrétní mapu; `MAPS` = střed projekce (LAEA) + body, které musí být vidět.
  Popisky: uvnitř státu, pokud se vejdou (maska ≥ 85 %), jinak rámeček s odkazovou čarou (hledání s penalizací za
  zakrytí zvýrazněných států a křížení čar); území mimo výřez → popisek u okraje se šipkou (jen ←↑→↓, diagonální LO neumí).
  Náhledy: `python3 -I skripty/mapy_prefixu.py . VÝST_SLOŽKA` (+ `google-chrome --headless --screenshot`).
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
- `skripty/pasma_provoz.py` – poslední příloha „Radioamatérská pásma podle druhů provozu“ (za spektrem 0–6 GHz): legenda
  + 1 graf na pásmo (lineární osa, KV v kHz, jinak MHz). Pruh „IARU R1“ = zjednodušený plán IARU (kategorie `CAT`:
  cw/nb/dig/fone/fm/bcn/sat/atv/wide/gap), oříznutý na rozsah vyhl. 156; pruh „ČTÚ“ = úseky přesně podle odpovědí
  provoz a) s číslem otázky (překrývající se úseky pod sebou); trojúhelníky = centra aktivity IARU; `zoom` = detail(y)
  úzkých úseků (70 cm, 23 cm – dva detaily A/B, 13 cm, 6 cm). Data v `BANDS`. Náhledy: `python3 -I skripty/pasma_provoz.py VÝST_SLOŽKA`.
- `skripty/pasma.py` – pásma v metrech → MHz (`MHZ`, podle přílohy 1 vyhl. 156/2005; 4 m tam není → „≈ 70 MHz“).
  `BAND_NOTES` = otázky ČTÚ zmiňující pásmo v m → „Vysvětlivka:“ za odpovědí (text ČTÚ se nemění).
  **Pravidlo uživatele (platí pro celý text):** všude, kde je pásmo v metrech, uvést i kmitočet v MHz – ve vlastních
  textech (praxe, spektra, šíření, obrázky, pracovní překlady) přímo v závorce; doslovné výňatky se nemění.
  Pozor: ČTÚ někdy píše pásmo slovem („20 metrů“, g) 10) – při kontrole hledat i „metr…/centimetr…“.
- Úvodní oddíl „Jak probíhá zkouška“ (v `build.py` před Úvodem) – podle vyhl. 157/2005, Zkušebního řádu ČTÚ
  03/2023 (`zdroje/ctu/zkusebni_rad/`) a webu ČTÚ (poplatek 600 Kč, ověřeno 14. 11. 2026).
- `skripty/doplnky.py` – doplňky inspirované e-booky v `../ebooks/` („Radioamatér – vizuální průvodce“ + 2 bonusy), **přepracované
  podle ČTÚ** (otázky ČTÚ mají vždy přednost, data z e-booků v rozporu s ČTÚ se nepřejímají; obrázky se nekopírují):
  S-metr a report RST za otázkou provoz c) 18 (`smeter_figure`, `S_ROWS` podle IARU R.1, `RST_ROWS`); `PRAXE_C` = „Z praxe:“
  k provoz c) 12, 13, 17, 18, 21; `VYSV_I` = vysvětlivky k elektrotechnika i) 1, 3 (zádrž vs. propust); `TAHAK` = poslední
  příloha „Tahák: vzorce a čísla k výpočtovým otázkám“ (jen vzorce potřebné k otázkám ČTÚ, s odkazy na otázky).
  Zjištěné rozpory e-booků s ČTÚ: bezpečné stříd. napětí „50 V“ (ČTÚ j) 1: 25 V / ss 60 V); deník pro všechny (ČTÚ předpisy c) 2:
  jen klubové stanice); 20 m (14 MHz) fonie až od 14 112 kHz (ČTÚ provoz a) 15: 14 101–14 350); TVI „horní propust“ (ČTÚ i) 3:
  „dolnofrekvenční zádrž“ – totéž, jiný název); jen mezinárodní hláskování (vyhl. 155: vnitrostátně i česká); F2 ≈ 150 km (chyba).
  Cvičné testy z e-booků nejsou otázky ČTÚ – nepřebírat.
- `skripty/build.py` – přiřazení výňatků k otázkám + seznam zkratek (za úvodem) + generování ODT (odfpy)

## Postup sestavení (opakovatelný)
```
cd ~/Desktop/hamradio/HAREC
python3 -I skripty/parse_faq.py zdroje/ctu/faq.txt data/faq.json
python3 -I skripty/build.py ~/Desktop/hamradio/HAREC ~/Desktop/hamradio/HAREC/HAREC_A_otazky_s_predpisy.odt
soffice --headless --convert-to pdf HAREC_A_otazky_s_predpisy.odt   # PDF generovat vždy spolu s ODT
```
Na tomto PC (Python 3.10) není odfpy systémově – použít venv s `pip install odfpy` (např. ve scratchpadu) a spouštět jeho python.
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
- Aktuálnost ověřena 27. 11. 2026 (PDF 05/2026 na webu bajtově shodné s `zdroje/ctu/`, novější verze neexistuje); dříve 14. 11. 2026: ČTÚ 05/2026 stále platná (stránka ctu.gov.cz/prukazy-zkousky ještě odkazuje
  na starší 06-2025, novější je ve složce /obsah/Prukazy/); zákon 127/2005 znění od 1. 11. 2026 (v53), vyhl. 155 a 157
  znění od 23. 8. 2023, vyhl. 156 bez novel – vše shodné se staženými zdroji.
- Průběžně kontrolovat aktuálnost: nová verze otázek ČTÚ (stránka „Průkazy“ na ctu.gov.cz), znění vyhlášek na zakonyprolidi.cz.

## Preference uživatele
- Komunikace česky. Výstupní formát ODT. Vše (zdroje, skripty, výstup, poznámky) držet v `~/Desktop/hamradio/HAREC`.
