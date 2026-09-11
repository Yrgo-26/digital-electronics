# Labb 3 - Del 3-10: Aritmetik, logik och flaggor

Delarna hör till [L08](../../lectures/L08/README.md). Varje del är ett eget projekt som utgår från
[mallen](./code/template.asm). Ha [referensbladet](../../info/avr_instructions.md) till hands.

**Förutsäg alltid först.** Varje del har uppgifter som börjar med *Förutsäg*. Skriv svaret på papper
eller som en kommentar i programmet innan ni stegar, och jämför sedan.

---

## Del 3 - Addition

### Mål
Addera med `add` och `inc`, och se vad som händer när summan inte får plats i en byte.

### Bakgrund
[L08 Appendix A.1 och
A.2](../../lectures/L08/appendix/a_arithmetic_and_flags.md#a1-addition-i-ett-register).

### Uppgifter
1. Skriv ett program som laddar 25 i `r16` och 17 i `r17`, och adderar dem med `add r16, r17`.
   **Förutsäg** `r16` decimalt, hexadecimalt och binärt. Simulera och kontrollera.
2. Gör samma addition för hand på papper, binärt, kolumn för kolumn med minnessiffror.
3. Lägg till en addition av två hexadecimala tal: `0x3A` i `r18` plus `0x15` i `r19`. **Förutsäg**
   `r18`, både hexadecimalt och decimalt.
4. Lägg till instruktioner som räknar ut 10 + 20 + 30 i `r20`. Hur många `add` behövs?
5. Lägg till en addition av 200 i `r23` och 100 i `r24`. **Förutsäg** `r23`. Titta sedan på
   flaggan `C` i Processor Status efter additionen. Vad betyder den här?

### Frågor
* Vilket av de två registren i `add r16, r17` ändras?
* Summan 200 + 100 = 300 får inte plats. Var finns "resten" av svaret efter additionen?

*Redovisa* programmet, uträkningen från uppgift 2 och svaret på frågorna.

---

## Del 4 - Subtraktion

### Mål
Subtrahera med `sub`, `subi` och `dec`, och addera en konstant utan en `addi`.

### Bakgrund
[L08 Appendix A.4](../../lectures/L08/appendix/a_arithmetic_and_flags.md#a4-subtraktion).

### Uppgifter
1. Räkna ut 50 - 20 med `sub`, med 50 i `r16` och 20 i `r17`. **Förutsäg** resultatet.
2. Ladda `0x20` i `r18` och dra ifrån `0x05` med `subi`. **Förutsäg** `r18` hexadecimalt och
   decimalt.
3. Ladda 3 i `r19` och kör `dec r19` tre gånger. **Förutsäg** `r19` och flaggan `Z` efter varje
   `dec`. Sätt en etikett efter den tredje, så kan ni köra dit med **Run To Cursor**.
4. Det finns ingen `addi`. Ladda 100 i `r20` och addera 28 med en `subi`. Vilken konstant ska
   `subi` ha? **Förutsäg** `r20`.
5. Räkna ut 20 - 50 med `sub`, med 20 i `r21` och 50 i `r22`. **Förutsäg** `r21` och `C`.

### Frågor
* Vad betyder `C = 1` efter en subtraktion?
* `r21` blev 226 i uppgift 5. Vilket tal är det om man läser det med tecken? Jämför med [L08
  Appendix
  A.5](../../lectures/L08/appendix/a_arithmetic_and_flags.md#a5-tvåkomplement-negativa-tal).

*Redovisa* programmet och förutsägelserna.

---

## Del 5 - Addition och subtraktion decimalt, binärt och hexadecimalt

### Mål
Räkna med tal som är skrivna i olika talsystem i samma uttryck.

### Bakgrund
[L07 Appendix B.4](../../lectures/L07/appendix/b_assembly_language.md#b4-talformat) och
[L01](../../lectures/L01/README.md).

### Uppgifter
Skriv ett program som räknar ut de tre uttrycken, med talen skrivna **precis som i uttrycket**.
**Förutsäg** först varje resultat decimalt, hexadecimalt och binärt, i en tabell.

1. `r20` = `0x3C` + `0b00001010` - 25
2. `r21` = `0b11110000` - `0x0F` + 1, där den sista additionen görs med `inc`
3. `r22` = `0b10101010` + `0x55`

| Register | Decimalt | Hexadecimalt | Binärt |
|----------|----------|--------------|--------|
| `r20` | | | |
| `r21` | | | |
| `r22` | | | |

Simulera och jämför med tabellen.

### Frågor
* Uttryck 3 ger ett särskilt bitmönster. Vilket, och varför blev det så? Titta på de två talen
  binärt.

*Redovisa* tabellen och simuleringen.

---

## Del 6 - Utporten PORTB, inc, I/O-simulering och .def

### Mål
Göra port B till utport, räkna på den, och följa bitarna i simulatorns I/O-fönster.

### Bakgrund
[L08 Appendix C](../../lectures/L08/appendix/c_output_port.md), särskilt C.3, C.6 och C.7.

### Programmet

```asm
.include "m328Pdef.inc"

.def counter = r16                  ; The value shown on port B.
.def temp = r17                     ; A scratch register.

.org 0x0000
    rjmp main

main:
    ser temp                        ; temp = 0xFF
    out DDRB, temp                  ; All eight pins of port B are outputs.
    clr counter                     ; Start counting at zero.

loop:
    out PORTB, counter              ; Show the count on port B.
    inc counter                     ; Count up.
    rjmp loop                       ; And again, forever.
```

### Uppgifter
1. Skriv av programmet, bygg och starta simuleringen. Öppna fönstret **I/O** (**Debug → Windows →
   I/O**) och välj port B.
2. Stega och följ rutorna i `DDRB` och `PORTB`. När blir alla rutor i `DDRB` fyllda?
3. **Förutsäg** hur rutorna i `PORTB` ser ut efter fem varv i loopen. Stega och kontrollera.
4. Varför ändras även `PINB`, fast programmet aldrig skriver dit?
5. Ändra programmet så att det räknar **nedåt**. **Förutsäg** vilket värde som visas direkt efter 0.
6. Ändra programmet så att det räknar uppåt i steg om **två**, med en enda instruktion i stället för
   `inc`.
7. Kör programmet fritt med **F5**, vänta några sekunder och stoppa med **Break All**. Går det att
   förutsäga värdet i `PORTB`? Hur lång tid tar ett varv i loopen, vid 16 MHz?

### Frågor
* Vad gör `.def`, och blir det någon skillnad i maskinkoden?
* Hur skulle lysdioderna se ut på ett riktigt kort om programmet kördes fritt?

*Redovisa* programmet med nedräkning och med steg om två, och svaren på frågorna.

---

## Del 7 - Logiska operationer

### Mål
Använda `andi`, `ori`, `eor` och `com` med masker för att ändra enskilda bitar.

### Bakgrund
[L08 Appendix B.1 och B.2](../../lectures/L08/appendix/b_logic_and_shifts.md#b2-masker).

### Uppgifter
Gör port B till utport först i programmet, och skriv varje resultat till `PORTB` med `out`, så att
det syns bit för bit i I/O-fönstret. **Förutsäg** varje resultat binärt innan ni stegar.

1. Ladda `0b10101010` i `r16` och behåll bara de fyra nedre bitarna.
2. Ladda `0b00110000` i `r17` och ettställ bit 7 och bit 0.
3. Ladda `0b00001111` i `r18` och invertera de fyra övre bitarna. Det finns ingen `eori`: hur gör
   ni?
4. Ladda `0b00110011` i `r19` och invertera alla bitar med en enda instruktion.
5. Ladda `0b01010101` i `r20`. Ettställ bit 1, nollställ bit 6 och invertera bit 7, med en
   instruktion per ändring. Vilket värde får `r20`, och vilka stift på port B lyser?

### Frågor
* Vilken instruktion och vilken sorts mask använder man för att nollställa bitar? För att ettställa?
* Varför ger `com` och `eor` med `0xFF` samma resultat?

*Redovisa* programmet och förutsägelserna.

---

## Del 8 - Rotationer och skift

### Mål
Skifta och rotera bitar, och använda skift för att multiplicera och dividera med 2.

### Bakgrund
[L08 Appendix B.3 och B.4](../../lectures/L08/appendix/b_logic_and_shifts.md#b3-skift).

### Uppgifter
**Förutsäg** varje resultat, och `C`, innan ni stegar.

1. Ladda 3 i `r16` och skifta vänster två gånger med `lsl`. Vilket tal har `r16` multiplicerats med?
2. Ladda 200 i `r17` och skifta höger två gånger med `lsr`.
3. Ladda `0b11110000` i `r18`, som är -16 med tecken, och kopiera det till `r19`. Skifta `r18` med
   `asr` och `r19` med `lsr`. Vilket av resultaten är -16 / 2?
4. Ladda `0b10010011` i `r20`, nollställ `C` med `clc`, och rotera vänster två gånger med `rol`.
   **Förutsäg** `r20` och `C` efter varje `rol`.
5. Skriv ett rinnande ljus på port B med `rol r21`, som i
   [L08 Appendix B.4](../../lectures/L08/appendix/b_logic_and_shifts.md#b4-rotation). Stega igenom
   ett helt varv, och följ `PORTB` och `C`. Hur många steg går det på ett varv, och varför är ett av
   dem mörkt?

### Frågor
* Varför används `asr` och inte `lsr` för att dividera ett tal med tecken med 2?
* *(Fördjupning)* Byt ut `rol r21` mot de två instruktionerna `lsl r21` och `adc r21, r25`, där
  `r25` har nollställts med `clr` före loopen. Hur många steg går ljuset nu på ett varv, och varför?

*Redovisa* det rinnande ljuset och förutsägelserna.

---

## Del 9 - Aritmetisk rundgång

### Mål
Se vad som händer när ett register räknas förbi 255 eller under 0, och vilka flaggor som visar det.

### Bakgrund
[L08 Appendix A.3](../../lectures/L08/appendix/a_arithmetic_and_flags.md#a3-aritmetisk-rundgång).

### Uppgifter
Sätt en etikett efter varje uppgift, så att ni kan köra fram till den och läsa SREG. **Förutsäg**
registret och flaggorna `Z` och `C` innan ni kör.

1. Nollställ `C` med `clc`. Ladda 250 i `r16` och kör `inc r16` sex gånger.
2. Ladda 255 i `r17` och 1 i `r18`, och addera dem med `add`.
3. Ladda 0 i `r19` och kör `dec r19`. Titta även på `N`.
4. Ladda 3 i `r20` och 5 i `r21`, och räkna ut `r20 - r21` med `sub`.
5. Ladda 200 i `r22` och 100 i `r23`, och addera dem.

### Frågor
* Efter uppgift 1 är `r16` = 0 och `Z` = 1. Vad är `C`, och varför?
* Efter uppgift 3 är `C` = 1. Är det `dec` som har satt den? Vilken instruktion satte den?
* Vilket tal ska man lägga till 44 för att få det "riktiga" svaret på uppgift 5?

*Redovisa* förutsägelserna och svaren på frågorna.

---

## Del 10 - Flaggorna i SREG

### Mål
Förutsäga flaggorna `C`, `Z`, `N`, `V`, `S` och `H` efter olika operationer, och kontrollera dem.

### Bakgrund
[L08 Appendix A.6 och A.7](../../lectures/L08/appendix/a_arithmetic_and_flags.md#a6-flaggorna).

### Uppgifter
1. Fyll i tabellen **för hand**. Varje rad görs för sig, med `add`, `sub`, `andi` eller `com` som
   anges.

   | Rad | Operation | Resultat | C | Z | N | V | S | H |
   |-----|-----------|----------|---|---|---|---|---|---|
   | a | `0x7F + 0x01` | | | | | | | |
   | b | `0xFF + 0x01` | | | | | | | |
   | c | `0x80 + 0x80` | | | | | | | |
   | d | `0x05 - 0x07` | | | | | | | |
   | e | `0x40 + 0x40` | | | | | | | |
   | f | `0x0F + 0x01` | | | | | | | |
   | g | `0x0F` AND `0xF0` (`andi`) | | | | | | | |
   | h | NOT `0x00` (`com`) | | | | | | | |

2. Skriv ett program med en rad per operation och en etikett efter varje, till exempel `row_a`,
   `row_b` och så vidare.
3. Kör fram till varje etikett och jämför SREG med tabellen. Markera varje ruta ni hade fel på.
4. För rad g och h: vilka flaggor ändrades inte av operationen? Jämför med kolumnen *Flaggor* på
   [referensbladet](../../info/avr_instructions.md).

### Frågor
* Rad a och rad e ger båda `V = 1`. Vad har de gemensamt?
* Rad d ger `C = 1` men `V = 0`. Är svaret rätt eller fel? Svara både utan och med tecken.

*Redovisa* tabellen, med era förutsägelser och de rätta värdena bredvid varandra.

---
