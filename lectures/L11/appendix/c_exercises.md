# Appendix C - Övningar

> **Så kontrollerar du ditt arbete.** Övningarna märkta **Program** skrivs i Microchip Studio och
> testas först i simulatorn och sedan, om ni har kortet, på ett Arduino Uno. Övning 9, kontrollen,
> kräver kortet och en multimeter, och görs lämpligen på passet.
>
> Övningarna märkta **Räkna för hand**, **Förståelse** och **Konstruktion** görs på papper, utan
> miniräknare, och kontrolleras mot [Appendix D](./d_solutions.md). Gör varje övning innan du läser
> lösningen.

Varje övning är märkt med sin sort. Exakt en övning är en **Kontroll**, och i det här passet är det
övning 9.

---

## 1. Ingångar, beslut och utgångar
**Förståelse.**

Beskriv för vart och ett av styrsystemen nedan vilka **ingångar** det har, vilka **utgångar**, och
vilket **beslut** det fattar, som i [A.1](./a_control_objects.md#a1-vad-ett-styrobjekt-är).

**a)** En garageport med en knapp, en motor som kan köra upp och ned, och två gränslägesbrytare, en
som känner att porten är helt öppen och en att den är helt stängd.

**b)** En handtork som blåser när en IR-givare ser en hand, och slutar tio sekunder efter att handen
försvunnit.

**c)** Övergångsstället i [slutuppgiften](../../../labs/lab3/e_final_task.md).

---

## 2. Förkopplingsmotståndet
**Räkna för hand.**

Stiftet ger 5 V. Räkna med 2 V över en röd lysdiod och 3 V över en grön.

**a)** Hur stor blir strömmen genom en röd lysdiod med 220 Ω, 330 Ω och 1 kΩ?

**b)** Hur stor blir strömmen genom en grön lysdiod med 220 Ω? Varför lyser den kanske svagare än
den röda med samma motstånd?

**c)** Vilket motstånd behövs för 10 mA genom en röd lysdiod?

**d)** Någon tar ett motstånd på 47 Ω. Hur stor blir strömmen, och vad säger databladets gräns om
det?

---

## 3. Hela porten
**Räkna för hand.**

Sex röda lysdioder sitter på PB0-PB5, var och en med 220 Ω, och alla lyser samtidigt.

**a)** Hur stor är den sammanlagda strömmen ut ur porten?

**b)** Jämför med gränsen på ungefär 100 mA för en grupp av stift, från
[A.2](./a_control_objects.md#a2-lysdioden-och-förkopplingsmotståndet). Hur mycket marginal finns
det?

**c)** Varför är 330 Ω ett säkrare val än 220 Ω om många lysdioder kan lysa samtidigt?

---

## 4. Reläet
**Förståelse.**

Titta på kopplingen i [A.3](./a_control_objects.md#a3-större-laster-transistor-och-relä).

**a)** Varför kopplas reläspolen inte direkt till stiftet?

**b)** Vad gör dioden, och vad händer om den saknas?

**c)** Mikrodatorn och 24 V-kretsen har ingen gemensam ledning. Varför är det en fördel?

**d)** Någon kopplar lampan på 24 V direkt mellan stiftet och jord, utan relä. Vad händer, med
lampan och med kortet?

---

## 5. Knappar som studsar
**Förståelse.**

**a)** Förklara med egna ord varför programmet i
[A.4](./a_control_objects.md#a4-knappar-som-studsar) räknar 6 i stället för 2 när väntan tas bort.

**b)** Varför väntar programmet 20 ms, och inte 1 ms eller 500 ms? Vad går fel med var och en av de
två andra?

**c)** Lysdioden i [`led_follows_button.asm`](../../L10/examples/led_follows_button.asm) i L10 tänds
så länge knappen hålls ned, och har ingen avstudsning alls. Varför behövs den inte där?

---

## 6. Hur lång tid tar ett varv?
**Räkna för hand.**

Använd formeln för `delay_s` i [B.4](./b_traffic_light.md#b4-subrutinen-delay_s).

**a)** Hur många cykler tar ett anrop av `delay_s` med `r24` = 4?

**b)** Vägarbetsljusets loop har, utöver de två anropen, tre instruktioner per tillstånd (`ldi`,
`out`, `ldi`) och ett `rjmp`. Hur många cykler tar ett helt varv? Jämför med de 128 000 716 cykler
som kursens kontroll mätte.

**c)** Hur mycket för långt blir ett varv, i mikrosekunder? Hur mycket blir det på en timme?

**d)** Jämför med resonatorns noggrannhet i
[A.7](./a_control_objects.md#a7-hur-noggrann-är-klockan). Vilken av de två felkällorna är värd att
bry sig om?

---

## 7. Nattläge
**Konstruktion.**

På natten stängs trafikljus ofta av, och bara den gula lampan blinkar: en halv sekund tänd, en halv
sekund släckt.

**a)** Skriv tillståndstabellen, som i [B.2](./b_traffic_light.md#b2-tillstånden).

**b)** Rita flödesplanen.

**c)** Skriv programmet, med den gula lysdioden på PB1 och subrutinen `delay_ms`. Kan `r24` laddas
en enda gång, före loopen? Varför, eller varför inte?

**d)** Hur lång blir en hel blinkperiod, räknat i cykler?

---

## 8. En knapp som växlar
**Program.**

Skriv ett program där varje tryck på knappen på PD2 **växlar** lysdioden på PB5: ett tryck tänder,
nästa släcker, och så vidare. Använd avstudsning som i
[A.4](./a_control_objects.md#a4-knappar-som-studsar).

**a)** Rita flödesplanen.

**b)** Skriv programmet och testa det i simulatorn.

**c)** Vad händer på kortet om väntan efter trycket tas bort? Prova, om ni har kortet.

---

## 9. Kontroll: strömmen genom lysdioden
**Kontroll.** *Räkna för hand, mät på kortet, förklara skillnaden.*

En röd lysdiod med 220 Ω sitter på stift 8 (PB0), och ett program tänder den.

**a) För hand.** Räkna ut strömmen genom lysdioden, med 2 V över den.

**b) Mät spänningen över motståndet** med en multimeter, när lysdioden lyser. Räkna ut strömmen med
Ohms lag. Mät också spänningen mellan stiftet och jord.

**c) Jämför.** Stämmer strömmarna i a och b? Förklara skillnaden med det du mätte: är spänningen på
stiftet verkligen 5 V, och är spänningen över lysdioden verkligen 2 V?

**d)** Byt till en grön lysdiod och gör om b. Vad ändras, och varför?

---

## 10. Felsökning på kortet
**Förståelse.**

Programmet för trafikljuset fungerar i simulatorn. Förklara för vart och ett av symptomen nedan vad
det troligaste felet är, och hur du kontrollerar det.

**a)** Den gröna lampan lyser aldrig. De andra två fungerar.

**b)** Alla tre lamporna ser ut att lysa svagt, hela tiden.

**c)** Ingenting händer alls, och utskriften efter överföringen slutar med
`ser_open(): can't open device`.

**d)** Den röda och den gula lampan har bytt plats: gul lyser när röd ska lysa.

---

## 11. En dag på ett trafikljus
**Räkna för hand.** *(fördjupning)*

**a)** Kortets resonator går 0,5 % för fort. Hur mycket fel har en klocka byggd på programmets
fördröjningar efter ett dygn?

**b)** Hur många hela ljuscykler, om 8 s var, hinner trafikljuset i slutuppgiften med på ett dygn?
Räkna med exakt 8 s.

---
