# Appendix C - Övningar

> **Så kontrollerar du ditt arbete.** Rita flödesplanen innan du skriver programmet, och förutsäg
> resultatet innan du simulerar. Övningarna märkta **Program** och **Kontroll** görs i Microchip
> Studio; tidsfördröjningar mäts med stoppuret enligt
> [Appendix B.6](./b_loops_and_delays.md#b6-mät-med-stoppuret).
>
> Övriga övningar görs med papper och penna. Lösningsförslag finns i [Appendix D](./d_solutions.md).

Varje övning är märkt med sin sort. Det finns en **Kontroll** i det här passet, övning 9.

---

## 1. Rita en flödesplan
**Konstruktion.**

Ett program ska läsa ett tal i `r16` och tända PB0 om talet är jämnt, annars PB1. Ett tal är jämnt
om bit 0 är 0.

**a)** Rita flödesplanen.

**b)** Vilken instruktion och mask använder du för att ta reda på bit 0? Tips:
[L08 Appendix B.2](../../L08/appendix/b_logic_and_shifts.md#b2-masker).

**c)** Vilket villkorligt hopp passar efter den instruktionen?

---

## 2. Vilket hopp?
**Förståelse.**

Skriv en jämförelse och ett villkorligt hopp till etiketten `yes` för varje villkor. Talen är utan
tecken om inget annat sägs.

**a)** `r16` är lika med `r17`.

**b)** `r16` är inte noll.

**c)** `r16` är mindre än 100.

**d)** `r16` är 100 eller större.

**e)** `r16` är större än 100.

**f)** `r16` är negativt, när det läses med tecken.

**g)** `r16` är mindre än `r17`, när båda läses med tecken.

---

## 3. Följ programmet
**Räkna för hand.**

Vilket värde får `PORTB` när `r16` börjar med 5, 10, 99, 100 respektive 200?

```asm
    ldi r17, 0
    cpi r16, 10
    brlo small
    cpi r16, 100
    brsh big
    ldi r17, 2
    rjmp done
small:
    ldi r17, 1
    rjmp done
big:
    ldi r17, 3
done:
    out PORTB, r17
```

Rita också programmets flödesplan. Vad är programmets uppgift, med en mening?

---

## 4. Om, annars
**Program.**

**a)** Skriv ett program som tänder alla lysdioder på port B om `r16` är 42, och släcker alla
annars.

**b)** Testa programmet med `r16` = 42 och med `r16` = 41. Byt värde antingen i `ldi`-raden eller i
Processor Status.

**c)** Ta bort `rjmp`-instruktionen efter den första grenen. Vad händer nu för `r16` = 41, och för
`r16` = 42? Förklara.

---

## 5. Hur många varv?
**Räkna för hand.**

```asm
    ldi r16, N
loop:
    inc r17
    dec r16
    brne loop
```

`r17` är 0 från början. Vad är `r17` efter loopen när

**a)** N = 5?

**b)** N = 1?

**c)** N = 0? Förklara svaret.

**d)** Hur många gånger körs `brne` när N = 5, och hur många av dem hoppar den?

---

## 6. Summera
**Program.**

**a)** Skriv ett program som räknar ut 1 + 2 + ... + n, med n i `r16` och summan i `r17`.

**b)** Prova med n = 15. Vilket svar ska du få?

**c)** Vilket är det största n som ger rätt svar i en byte? Vad får du för n = 23, och varför?

---

## 7. Räkna cykler
**Räkna för hand.**

**a)** Hur många klockcykler tar fördröjningen i [Appendix
B.4](./b_loops_and_delays.md#b4-en-kort-tidsfördröjning) om startvärdet är 100 i stället för 200?
Hur lång tid är det vid 16 MHz?

**b)** Samma fråga för startvärdet 1.

**c)** Samma fråga för startvärdet 0.

---

## 8. Välj konstanter
**Konstruktion.**

**a)** En fördröjning ska vara 40 µs. Hur många varv ska loopen i B.4 gå? Hur nära 40 µs kommer du,
och hur kan du komma exakt?

**b)** En fördröjning ska vara 5 ms. Välj OUTER och INNER för loopen i B.5, först utan och sedan med
en `nop` i den yttre loopen. Hur nära 5 ms kommer du i de två fallen?

**c)** Varför går det inte att göra en fördröjning på en sekund med två loopar?

---

## 9. Räkna, mät och förklara
**Kontroll.** *Räkna ut för hand, mät med stoppuret, förklara skillnaden.*

Använd [`long_delay.asm`](../examples/long_delay.asm), med OUTER = 208 och INNER = 255.

**a)** Räkna ut antalet klockcykler från raden `delay_start` till raden `delay_end`, med en tabell
som den i [Appendix B.4](./b_loops_and_delays.md#b4-en-kort-tidsfördröjning): en rad per
instruktion, cykler, antal gånger och summa. Räkna om till millisekunder.

**b)** Mät samma sak i simulatorn med brytpunkter och stoppuret. Stämmer det?

**c)** Flytta den första brytpunkten till raden `sbi PORTB, 0` och den andra till raden
`cbi PORTB, 0`. Förutsäg först hur mycket mätningen ändras, mät sedan. Förklara skillnaden.

**d)** Ändra OUTER till 100 och förutsäg den nya tiden med formeln. Mät och jämför.

**e)** En kamrat har räknat ut att fördröjningen tar OUTER · INNER · 3 = 159 120 cykler. Vad har
kamraten glömt, och hur stort blir felet i procent?

---

## 10. Flerval
**Program.**

Ett program ska visa ett mönster på port B beroende på läget i `r16`:
* läge 0: alla släckta;
* läge 1: bara PB0;
* läge 2: PB0 och PB1;
* alla andra lägen: alla tända, som en felindikering.

**a)** Rita flödesplanen, med en gemensam ruta för `PORTB = mönster`.

**b)** Skriv programmet och testa alla fyra fallen.

---

## 11. Arbeta om
**Konstruktion.**

Programmet nedan fungerar, men det har tre slut och tre kopior av `out`. Rita dess flödesplan,
arbeta om den enligt [Appendix A.8](./a_flowcharts_and_branches.md#a8-att-arbeta-om-en-flödesplan),
och skriv det omarbetade programmet.

```asm
    cpi r16, 1
    breq one
    cpi r16, 2
    breq two
    ldi r17, 0
    out PORTB, r17
end_1:
    rjmp end_1
one:
    ldi r17, 1
    out PORTB, r17
end_2:
    rjmp end_2
two:
    ldi r17, 3
    out PORTB, r17
end_3:
    rjmp end_3
```

---

## 12. Minusgrader
**Förståelse.** *(fördjupning)*

Värmaren i [Appendix A.5](./a_flowcharts_and_branches.md#a5-om-annars) ska användas utomhus, där
temperaturen kan bli negativ. Den lagras som ett tal med tecken.

**a)** Vad gör programmet när temperaturen är -5 grader? Följ `cpi` och `brlo` steg för steg.

**b)** Vilket hopp ska användas i stället, och vilken flagga läser det?

**c)** Fungerar det rättade programmet även för temperaturen 25 grader? För 100 grader?

---
