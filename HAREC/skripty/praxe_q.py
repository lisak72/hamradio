# -*- coding: utf-8 -*-
"""Krátká vysvětlení z praxe k otázkám provoz d) Q kódy (1–21). Klíč = číslo otázky.

Q kód s otazníkem je dotaz, bez otazníku sdělení nebo odpověď. Příklady jsou typické obraty z CW a fone spojení.
"""

PRAXE_D = {
    1: 'QRM = rušení jinými stanicemi (umělé rušení). „UR SIGS 579 BUT QRM“ = slyším vás dobře, ale ruší mě jiná stanice; ve fone se běžně říká „je tu QRM“. Na rozdíl od QRN (atmosférické rušení, otázka 14) jde o rušení způsobené lidmi.',
    2: 'QRO? = mohu (máte) zvýšit výkon?; QRO = zvyšte výkon. Hovorově „QRO stanice“ = stanice s velkým výkonem (s koncovým stupněm). Výkon se zvyšuje jen do mezí oprávnění a jen tolik, kolik je pro spojení třeba.',
    3: 'QRZ = volá vás …; QRZ? = kdo mě volá? Když stanice na výzvu CQ slyší zavolání, ale nerozumí značce, vysílá „QRZ?“. Podle QRZ se jmenuje i známý web s databází radioamatérů (qrz.com).',
    4: 'QRX = počkejte, zavolám vás znovu (v … hodin, na … kHz): „QRX 5 MIN“ = počkejte 5 minut. Používá se např. když operátor musí na chvíli od stanice.',
    5: 'QSB = únik, síla signálu kolísá – typicky při šíření odrazem od ionosféry: „UR SIGS 559 QSB“. Při silném QSB je vhodné opakovat důležité údaje (značku, report).',
    6: 'QRS = vysílejte pomaleji; QRS? = mám vysílat pomaleji? Začínající telegrafista požádá rychlejší protistanici „PSE QRS“. Opak je QRQ (vysílejte rychleji).',
    7: 'QRT = přestaňte vysílat; v praxi hlavně „končím, zavírám stanici“: „TNX QSO, I AM QRT“ = končím vysílání. Výzvu QRT vůči jiné stanici je třeba použít zdvořile (např. když ruší tísňový provoz).',
    8: 'QRP = snižte výkon; QRP? = mám snížit výkon? Hovorově „QRP provoz“ = vysílání malým výkonem (do 5 W v CW, do 10 W PEP v SSB) – populární disciplína, např. „QRP 5 W ES WIRE ANT“.',
    9: 'QRV = jsem připraven; QRV? = jste připraven? Hovorově i „jsem aktivní na pásmu“: „QRV ON 40M CW“; „QRV TMW?“ = budete zítra na pásmu?',
    10: 'QRU = nemám pro vás nic (dalšího); QRU? = máte pro mě něco? Typicky před koncem spojení: „QRU? 73“ = ještě něco? jinak na shledanou.',
    11: 'QSL = potvrzuji příjem; „QSL?“ = potvrzujete příjem? Ve fone „QSL“ = rozuměl jsem. Hovorově také QSL lístek – kartička potvrzující spojení: „PSE QSL VIA BURO“, dnes i elektronicky (LoTW, eQSL).',
    12: 'QRL? = je kmitočet obsazen? – před voláním výzvy CQ se na kmitočtu nejprve zeptáme „QRL?“ (ve fone „is this frequency in use?“). Odpověď „QRL“ nebo „C“ znamená obsazeno, je nutné najít jiný kmitočet.',
    13: 'QTH = stanoviště, poloha: „QTH PRAGUE“, ve fone „my QTH is Prague“. Na VKV se místo názvu obce udává QTH lokátor (např. JO70FC), podle kterého se počítají body v závodech.',
    14: 'QRN = atmosférické (přírodní) rušení – praskání od bouřek, typické v létě na pásmech 160 a 80 m (1,8–2,0 a 3,5–3,8 MHz): „QRN VY BAD“. Proti QRN pomáhá omezovač šumu (NB) nebo přijímací anténa s menším příjmem šumu.',
    15: 'QSO = spojení; QSO? = mohu navázat spojení s … přímo (nebo přes …)? Hovorově „QSO“ = každé radioamatérské spojení: „TNX FER QSO“, „QSO zapsané v deníku“.',
    16: 'QSY = přejděte na jiný kmitočet; QSY? = mám přejít? „QSY 7.020“ = přejděte na 7 020 kHz; „QSY UP 2“ = posuňte se o 2 kHz výš. Používá se k uvolnění kmitočtu nebo k přechodu z volacího kmitočtu.',
    17: 'QSV = vysílejte řadu písmen V (···− ···− ···−) – slouží k naladění nebo ke kontrole signálu protistanicí; v amatérské praxi se dnes používá výjimečně (testovací signál při seřizování).',
    18: 'QSK = mohu poslouchat mezi svými značkami (plný break-in); QSK? = můžete mě poslouchat mezi značkami? U transceiveru přepínač „QSK/full break-in“: přijímač se zapíná hned mezi tečkami a čárkami, takže protistanice může operátora kdykoli přerušit.',
    19: 'QRJ v radioamatérském významu = nemohu vás přijímat, vaše signály jsou velmi slabé (historický význam, viz poznámka u otázky). Dnes se místo toho spíše řekne „UR SIGS VY WEAK“ nebo „NO CPY“.',
    20: 'QRK? = jaká je čitelnost mých značek?; QRK 1–5 = čitelnost od nečitelné po dokonale čitelnou – odpovídá písmenu R v reportu RST. „QRK 5“ = čitelnost výborná.',
    21: 'QSZ = vysílejte každé slovo (skupinu) dvakrát – při velmi špatných podmínkách nebo silném rušení: „PSE QSZ“. Podobně se při obtížném spojení opakuje značka a report.',
}
