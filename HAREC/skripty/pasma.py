# -*- coding: utf-8 -*-
"""Amatérská pásma: označení v metrech -> kmitočtový rozsah v MHz.

Rozsahy podle přílohy 1 vyhl. č. 156/2005 Sb. (pásma, která vyhláška neuvádí, jsou označena poznámkou).
BAND_NOTES: otázky ČTÚ, v jejichž textu je pásmo vyjádřeno v metrech – k nim se automaticky vypíše
vysvětlivka s kmitočty (text otázky/odpovědi ČTÚ se nemění).
Ve vlastních textech (praxe, spektra, šíření, obrázky…) se kmitočet doplňuje přímo do textu v závorce.
"""

MHZ = {
    '2200 m': '0,1357–0,1378 MHz',
    '160 m': '1,810–2,000 MHz',
    '80 m': '3,500–3,800 MHz',
    '40 m': '7,000–7,200 MHz',
    '30 m': '10,100–10,150 MHz',
    '20 m': '14,000–14,350 MHz',
    '17 m': '18,068–18,168 MHz',
    '15 m': '21,000–21,450 MHz',
    '12 m': '24,890–24,990 MHz',
    '10 m': '28,000–29,700 MHz',
    '6 m': '50–52 MHz',
    '4 m': '≈ 70 MHz (vyhl. 156/2005 Sb. ho neuvádí)',
    '2 m': '144–146 MHz',
    '70 cm': '430–440 MHz',
    '23 cm': '1 240–1 300 MHz',
    '13 cm': '2 300–2 450 MHz',
    '9 cm': '3 400–3 410 MHz',
    '6 cm': '5 650–5 850 MHz',
    '3 cm': '10 000–10 500 MHz',
    '1,2 cm': '24 000–24 250 MHz',
}

# (část, oddíl, číslo) -> pásma zmíněná v otázce nebo odpovědi ČTÚ
BAND_NOTES = {
    ('radiokomunikační předpisy', 'c', 32): ['2 m'],
    ('radiokomunikační provoz', 'a', 41): ['30 m', '17 m', '12 m'],
    ('elektrotechnika a radiotechnika', 'g', 3): ['160 m', '80 m', '40 m'],
    ('elektrotechnika a radiotechnika', 'g', 4): ['70 cm'],
    ('elektrotechnika a radiotechnika', 'g', 10): ['20 m'],
    ('elektrotechnika a radiotechnika', 'g', 16): ['3 cm', '6 cm', '13 cm', '23 cm', '70 cm', '2 m', '6 m'],
}
# předpisy c) 31 (pásmo 6 m) – kmitočet už uvádí poznámka k otázce


def note(key):
    bands = BAND_NOTES.get(key)
    if not bands:
        return None
    return '; '.join(f'{b} = {MHZ[b]}' for b in bands) + '.'
