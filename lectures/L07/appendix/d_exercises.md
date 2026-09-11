# Appendix D - Övningar

> **Så kontrollerar du ditt arbete.** Övningarna märkta **Program** och **Kontroll** görs i
> Microchip Studio: skapa ett projekt enligt
> [info/microchip_studio.md](../../../info/microchip_studio.md), skriv programmet, bygg med **F7**
> och stega med **F11**. Förutsäg alltid resultatet innan du stegar
> ([Appendix C.3](./c_microchip_studio_simulator.md#c3-förutsäg-före-varje-steg)).
>
> Övriga övningar görs med papper och penna. Lösningsförslag finns i
> [Appendix E](./e_solutions.md). Gör övningen innan du läser lösningen: det du nästan svarade
> lär dig mer än det rätta svaret gör.

Varje övning är märkt med sin sort. Det finns en **Kontroll** i det här passet, övning 7.

---

## 1. Arbetsbänken
**Förståelse.**

**a)** Hur många register har ATmega328P, och hur många bitar rymmer vart och ett?

**b)** Vilka register kan laddas med `ldi`?

**c)** Förklara, med hjälp av hur instruktionen `ldi` är kodad, varför de övriga registren inte kan
laddas med `ldi`. Svaret ska innehålla ett antal bitar.

**d)** Du vill ha talet 7 i `r5`. Skriv två instruktioner som gör det.

---

## 2. Tre minnen
**Förståelse.**

**a)** I vilket minne ligger programmet?

**b)** I vilket minne ligger värden som ändras medan programmet kör?

**c)** Vilket av de två minnena behåller sitt innehåll när strömmen bryts? Varför är det viktigt för
ett Arduino-kort?

**d)** Vad heter adressen `0x08FF` i programmen, och vad ligger där?

---

## 3. Samma tal, olika skrivsätt
**Räkna för hand.**

**a)** Skriv tre `ldi`-instruktioner som var och en laddar talet 45 i `r16`: decimalt, binärt och
hexadecimalt.

**b)** Gör samma sak för talen 255, 16 och 100.

**c)** Vilket decimalt värde laddas av `ldi r16, 0b01010101`, `ldi r17, 0x3F`, `ldi r18, $80` och
`ldi r19, 'a'`? Tecknet `a` har ASCII-koden `0x61`.

**d)** En lysdiod ska lysa för varje etta i ett register. Vilket skrivsätt väljer du när du
laddar mönstret, och varför?

---

## 4. Förutsäg registren
**Räkna för hand.**

Fyll i tabellen med värdet i varje register **efter** varje instruktion, hexadecimalt. Alla
register är 0 när programmet startar.

```asm
main:
    ldi r16, 0x10
    ldi r17, 7
    mov r18, r17
    inc r18
    inc r18
    dec r16
    mov r19, r16
    clr r17
    ser r20
    dec r20
end:
    rjmp end
```

| Efter | `r16` | `r17` | `r18` | `r19` | `r20` |
|-------|-------|-------|-------|-------|-------|
| `ldi r16, 0x10` | | | | | |
| `ldi r17, 7` | | | | | |
| `mov r18, r17` | | | | | |
| `inc r18` | | | | | |
| `inc r18` | | | | | |
| `dec r16` | | | | | |
| `mov r19, r16` | | | | | |
| `clr r17` | | | | | |
| `ser r20` | | | | | |
| `dec r20` | | | | | |

Kontrollera sedan ditt svar genom att stega programmet i simulatorn.

---

## 5. Hitta felen
**Förståelse.**

Programmet nedan går inte att assemblera. Hitta alla fel, förklara vart och ett, och skriv det
rättade programmet.

```asm
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main
    ldi r16 5
    ldi r10, 3
    mov r17 r16
    inc r20, 1
    rjmp mian
```

---

## 6. Ditt första egna program
**Program.**

Skriv ett program, utifrån [mallen](../../../labs/lab3/code/template.asm), som:
1. laddar talet 12 i `r16`;
2. kopierar `r16` till `r17`;
3. ökar `r17` med 3, med `inc`;
4. laddar bitmönstret `1010 1010` i `r18`, skrivet binärt;
5. kopierar `r18` till `r19`;
6. nollställer `r18`.

**a)** Skriv ned vilka värden `r16`-`r19` ska ha när programmet når `end`, både decimalt och
hexadecimalt.

**b)** Bygg och stega programmet. Stämmer värdena?

**c)** Hur många klockcykler har programmet kört när det når `end`? Räkna först, kontrollera sedan
med Cycle Counter.

---

## 7. Maskinkod för hand
**Kontroll.** *Räkna ut för hand, kontrollera i listfilen, förklara.*

Använd kodningen av `ldi` i [Appendix A.6](./a_avr_core.md#a6-vad-en-instruktion-är): `1110 KKKK
dddd KKKK`, där `dddd` är registrets nummer minus 16.

**a)** Räkna ut maskinkoden, hexadecimalt, för:
* `ldi r16, 0x2A`
* `ldi r24, 0x2A`
* `ldi r31, 0xFF`
* `ldi r20, 0x03`

Visa de fyra fälten för åtminstone den första.

**b)** Skriv de fyra instruktionerna i ett program, bygg det, och öppna listfilen (`.lss`) i
projektets katalog `Debug`. Jämför maskinkoden där med dina svar.

**c)** Stämde alla fyra? Om inte: vilket fält hade du fel på? Det vanligaste felet är att skriva
konstanten i ett stycke i stället för att dela den i två halvor.

**d)** Varför finns det ingen maskinkod för `ldi r15, 0x2A`?

---

## 8. Programmet som inte tog slut
**Förståelse.**

**a)** Varför slutar varje program i kursen med raderna `end:` och `rjmp end`?

**b)** Ta bort de två raderna ur programmet i övning 4. Programmet går fortfarande att assemblera.
Vad händer när processorn har kört den sista instruktionen?

**c)** Varför börjar varje program med `rjmp main`, trots att `main` kommer direkt efter?

---

## 9. Tillåtet eller inte?
**Förståelse.**

Vilka av raderna är tillåtna? Förklara varför de otillåtna inte är det, och skriv en rad som gör
det som troligen var meningen.

**a)** `mov r5, r16`

**b)** `ldi r5, 16`

**c)** `mov r16, 5`

**d)** `ldi r16, r5`

**e)** `inc r3`

---

## 10. Hur lång tid tar programmet?
**Räkna för hand.**

**a)** Hur många klockcykler tar programmet i övning 4, från start tills det når `end`? Programmet
står i mallen, så det börjar med `rjmp main` på adress 0.

**b)** Hur lång tid är det vid 16 MHz?

**c)** Ungefär hur många gånger per sekund skulle processorn hinna köra programmet, om det startade
om efter varje varv?

---

## 11. Maskinkod baklänges
**Räkna för hand.** *(fördjupning)*

Tre instruktioner i en listfil har maskinkoden nedan. Alla tre är `ldi`-instruktioner. Vilka?

**a)** `0xE3F5`

**b)** `0xE0A0`

**c)** `0xEF0F`. Vilken annan instruktion ur [Appendix
B.5](./b_assembly_language.md#b5-de-första-instruktionerna) gör exakt samma sak?

---
