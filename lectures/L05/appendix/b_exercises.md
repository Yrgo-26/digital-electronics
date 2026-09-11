# Appendix B - Övningar

> **Så kontrollerar du ditt arbete.** De flesta övningarna här är felsökningsfall: en beskrivning
> av ett nät, vad som mättes, och frågan var felet sitter. Svara alltid med **var du mäter härnäst
> och varför**, inte bara med en gissning om orsaken. En gissning som råkar vara rätt lär dig
> ingenting om nästa fel.
>
> Kontrolluppgiften, övning 10, görs på labbstationen, gärna under Labb 2-1.
>
> Lösningsförslagen finns i [Appendix C](./c_solutions.md).

Varje övning är märkt med sin sort.

---

## 1. Matningen först
**Förståelse.**

**a)** Mellan vilka ben mäter du matningen på en 74HC08, och vilket värde ska du se?

**b)** Varför ska du mäta på kretsens ben och inte på matningsskenorna?

**c)** En krets saknar matning helt, men nätet "fungerar nästan". Hur kan en krets utan matning
alls ge några utsignaler?

---

## 2. Vad betyder mätvärdet?
**Förståelse.**

Du mäter på ingångar och utgångar i ett nät med 74HC-kretsar på 5 V. Vilken logisk nivå motsvarar
varje mätvärde, och vilka av dem tyder på ett fel?

**a)** 4,7 V på en utgång.

**b)** 0,1 V på en utgång.

**c)** 2,3 V på en ingång.

**d)** 2,5 V på en utgång, som dessutom är ansluten till en annan grinds utgång.

---

## 3. En grind som ljuger
**Räkna för hand.**

På en krets som ska vara en 74HC08 mäter du på grind 1: ben 1 = 4,9 V, ben 2 = 0,1 V och ben 3 =
4,8 V.

**a)** Vad borde ben 3 ha visat?

**b)** Grinden beter sig som en annan grind. Vilken? Ge en trolig förklaring, och vad du
kontrollerar för att bekräfta den.

---

## 4. Den varma kretsen
**Förståelse.**

Direkt efter att du slagit på matningen känner du att en av kretsarna blir varm.

**a)** Vad gör du först?

**b)** Nämn två troliga orsaker.

**c)** Hur kontrollerar du, utan att slå på matningen igen, vilken av dem det är?

---

## 5. Läs felet ur tabellen
**Räkna för hand.**

Nätet `X = AB + C` ger den här tabellen:

| A | B | C | X, mätt |
|---|---|---|---------|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

**a)** Vilka rader är fel?

**b)** Vad har de gemensamt, och vilken del av nätet pekar det ut?

**c)** Var mäter du först?

---

## 6. Bromsassistenten som inte bromsar
**Räkna för hand.**

Ett par har byggt bromsassistenten i Labb 2-1 uppgift 3. Nätet stämmer på tolv av sexton rader.
De fyra felaktiga raderna är alla rader där `D = 1` och `F = 1`: där blir `B = 0`, men ska vara 1.
Beteckningarna är desamma som i
[L02 A.10](../../L02/appendix/a_logic_gates.md#a10-föreläsningens-krets-bromsassistenten).

**a)** Vilket krav i specifikationen bryter nätet mot, och varför är just det felet farligt?

**b)** Paret har kopplat förarens pedal på ett ställe i nätet där den inte hör hemma. Var sitter
den, och vilket uttryck har de byggt i stället för det rätta?

**c)** Var mäter du för att bekräfta det?

---

## 7. Halvering
**Förståelse.**

En signal går genom sexton grindar i rad, och den är fel vid utgången. Den är rätt vid ingången.

**a)** Var gör du den första mätningen, och varför just där?

**b)** Hur många mätningar behöver du högst för att hitta den grind där felet uppstår?

**c)** Hur många hade du behövt, i värsta fall, om du i stället börjat från ingången och mätt efter
varje grind?

---

## 8. Den flimrande lysdioden
**Förståelse.**

En lysdiod på utgången av ett nät tänds och släcks när du för handen nära kopplingsdäcket, fast du
inte rör strömbrytarna.

**a)** Vad är den troliga orsaken?

**b)** Hur hittar du exakt vilket ben det gäller?

**c)** Varför händer det här med HC-kretsar, men inte på samma sätt med de äldre LS-kretsarna?

---

## 9. Planera fläkten
**Konstruktion.**

Fläkten från [L04, övning 8](../../L04/appendix/c_exercises.md#8-fläkten) har uttrycket
`F = TW'B' + CB'`.

**a)** Gör en fullständig grindtilldelning med kretsbeteckningar och bennummer, med 74HC04, 74HC08
och 74HC32.

**b)** Skriv kopplingslistan, med matningen först och de oanvända ingångarna sist.

**c)** Nätet fungerar, utom att fläkten aldrig startar på hög temperatur. Vilka rader i tabellen
är fel, och vilken del av nätet mäter du först?

---

## 10. Kontroll: en utgång under last
**Kontroll.** *Förutsäg, mät på labbstationen, förklara skillnaden.*

En utgång på en 74HC08 driver en röd lysdiod genom ett förkopplingsmotstånd på 330 Ω till jord.

**a) Förutsäg.** Räkna ut strömmen genom lysdioden som i
[L04 B.5](../../L04/appendix/b_integrated_circuits.md#b5-utgångar-lysdiod-med-förkopplingsmotstånd),
med antagandet att utgången ger exakt 5 V och att lysdioden har 2 V över sig.

**b) Mät.** Med utgången hög: mät spänningen på utgången och spänningen över lysdioden. Med
utgången låg: mät spänningen på utgången.

**c) Räkna igen**, nu med de uppmätta spänningarna: spänningen över motståndet är utgångens spänning
minus lysdiodens. Vilken ström går det?

**d) Förklara skillnaden** mellan a) och c). Vilket av de två antagandena i a) var fel, och varför?
Stämmer den uppmätta höga och låga nivån med databladets V<sub>OH</sub> och V<sub>OL</sub>?

---

## 11. Fel krets i sockeln
**Förståelse.** *(fördjupning)*

Någon har satt en 74HC02 där det skulle sitta en 74HC00, och kopplat den enligt benplaceringen för
74HC00: strömbrytarna A och B till ben 1 och 2, och ben 3 till lysdioden.

**a)** Vad är ben 1 på en 74HC02?

**b)** Vad händer elektriskt när strömbrytaren på ben 1 står i läge 0 medan NOR-grinden försöker ge
en etta på samma ben? Varför kan kretsen bli varm?

**c)** Vad visar lysdioden på ben 3?

---
