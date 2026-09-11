# Appendix C - Övningar

> **Så kontrollerar du ditt arbete.** Varje uttryck du tar fram med ett Karnaughdiagram kan du
> kontrollera på två sätt, och du ska göra minst ett av dem varje gång: sätt in varje rad i
> sanningstabellen i ditt uttryck och se att det ger rätt utgång, eller bygg nätet i
> [CircuitVerse](https://circuitverse.org/simulator) och gå igenom alla kombinationer av
> ingångarna. Ett uttryck som inte är kontrollerat är en gissning.
>
> Lösningsförslagen finns i [Appendix D](./d_solutions.md). Gör varje övning innan du läser
> lösningen. Där det finns ett vanligt felsvar visar lösningen det också, och varför det är fel.

Varje övning är märkt med sin sort. Kontrolluppgiften är övning 12.

---

## 1. Graykod och grannar
**Förståelse.**

**a)** Varför skrivs rubrikerna i ett Karnaughdiagram i ordningen `00, 01, 11, 10` och inte
`00, 01, 10, 11`? Svara med en mening om vad två grannrutor måste ha gemensamt.

**b)** I ett diagram med fyra ingångar, `ABCD`: vilka fyra rutor är grannar till ruta 5
(`ABCD = 0101`)? Ange dem som mintermnummer. Använd figuren med rutornas nummer i
[A.2](./a_karnaugh_maps.md#a2-diagrammet-och-graykoden) om du vill, men kontrollera svaret genom att
se att varje granne skiljer sig från 0101 i exakt en bit.

**c)** Samma fråga för ruta 0. Två av grannarna ligger på andra sidan en kant. Vilka?

**d)** Varför får en grupp inte bestå av tre rutor, ens när tre ettor ligger på rad?

---

## 2. Två ingångar
**Räkna för hand.**

| A | B | X |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**a)** Rita Karnaughdiagrammet och ringa in grupperna.

**b)** Läs av det minimerade uttrycket. Vad säger det om ingången `A`?

**c)** Läs av uttrycket direkt ur tabellen, på L02:s sätt, och förenkla det algebraiskt. Får du
samma svar?

---

## 3. Tre ingångar
**Räkna för hand.**

| ABC | X |
|-----|---|
| 000 | 1 |
| 001 | 1 |
| 010 | 0 |
| 011 | 0 |
| 100 | 1 |
| 101 | 1 |
| 110 | 0 |
| 111 | 0 |

**a)** Fyll i diagrammet. Två av raderna med ettor ligger inte bredvid varandra på papperet. Är de
grannar ändå?

**b)** Ringa in och läs av det minimerade uttrycket.

**c)** Hur många grindar behövs för det minimerade nätet, och hur många hade den direkta
avläsningen ur tabellen krävt?

---

## 4. Från mintermer
**Räkna för hand.**

`X` har tre ingångar `A`, `B`, `C` och är `1` för mintermerna 0, 2, 5 och 7.

**a)** Skriv sanningstabellen, och fyll i diagrammet.

**b)** Ringa in och läs av det minimerade uttrycket.

**c)** Uttrycket beror bara på två av ingångarna. Vilken grind från L02 beräknar det med en enda
grind?

---

## 5. Två utgångar
**Räkna för hand.**

En krets har fyra ingångar `ABCD` och två utgångar `X` och `Y`:

| ABCD | XY | ABCD | XY |
|------|----|------|----|
| 0000 | 01 | 1000 | 11 |
| 0001 | 00 | 1001 | 10 |
| 0010 | 00 | 1010 | 10 |
| 0011 | 01 | 1011 | 11 |
| 0100 | 11 | 1100 | 01 |
| 0101 | 10 | 1101 | 00 |
| 0110 | 10 | 1110 | 00 |
| 0111 | 11 | 1111 | 01 |

**a)** Rita ett diagram för `X` och ett för `Y`, och läs av båda uttrycken.

**b)** Två av ingångarna påverkar inte `X` alls, och två andra påverkar inte `Y`. Vilka? Hur syns
det i diagrammen?

**c)** Båda uttrycken kan skrivas med en enda grind var. Vilka grindar?

---

## 6. Hörnen
**Räkna för hand.**

`X` har fyra ingångar och är `1` för mintermerna 0, 2, 8, 10 och 15.

**a)** Fyll i diagrammet, ringa in och läs av.

**b)** Minterm 15 får ingen granne att gå ihop med. Är det ett fel i din gruppering? Motivera.

---

## 7. Segment e i en sifferdisplay
**Räkna för hand.**

En 7-segmentsdisplay visar en BCD-siffra 0-9 som kommer in på fyra ledningar `ABCD`
([L01 Appendix B](../../L01/appendix/b_binary_codes.md)). Segment **e**, det nedre vänstra, ska
lysa för siffrorna 0, 2, 6 och 8, och vara släckt för 1, 3, 4, 5, 7 och 9. Kombinationerna 10-15
förekommer aldrig.

**a)** Fyll i diagrammet med ettor, och med X för 10-15.

**b)** Ringa in och läs av ett minimerat uttryck för `e`. Använd X-rutorna där de gör grupperna
större.

**c)** Kontrollera ditt uttryck för alla tio siffrorna.

**d)** Vad visar segment e om kretsen ändå får `1010` på ingången? Är det ett problem?

---

## 8. Fläkten
**Konstruktion.**

En ventilationsfläkt `F` styrs av fyra signaler:
* `T`: temperaturen är hög;
* `W`: fönstret är öppet;
* `C`: koldioxidhalten är hög;
* `B`: brandlarmet har löst ut.

Fläkten ska gå om temperaturen är hög och fönstret är stängt, eller om koldioxidhalten är hög. Men
när brandlarmet har löst ut ska fläkten **aldrig** gå, eftersom den då skulle mata elden med luft.

**a)** Skriv sanningstabellen, med ingångarna i ordningen `T W C B`.

**b)** Fyll i Karnaughdiagrammet, med `TW` nedåt och `CB` åt sidan, och läs av ett minimerat
uttryck.

**c)** Rita grindnätet.

**d)** Gör en grindtilldelning ([B.7](./b_integrated_circuits.md#b7-att-planera-en-uppkoppling)):
vilka kretsar ur 74HC08, 74HC32 och 74HC04 behövs, och hur många av varje?

---

## 9. Enbart NAND
**Konstruktion.**

`X = AB' + C`.

**a)** Rita nätet med AND, OR och NOT.

**b)** Gör om det till enbart NAND-grindar, enligt
[A.9](./a_karnaugh_maps.md#a9-nand--och-nor-nät). Glöm inte inverteringen av `B`, och ingången `C`
som går direkt till OR-grinden.

**c)** Kontrollera med De Morgan att ditt NAND-uttryck är lika med `AB' + C`.

**d)** Hur många NAND-grindar behövs, och hur många 74HC00?

---

## 10. Enbart NOR
**Konstruktion.**

`X = (A + B)C`.

**a)** Vilken form är uttrycket på, SP eller PS?

**b)** Gör om det till enbart NOR-grindar. Rita nätet.

**c)** Kontrollera ditt nät för alla åtta kombinationerna av `A`, `B` och `C`.

---

## 11. Kretsar och ben
**Förståelse.**

Använd benplaceringarna i [B.2](./b_integrated_circuits.md#b2-kapsel-och-benplacering).

**a)** Vilka ben har grind 3 i en 74HC00: ingångarna och utgången? Samma fråga för en 74HC02.

**b)** Ett nät behöver sex AND-grindar och en inverterare. Hur många kretsar av vilka sorter?

**c)** En grön lysdiod har spänningsfallet 2,1 V och ska drivas med ungefär 5 mA från en utgång på
5 V. Räkna ut förkopplingsmotståndet och välj ett standardvärde ur E12-serien (…, 330, 390, 470,
560, 680, 820, 1000 Ω). Vilken ström blir det?

**d)** En labbkamrat har lämnat ingångarna på de oanvända grindarna okopplade, och säger att det
fungerar. Förklara varför det ändå är fel, och vad som kan hända.

---

## 12. Kontroll: minimerat och ominimerat nät
**Kontroll.** *Räkna för hand, bygg och jämför, förklara.*

`X` har fyra ingångar och är `1` för mintermerna 1, 3, 5, 7, 9 och 11.

**a) För hand.** Skriv den direkta avläsningen ur tabellen: sex AND-termer med fyra ingångar var.
Minimera sedan med ett Karnaughdiagram.

**b) Förutsäg.** Hur många grindar och hur många kretsar behövs för vart och ett av de två
uttrycken? Skriv ned siffrorna innan du bygger något.

**c) Bygg båda i CircuitVerse**, med samma fyra ingångar, och varsin utgång. Gå igenom alla sexton
kombinationerna och anteckna båda utgångarna.

**d) Jämför.** Utgångarna ska vara lika på varje rad. Om de skiljer sig på någon rad: vilken rad,
och vad säger det om vilket av uttrycken som är fel?

**e)** Det minimerade uttrycket kan skrivas `D(A' + B')`, och `A' + B'` är enligt De Morgan
`(AB)'`. Hur få grindar och kretsar klarar du dig med då? Jämför med ditt svar på b).

---

## 13. Multiplexern
**Konstruktion.** *(fördjupning)*

En **multiplexer** väljer vilken av två signaler som ska släppas fram. Den har två dataingångar `A`
och `B`, en väljare `S` och en utgång `X`: när `S = 0` ska `X = B`, och när `S = 1` ska `X = A`.

**a)** Skriv sanningstabellen med ingångarna i ordningen `S A B`.

**b)** Minimera med ett Karnaughdiagram, med `SA` nedåt och `B` åt sidan.

**c)** Rita nätet, och förklara med egna ord varför högst en av de två AND-termerna kan vara 1 åt
gången.

---
