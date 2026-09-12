# Referensblad - AVR-instruktioner

De instruktioner och direktiv som används i kursen, för ATmega328P. Bladet delas ut tillsammans
med det skriftliga provet, och är tänkt att ligga bredvid tangentbordet under Labb 3.

`Rd` och `Rr` är vilket som helst av registren `r0`-`r31`. `K` är en konstant, 0-255. Instruktioner
med `K` fungerar **bara med `r16`-`r31`**. Klockfrekvensen på ett Arduino Uno-kort är 16 MHz, så en
klockcykel tar 62,5 ns.

Flaggorna i SREG: **C** carry (minnessiffra, eller lån vid subtraktion), **Z** zero (resultatet
blev noll), **N** negative (bit 7 i resultatet), **V** overflow (spill i tvåkomplement), **S** sign
(`N` xor `V`), **H** half carry (minnessiffra från bit 3). I kolumnen *Flaggor* står de flaggor
instruktionen kan ändra; övriga flaggor lämnas orörda.

---

## Direktiv
Direktiv är instruktioner till assemblern, inte till processorn. De blir ingen maskinkod.

| Direktiv | Exempel | Betydelse |
|----------|---------|-----------|
| `.include` | `.include "m328Pdef.inc"` | Läs in en annan fil, här registernamnen för ATmega328P. |
| `.org` | `.org 0x0000` | Lägg nästa instruktion på den här adressen i programminnet. |
| `.def` | `.def counter = r16` | Ge ett register ett namn. |
| `.equ` | `.equ LIMIT = 10` | Ge en konstant ett namn. |
| `low()`, `high()` | `ldi r16, low(RAMEND)` | Den låga respektive höga byten av ett 16-bitars värde. |

Talformat: decimalt `25`, binärt `0b00011001`, hexadecimalt `0x19` eller `$19`, tecken `'A'`.

---

## Dataöverföring

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `ldi Rd, K` | `ldi r16, 0x2A` | Rd = K | - | 1 |
| `mov Rd, Rr` | `mov r17, r16` | Rd = Rr | - | 1 |
| `movw Rd, Rr` | `movw r24, r22` | Rd+1:Rd = Rr+1:Rr (ett registerpar; Rd och Rr jämna) | - | 1 |
| `clr Rd` | `clr r16` | Rd = 0 | Z N V S | 1 |
| `ser Rd` | `ser r16` | Rd = 0xFF (bara `r16`-`r31`, som `ldi`) | - | 1 |
| `in Rd, A` | `in r16, PIND` | Rd = I/O-registret A | - | 1 |
| `out A, Rr` | `out PORTB, r16` | I/O-registret A = Rr | - | 1 |
| `lds Rd, k` | `lds r16, 0x0100` | Rd = byten på adress k i dataminnet (SRAM) | - | 2 |
| `sts k, Rr` | `sts 0x0100, r16` | Byten på adress k i dataminnet = Rr | - | 2 |
| `push Rr` | `push r16` | Lägg Rr på stacken | - | 2 |
| `pop Rd` | `pop r16` | Hämta Rd från stacken | - | 2 |

---

## Aritmetik

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `add Rd, Rr` | `add r16, r17` | Rd = Rd + Rr | H S V N Z C | 1 |
| `adc Rd, Rr` | `adc r17, r19` | Rd = Rd + Rr + C | H S V N Z C | 1 |
| `sub Rd, Rr` | `sub r16, r17` | Rd = Rd - Rr | H S V N Z C | 1 |
| `subi Rd, K` | `subi r16, 5` | Rd = Rd - K | H S V N Z C | 1 |
| `sbc Rd, Rr` | `sbc r17, r19` | Rd = Rd - Rr - C | H S V N Z C | 1 |
| `inc Rd` | `inc r16` | Rd = Rd + 1 | S V N Z | 1 |
| `dec Rd` | `dec r16` | Rd = Rd - 1 | S V N Z | 1 |
| `neg Rd` | `neg r16` | Rd = 0 - Rd (tvåkomplement) | H S V N Z C | 1 |
| `adiw Rd, K` | `adiw r24, 1` | Rd+1:Rd = Rd+1:Rd + K, K = 0-63 | S V N Z C | 2 |
| `sbiw Rd, K` | `sbiw r24, 1` | Rd+1:Rd = Rd+1:Rd - K, K = 0-63 | S V N Z C | 2 |

Det finns ingen `addi`. Addera en konstant genom att subtrahera dess negativa värde:
`subi r16, -5` adderar 5. `inc` och `dec` ändrar **inte** C. `adiw` och `sbiw` fungerar bara med
registerparen `r25:r24`, `r27:r26`, `r29:r28` och `r31:r30`.

---

## Logiska operationer

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `and Rd, Rr` | `and r16, r17` | Rd = Rd AND Rr, bit för bit | S V N Z | 1 |
| `andi Rd, K` | `andi r16, 0x0F` | Rd = Rd AND K | S V N Z | 1 |
| `or Rd, Rr` | `or r16, r17` | Rd = Rd OR Rr | S V N Z | 1 |
| `ori Rd, K` | `ori r16, 0x80` | Rd = Rd OR K | S V N Z | 1 |
| `eor Rd, Rr` | `eor r16, r17` | Rd = Rd XOR Rr | S V N Z | 1 |
| `com Rd` | `com r16` | Rd = NOT Rd (inverterar alla bitar) | S V N Z C | 1 |
| `tst Rd` | `tst r16` | Rd AND Rd: sätter Z och N, ändrar inte Rd | S V N Z | 1 |
| `swap Rd` | `swap r16` | Byter plats på de två halvorna (nibblarna) | - | 1 |

Efter `and`, `andi`, `or`, `ori`, `eor`, `com` och `tst` är V alltid 0. Efter `com` är C alltid 1.

---

## Skift och rotation

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `lsl Rd` | `lsl r16` | Skifta vänster; bit 7 till C, 0 in i bit 0 (Rd x 2) | H S V N Z C | 1 |
| `lsr Rd` | `lsr r16` | Skifta höger; bit 0 till C, 0 in i bit 7 (Rd / 2, utan tecken) | S V N Z C | 1 |
| `asr Rd` | `asr r16` | Skifta höger; bit 7 behålls (Rd / 2, med tecken) | S V N Z C | 1 |
| `rol Rd` | `rol r16` | Rotera vänster genom C: C in i bit 0, bit 7 till C | H S V N Z C | 1 |
| `ror Rd` | `ror r16` | Rotera höger genom C: C in i bit 7, bit 0 till C | S V N Z C | 1 |

---

## Jämförelse

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `cp Rd, Rr` | `cp r16, r17` | Beräknar Rd - Rr, sparar bara flaggorna | H S V N Z C | 1 |
| `cpc Rd, Rr` | `cpc r17, r19` | Beräknar Rd - Rr - C, sparar bara flaggorna | H S V N Z C | 1 |
| `cpi Rd, K` | `cpi r16, 100` | Beräknar Rd - K, sparar bara flaggorna | H S V N Z C | 1 |

---

## Hopp

| Instruktion | Hoppar om | Flagga | Cykler |
|-------------|-----------|--------|--------|
| `rjmp k` | alltid | - | 2 |
| `breq k` | lika (resultatet var noll) | Z = 1 | 1 / 2 |
| `brne k` | inte lika | Z = 0 | 1 / 2 |
| `brlo k` | lägre, utan tecken | C = 1 | 1 / 2 |
| `brsh k` | samma eller högre, utan tecken | C = 0 | 1 / 2 |
| `brlt k` | mindre än, med tecken | S = 1 | 1 / 2 |
| `brge k` | större än eller lika, med tecken | S = 0 | 1 / 2 |
| `brmi k` | negativt (bit 7 satt) | N = 1 | 1 / 2 |
| `brpl k` | positivt (bit 7 noll) | N = 0 | 1 / 2 |
| `brcs k` | carry satt | C = 1 | 1 / 2 |
| `brcc k` | carry noll | C = 0 | 1 / 2 |

`k` är en etikett. Ett villkorligt hopp tar **1 cykel om det inte hoppar och 2 om det hoppar**. Det
når högst 64 instruktioner bort; längre bort når man med ett `rjmp`.

---

## Subrutiner

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `rcall k` | `rcall delay` | Lägg returadressen på stacken och hoppa till k | - | 3 |
| `ret` | `ret` | Hämta returadressen från stacken och hoppa tillbaka | - | 4 |

---

## Bitinstruktioner

| Instruktion | Exempel | Gör | Flaggor | Cykler |
|-------------|---------|-----|---------|--------|
| `sbi A, b` | `sbi PORTB, 5` | Sätt bit b i I/O-registret A till 1 | - | 2 |
| `cbi A, b` | `cbi PORTB, 5` | Nollställ bit b i I/O-registret A | - | 2 |
| `sbic A, b` | `sbic PIND, 2` | Hoppa över nästa instruktion om bit b i A är 0 | - | 1 / 2 |
| `sbis A, b` | `sbis PIND, 2` | Hoppa över nästa instruktion om bit b i A är 1 | - | 1 / 2 |
| `sbrc Rr, b` | `sbrc r16, 0` | Hoppa över nästa instruktion om bit b i Rr är 0 | - | 1 / 2 |
| `sbrs Rr, b` | `sbrs r16, 7` | Hoppa över nästa instruktion om bit b i Rr är 1 | - | 1 / 2 |
| `clc` | `clc` | Nollställ carryflaggan: C = 0 | C | 1 |
| `sec` | `sec` | Ettställ carryflaggan: C = 1 | C | 1 |
| `nop` | `nop` | Ingenting, en cykel | - | 1 |

`sbi`, `cbi`, `sbic` och `sbis` når bara I/O-registren på adress 0-31, bland annat `PINB`, `DDRB`,
`PORTB`, `PIND`, `DDRD` och `PORTD`. En instruktion som hoppar över nästa tar 1 cykel om den inte
hoppar och 2 om den hoppar, eller 3 om instruktionen den hoppar över är två ord lång, som `lds` och
`sts`.

---

## I/O-registren i kursen

| Register | Betydelse |
|----------|-----------|
| `DDRB`, `DDRD` | Riktning: 1 = utgång, 0 = ingång, en bit per stift. |
| `PORTB`, `PORTD` | Utgång: nivån som drivs ut. Ingång: 1 = pull-up påslagen. |
| `PINB`, `PIND` | Stiftens verkliga nivå, att läsa. |
| `SPH`, `SPL` | Stackpekaren, hög och låg byte. `RAMEND` = 0x08FF. |
| `SREG` | Statusregistret, med flaggorna. |

---
