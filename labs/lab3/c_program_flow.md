# Labb 3 - Del 11, 12 och 14-17: Programflöde, loopar och tidsfördröjningar

Delarna hör till [L09](../../lectures/L09/README.md). Varje del är ett eget projekt som utgår från
[mallen](./code/template.asm).

Från och med nu gäller två vanor till:
* **Rita flödesplanen först**, på papper, innan ni skriver en enda instruktion
  ([L09 Appendix A.1](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a1-flödesplaner)).
* **Mät tider med stoppuret**, med Frequency inställd på 16 MHz
  ([L09 Appendix B.6](../../lectures/L09/appendix/b_loops_and_delays.md#b6-mät-med-stoppuret)).

Del 13 ingår inte i laborationen; numreringen hoppar från 12 till 14.

---

## Del 11 - Vitsen med flaggor: jämförelse med cp

### Mål
Se vad `cp` och `cpi` gör med flaggorna, och hur flaggorna säger om två tal är lika, större eller
mindre.

### Bakgrund
[L09 Appendix
A.3](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a3-jämförelse-cp-cpi-och-tst) och
[A.6](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a6-utan-tecken-eller-med-tecken).

### Uppgifter
Skriv ett program med de fem jämförelserna nedan, med en etikett efter var och en. **Förutsäg** `Z`,
`C` och `S` för varje jämförelse i en tabell innan ni kör fram till etiketterna.

| Jämförelse | `r16` | `r17` | Z | C | S | `r16` är ... `r17` |
|------------|-------|-------|---|---|---|--------------------|
| 1. `cp r16, r17` | 50 | 30 | | | | |
| 2. `cp r16, r17` | 50 | 50 | | | | |
| 3. `cp r16, r17` | 50 | 70 | | | | |
| 4. `cpi r16, 50` | 50 | - | | | | |
| 5. `cp r16, r17` | -5 | 3 | | | | |

1. Fyll i tabellen, och fyll i sista kolumnen med *större än*, *lika med* eller *mindre än*.
2. Kör fram till varje etikett och kontrollera flaggorna.
3. Kontrollera efter jämförelse 1-3 att `r16` fortfarande är 50. Varför ändras det inte, fast `cp`
   räknar ut en subtraktion?
4. Titta särskilt på jämförelse 5. Är -5 mindre eller större än 3? Svara både **utan** tecken, när
   `r16` läses som 251, och **med** tecken. Vilken flagga svarar på vilken fråga?

### Frågor
* Vilka två flaggor räcker för att avgöra om två tal utan tecken är lika, om det första är större,
  eller om det är mindre?
* Varför behövs både `brlo` och `brlt`?

*Redovisa* tabellen.

---

## Del 12 - Flödesplan och villkorliga hopp

### Mål
Rita en flödesplan med beslut, och skriva det som ett program med jämförelser och villkorliga hopp.

### Bakgrund
[L09 Appendix A.4 och A.5](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a5-om-annars).

### Specifikation
En termostat styr ett rum. Temperaturen i grader finns i `r16`. Port B styr två saker:
* **PB0**, en värmare, ska vara på när temperaturen är **under 20** grader;
* **PB1**, en fläkt, ska vara på när temperaturen är **25 grader eller mer**;
* mellan 20 och 24 grader ska båda vara av.

Programmet ska gå i en loop: det läser `r16`, sätter utgångarna, och börjar om. Då kan ni stoppa
simuleringen, ändra värdet i `r16` i Processor Status, och köra vidare för att se utgångarna ändras.

### Uppgifter
1. Rita flödesplanen. Den har två beslut. Märk varje beslut med Ja och Nej.
2. Skriv programmet. Ladda startvärdet 18 i `r16` **före** loopen, så att ett värde ni skriver in i
   Processor Status inte skrivs över.
3. **Förutsäg** `PORTB` för temperaturerna 18, 20, 24, 25 och 30. Testa alla fem i simulatorn.
4. Vilka av värdena är **gränsfall**, och varför är det de som är viktigast att testa?

### Frågor
* Villkoret "25 grader eller mer" används för fläkten. Hur skriver man "mer än 24" med de hopp som
  finns?
* Vad händer med termostaten vid -5 grader? Se [L09 Appendix
  A.6](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a6-utan-tecken-eller-med-tecken).

*Redovisa* flödesplanen och programmet, och visa minst tre temperaturer i simulatorn.

---

## Del 14 - Loop med visst antal varv

### Mål
Skriva en loop som går ett bestämt antal varv med en räknare, och veta exakt hur många gånger varje
instruktion i den körs.

### Bakgrund
[L09 Appendix
B.1](../../lectures/L09/appendix/b_loops_and_delays.md#b1-en-loop-med-ett-bestämt-antal-varv).

### Specifikation
Processorn har ingen multiplikation i den här laborationen. Räkna ut 7 · 3 genom att addera 3 sju
gånger, med en loop. Visa antalet varv som hittills gått på port B, så att det syns i I/O-fönstret.

### Uppgifter
1. Rita flödesplanen. Använd ett register för resultatet, ett för talet som adderas, ett för varven
   som är kvar och ett för varven som har gått.
2. Skriv programmet med `.equ` för konstanterna, till exempel `.equ LAPS = 7` och `.equ TERM = 3`.
3. **Förutsäg** resultatet och `PORTB` när programmet är klart. Stega igenom minst två varv och se
   `PORTB` räkna, kör sedan till slutet med **Run To Cursor**.
4. Hur många gånger körs `brne`, och hur många av dem hoppar den?
5. Ändra `LAPS` till 0. **Förutsäg** resultatet innan ni kör. Förklara det ni ser.
6. Räkna ut 12 · 25 med samma program. Stämmer resultatet? Varför, eller varför inte?

### Frågor
* Varför behövs ingen `cpi` före `brne`?

*Redovisa* programmet och svaren på uppgift 4-6.

---

## Del 15 - Kort tidsfördröjning

### Mål
Göra en tidsfördröjning med en loop, räkna ut dess längd i klockcykler, och kontrollera den med
stoppuret.

### Bakgrund
[L09 Appendix B.3 och
B.4](../../lectures/L09/appendix/b_loops_and_delays.md#b4-en-kort-tidsfördröjning).

### Programmet

```asm
main:
    sbi DDRB, 0                     ; PB0 is an output.
    sbi PORTB, 0                    ; The pulse starts.

delay_start:
    ldi r18, 200
delay_loop:
    dec r18
    brne delay_loop
delay_end:
    cbi PORTB, 0                    ; The pulse ends.

end:
    rjmp end
```

Programmet ger en puls på PB0: stiftet går högt, fördröjningen körs, och stiftet går lågt.

### Uppgifter
1. Räkna ut fördröjningens längd, från `delay_start` till `delay_end`, i klockcykler och i
   mikrosekunder. Använd en tabell med en rad per instruktion, som i L09 Appendix B.4.
2. Mät samma sak i simulatorn: brytpunkt på `delay_start` och `delay_end`, Frequency på 16 MHz, och
   stoppuret nollställt vid den första brytpunkten. Stämmer det?
3. Pulsen ska vara **30 µs**. Räkna ut hur många varv loopen ska gå, ändra programmet, och mät.
4. Vilken är den längsta fördröjning loopen kan ge? Räkna först, mät sedan.
5. Flytta den första brytpunkten till `sbi PORTB, 0`. **Förutsäg** hur mycket mätningen ändras.

### Frågor
* Varför blir det exakt 3 · n cykler och inte 3 · n + 1?

*Redovisa* uträkningen och mätningen för 30 µs.

---

## Del 16 - Längre tidsfördröjning

### Mål
Göra en längre fördröjning med två loopar i varandra, och träffa en önskad tid exakt.

### Bakgrund
[L09 Appendix B.5](../../lectures/L09/appendix/b_loops_and_delays.md#b5-en-längre-tidsfördröjning).

### Specifikation
PB0 ska byta läge var **10:e millisekund**: hög i 10 ms, låg i 10 ms, och så vidare, för alltid.
Byt läge genom att läsa `PORTB`, invertera bit 0 med `eor` och en mask, och skriva tillbaka.
Fördröjningen mellan bytena görs med två loopar i varandra.

### Uppgifter
1. Rita flödesplanen: en loop som byter läge på PB0 och sedan väntar, med fördröjningen som två
   loopar i varandra.
2. Välj OUTER och INNER med formeln OUTER · (3 · INNER + 3) så att fördröjningen blir så nära 10 ms
   som möjligt. Skriv programmet och mät fördröjningen.
3. Lägg till en `nop` i den yttre loopen. Hur ändras formeln? Välj nya konstanter så att
   fördröjningen blir **exakt** 10 ms, 160 000 cykler. Mät.
4. Mät nu en hel halvperiod: från ett byte av PB0 till nästa. Den blir några cykler längre än
   fördröjningen. Hur många, och vilka instruktioner är det?
5. Kör programmet fritt med **F5** i några sekunder och stoppa. Hur lång tid har gått enligt
   stoppuret? Ungefär hur många gånger har PB0 bytt läge?

### Frågor
* Skulle en lysdiod på PB0 synas blinka med den här fördröjningen på ett riktigt kort? Varför inte?

*Redovisa* konstanterna för exakt 10 ms och mätningarna.

---

## Del 17 - Flervalssituationer och omarbetning av flödesplaner

### Mål
Skriva ett program som väljer mellan flera alternativ, och arbeta om en flödesplan så att programmet
får en väg in och en väg ut.

### Bakgrund
[L09 Appendix A.7 och A.8](../../lectures/L09/appendix/a_flowcharts_and_branches.md#a7-flerval).

### Specifikation
Ett läge i `r16` väljer ett mönster på port B:

| Läge | Mönster på port B |
|------|-------------------|
| 0 | alla släckta |
| 1 | alla tända |
| 2 | de fyra nedre, PB0-PB3 |
| 3 | de fyra övre, PB4-PB7 |
| annat | varannan, `0101 0101`, som felindikering |

Programmet går i en loop, så att läget kan ändras i Processor Status medan programmet står stilla.

### Uppgifter
1. Rita en **första** flödesplan, hur ni vill. Skriv programmet efter den, och testa alla lägen,
   inklusive ett felläge.
2. Räkna i er flödesplan och i programmet: hur många rutor eller instruktioner skriver till port B?
   Hur många ställen går programmet tillbaka till loopens början från?
3. **Arbeta om** flödesplanen enligt L09 Appendix A.8: låt varje alternativ bara välja mönster, och
   låt alla alternativ mötas i **en** ruta som skriver till port B.
4. Skriv om programmet efter den nya flödesplanen. Testa alla lägen igen. Programmet ska göra exakt
   samma sak som förut.
5. Lägg till läge 4, PB0 och PB7 tända. Hur många ställen i programmet behövde ändras, i den första
   versionen och i den omarbetade?

### Frågor
* Varför är det viktigt att ha med alternativet "annat" i flödesplanen?

*Redovisa* båda flödesplanerna och det omarbetade programmet.

---
