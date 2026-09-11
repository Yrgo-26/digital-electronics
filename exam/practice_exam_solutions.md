# Övningsprov - lösningsförslag

Lösningarna följer [övningsprovet](./practice_exam.md). Vid varje deluppgift står poängen och vad
som ger delpoäng. Bedömningsprinciperna, med metod och följdfel, står i [README.md](./README.md).
Programmen i fråga 6 har körts i simulatorn.

---

## Fråga 1 - Talsystem och koder (8 p)

**a) (2 p)** Ettorna har vikterna 128, 64, 16, 4 och 2: `128 + 64 + 16 + 4 + 2 = 214`. Grupperna
`1101` och `0110` är `D` och `6`: **214** och **`0xD6`**.

*1 p per rätt omvandling med uträkning.*

**b) (2 p)** 173: 128 ryms, 45 kvar; 32 ryms, 13 kvar; 8 ryms, 5 kvar; 4 ryms, 1 kvar; 1 ryms. Ettor
på vikterna 128, 32, 8, 4 och 1: **`1010 1101`**. Grupperna `1010` och `1101` är `A` och `D`:
**`0xAD`**.

*1 p per rätt omvandling. Division med 2 och avläsning av resterna är lika bra.*

**c) (2 p)**

```text
  minnessiffror: 1 11
                   1011 0100      0xB4 = 180
                 + 0110 1010    + 0x6A = 106
                 -----------
                 1 0001 1110      286
```

Bit 5 ger en minnessiffra in i bit 6, bit 6 en in i bit 7, och bit 7 en som går ut ur registret.

Registret får de åtta låga bitarna, **`0x1E`**, och **en minnessiffra går ut** ur registret,
eftersom `180 + 106 = 286` inte ryms i åtta bitar: `286 - 256 = 30 = 0x1E`.

*1 p för en korrekt uppställd addition, 1 p för `0x1E` och minnessiffran.*

**d) (2 p)** BCD skriver varje siffra för sig med fyra bitar: **`0101 1001`**. ASCII-koderna för
tecknen `'5'` och `'9'` är **`0x35`** och **`0x39`**.

*1 p för BCD, 1 p för ASCII-koderna.* **Fälla:** 59 binärt, `0011 1011`, är inte BCD och ger 0 p på
BCD-delen.

---

## Fråga 2 - Grindar och boolesk algebra (8 p)

**a) (2 p)**

| A | B | C | `A'B` | `BC'` | X |
|---|---|---|-------|-------|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 0 |

*2 p för en helt rätt tabell, 1 p för högst ett fel.*

**b) (3 p)**

```text
X = AB + AB' + A'B
  = A(B + B') + A'B        bryt ut A
  = A · 1 + A'B            komplement: B + B' = 1
  = A + A'B                identitet
  = A + B                  förenklingslagen: A + A'B = A + B
```

Det förenklade uttrycket är en **OR-grind**.

*1 p för att slå ihop de två första termerna till A, 1 p för förenklingslagen, 1 p för OR.* Ett svar
som stannar vid `A + A'B` får 1 p: det saknar förenklingslagen, och pekar inte ut någon enda grind.

**c) (3 p)**
1. **`A'B'`**, med De Morgan. *(1 p)*
2. Med De Morgan är `A + B = (A'B')'`. Inversen av en variabel är en NAND-grind med båda ingångarna
   kopplade till variabeln: `(AA)' = A'`. Nätet blir tre NAND-grindar: en som bildar `A'`, en som
   bildar `B'`, och en tredje med `A'` och `B'` in, som bildar `(A'B')' = A + B`. *(2 p)*

*1 p för ett korrekt nät, 1 p för att visa varför det stämmer.*

---

## Fråga 3 - Karnaughdiagram (6 p)

**a) (2 p)**

| AB \ CD | 00 | 01 | 11 | 10 |
|---------|----|----|----|----|
| **00** | 1 | | | 1 |
| **01** | | 1 | 1 | |
| **11** | | 1 | 1 | |
| **10** | 1 | | | 1 |

*1 p för rätt Graykod på båda axlarna, 1 p för rätt placerade ettor.* **Fälla:** axlarna i binär
ordning, `00, 01, 10, 11`, ger 0 p på axlarna, men följdfelet bedöms i b).

**b) (3 p)** Två grupper om fyra:
* **De fyra hörnen**, mintermerna 0, 2, 8 och 10. Hörnen är grannar eftersom diagrammet går runt
  både uppifrån och ned och från vänster till höger. Där är `B` = 0 och `D` = 0: termen **`B'D'`**.
* **De fyra mittrutorna**, mintermerna 5, 7, 13 och 15. Där är `B` = 1 och `D` = 1: termen **`BD`**.

```text
X = B'D' + BD
```

*1 p för varje rätt grupp med rätt term, 1 p för det samlade uttrycket.* Den som missar att hörnen
är en grupp och skriver hörnen som två par, `A'B'D' + AB'D' + BD`, får 1 p.

**c) (1 p)** `X` beror bara på **B och D**, och är 1 när de är lika: en **XNOR**-grind. A och C
påverkar inte `X` alls.

---

## Fråga 4 - Analys av ett kontaktnät (6 p)

**a) (2 p)** Två parallellkopplingar i serie. Den första är `S1 + S2`, den andra `S1 + S3'`,
eftersom S3 är brytande:

```text
H1 = (S1 + S2)(S1 + S3')
```

*1 p per rätt parallellkoppling, inklusive `S3'`.*

**b) (2 p)**

| S1 | S2 | S3 | `S1 + S2` | `S1 + S3'` | H1 |
|----|----|----|-----------|------------|----|
| 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 |

*2 p för en helt rätt tabell, 1 p för högst ett fel. Följdfel från a) bedöms här.*

**c) (2 p)** Med den distributiva lagen `A + BC = (A + B)(A + C)`, läst baklänges:

```text
H1 = (S1 + S2)(S1 + S3') = S1 + S2S3'
```

Nätet: den slutande kontakten S1 **parallellt med** en seriekoppling av den slutande kontakten S2
och den brytande kontakten S3, och sedan lampan. Tre kontakter i stället för fyra, och bara ett
kontaktblock på S1.

*1 p för det förenklade uttrycket, 1 p för ett rätt ritat nät.* Kontrollera med tabellen:
`S1 + S2S3'` är 1 på raderna 010, 100, 101, 110 och 111, samma som i b).

---

## Fråga 5 - Mikrodatorns uppbyggnad (4 p)

**a) (2 p)** CPU:n med ALU (räknar och jämför), register (håller värdena som räknas med), styrenhet
(avkodar instruktionerna och styr resten) och programräknare (pekar på nästa instruktion).
Programminnet håller programmet, dataminnet variablerna och stacken, och in- och utportarna
förbinder mikrodatorn med omvärlden. Bussarna, adressbussen och databussen, förbinder CPU:n med
minnena och portarna.

*1 p för ett blockschema med alla delar på plats, 1 p för att beskriva vad de gör.*

**b) (1 p)** Programräknaren innehåller **adressen till nästa instruktion** som ska hämtas. Vid
`rcall` sparas adressen till instruktionen efter `rcall` på stacken, och programräknaren får
subrutinens adress, så att nästa instruktion hämtas därifrån.

**c) (1 p)** Programmet ligger i **flashminnet**, som behåller sitt innehåll utan ström. Stacken
ligger i **SRAM**, som töms när strömmen bryts.

---

## Fråga 6 - Assemblerprogrammering (8 p)

**a) (3 p)** Uppmätt i simulatorn: **`r16` = `0x68`**, **`r17` = `0x04`**, **`r18` = `0x2C`**, och
**`C` = 1** efter `add`.
* `and r17, r16`: `0000 1111 AND 1011 0100 = 0000 0100` = `0x04`.
* `lsl r16`: `1011 0100` skiftas ett steg åt vänster och blir `0110 1000` = `0x68`. Bit 7 hamnar i
  `C`, men `C` skrivs över senare av `add`.
* `add r18, r19`: `200 + 100 = 300`, som inte ryms i åtta bitar. Registret får `300 - 256 = 44` =
  `0x2C`, och minnessiffran hamnar i `C`.

*1 p för `r16` och `r17`, 1 p för `r18`, 1 p för `C` och förklaringen: åtta bitar räcker till 255.*

**b) (2 p)**
1. Loopen körs **4 gånger**, en gång för varje värde på `r17`: 4, 3, 2 och 1. `PORTB` får värdena 1,
   2, 4 och 8, och är **`0x08`** när loopen är klar. `r16` är då `0x10`, men det skrivs aldrig till
   porten.
2. Ett varv är `out` 1, `lsl` 1, `dec` 1 och `brne` 2 cykler, alltså 5; det sista varvet 4. Loopen
   tar `4 · 5 - 1 = 19` cykler, och `19 · 62,5 ns ≈ 1,19 µs`. Simulatorn mäter 19 cykler.

*1 p per deluppgift.* **Fälla:** `PORTB` = `0x10`, genom att räkna med `lsl` efter den sista `out`,
ger 0 p på den delen.

**c) (3 p)** Till exempel:

```asm
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    sbi DDRB, 0                     ; PB0, the LED, is an output.
    cbi DDRD, 3                     ; PD3, the button, is an input ...
    sbi PORTD, 3                    ; ... with its pull-up switched on.

loop:
    sbic PIND, 3                    ; Skip the next instruction if PD3 is 0 (pressed).
    rjmp off                        ; PD3 is 1: released.
    sbi PORTB, 0                    ; Pressed: LED on.
    rjmp loop
off:
    cbi PORTB, 0                    ; Released: LED off.
    rjmp loop
```

Programmet har körts i simulatorn med knappen släppt och nedtryckt.

*1 p för initieringen (utgång, ingång och pull-up), 1 p för att läsa rätt bit och ta hänsyn till att
knappen är aktivt låg, 1 p för en loop som tänder och släcker rätt.* Ett program som läser hela
porten med `in`, inverterar med `com` och maskar med `andi` är lika bra. **Fälla:** ett program som
tänder lysdioden när biten är 1 lyser när knappen är släppt, och förlorar poängen för aktivt låg.

---
