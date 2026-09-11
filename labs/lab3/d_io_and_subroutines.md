# Labb 3 - Del 18-23: Text, 16 bitar, inporten och subrutiner

Delarna hör till [L10](../../lectures/L10/README.md). Läs
[L10 Appendix A](../../lectures/L10/appendix/a_ascii_and_16bit.md) före del 18-20,
[Appendix B](../../lectures/L10/appendix/b_input_port.md) före del 21 och
[Appendix C](../../lectures/L10/appendix/c_subroutines_and_stack.md) före del 22-23. Instruktionerna
finns på [referensbladet](../../info/avr_instructions.md).

Del 21 krävs för godkänt. Del 18-20 och 22-23 krävs för VG, och del 22 behövs dessutom för
slutuppgiften i [L11](../../lectures/L11/README.md), så gör den även om ni inte siktar på VG.

---

## Del 18 - ASCII-koder för hexadecimala siffertecken

### Mål
Göra om värden till de tecken som skriver ut dem, och tillbaka, och lägga text i minnet.

### Bakgrund
ASCII-tabellen och luckan på sju mellan `'9'` och `'A'` finns i
[L10 Appendix A.1-A.2](../../lectures/L10/appendix/a_ascii_and_16bit.md#a2-en-siffra-blir-ett-tecken).
En byte blir två tecken med `swap` och `andi` enligt
[A.3](../../lectures/L10/appendix/a_ascii_and_16bit.md#a3-en-byte-blir-två-tecken), och `sts`
beskrivs i [A.5](../../lectures/L10/appendix/a_ascii_and_16bit.md#a5-att-lägga-text-i-minnet). Kom
ihåg att `subi r17, -0x30` adderar `0x30`.

### Uppgifter
1. **En siffra blir ett tecken.** Ladda `r17` med 7 och gör om det till tecknet `'7'` med en enda
   instruktion. *Förutsäg* `r17` hexadecimalt innan ni stegar.
2. **En hexadecimal siffra blir ett tecken.** Ladda `r18` med ett värde 0-15, kopiera det till `r19`
   och gör om `r19` till tecknet för siffran, med `cpi`, `brlo` och två `subi`. Fyll i tabellen
   **innan** ni kör programmet, och kontrollera sedan varje rad genom att byta värdet i `ldi`:

   | `r18` | `r19`, förutsagt | `r19`, i simulatorn |
   |-------|------------------|---------------------|
   | `0x00` | | |
   | `0x09` | | |
   | `0x0A` | | |
   | `0x0B` | | |
   | `0x0F` | | |

3. **En byte blir text.** Ladda `r16` med `0xA7`. Gör om den höga nibblen till ett tecken i `r20`
   och den låga till ett tecken i `r21`, och lägg dem på adress `0x0100` och `0x0101` med `sts`.
   Öppna fönstret **Memory**, välj **data IRAM** och gå till adress `0x0100`. Står texten `A7` i
   ASCII-kolumnen till höger? Prova också `0x3C`, `0xFF` och `0x00`.
4. **Tillbaka från tecken till värde.** Ladda `r22` med `'F'` och gör om det till värdet 15, enligt
   [A.4](../../lectures/L10/appendix/a_ascii_and_16bit.md#a4-tillbaka-från-tecken-till-värde). Prova
   också `'0'`, `'9'` och `'A'`.

### Frågor
* Varför måste den höga nibblen flyttas ned med `swap` innan den kan göras om till ett tecken?
* Vad blir tecknet om man glömmer `andi r20, 0x0F` efter `swap`, för byten `0xA7`?

*Redovisa* uppgift 3 och 4 i simulatorn, med texten synlig i Memory-fönstret.

---

## Del 19 - 16-bitarsoperationer

### Mål
Räkna med tal som inte får plats i en byte: addera, subtrahera, räkna och jämföra 16-bitarstal.

### Bakgrund
Registerpar och `low()`/`high()` finns i
[L10 Appendix A.6](../../lectures/L10/appendix/a_ascii_and_16bit.md#a6-tal-större-än-255), addition
och subtraktion med minnessiffra i
[A.7](../../lectures/L10/appendix/a_ascii_and_16bit.md#a7-addition-och-subtraktion-med-16-bitar),
`adiw`, `sbiw` och `movw` i
[A.8](../../lectures/L10/appendix/a_ascii_and_16bit.md#a8-adiw-sbiw-och-movw) och jämförelsen med
`cpi`/`cpc` i [A.9](../../lectures/L10/appendix/a_ascii_and_16bit.md#a9-att-jämföra-16-bitarstal).

### Uppgifter
1. **Addition.** Beräkna 1000 + 2000 med `r25:r24` och `r23:r22`, med `add` och `adc`. Kopiera
   resultatet till `r19:r18` med `movw`.

   *Förutsäg* först, med additionen uppställd för hand: vad blir `r24` och flaggan `C` efter `add`,
   och vad blir `r25` efter `adc`? Stega sedan och jämför i Processor Status.

2. **Subtraktion.** Beräkna 3000 - 1234 med `sub` och `sbc`, och lägg resultatet i `r21:r20`.
   *Förutsäg* båda bytena hexadecimalt. Blir det ett lån från den låga byten?
3. **En 16-bitars räknare.** Nollställ `r25:r24` och räkna upp det med `adiw` tills det är 1000, med
   `cpi` och `cpc` i loopen. Sätt en etikett direkt efter loopen.

   *Förutsäg* hur många cykler loopen tar, med samma metod som i L09. Mät sedan med brytpunkter före
   och efter loopen och fönstret Processor Status ([info/microchip_studio.md, avsnitt
   4.4](../../info/microchip_studio.md#44-brytpunkter-och-cykelräknaren)). Stämmer siffrorna? Om
   inte: vilket varv räknade ni fel på?

4. **När 16 bitar inte räcker.** Ladda `r27:r26` med `0xFFFF` och addera 1 med `adiw`. *Förutsäg*
   resultatet och flaggorna `C` och `Z`.

### Frågor
* Varför måste de låga bytena adderas först?
* Varför behövs registret med `high(1000)` i uppgift 3, när den låga byten kan jämföras direkt med
  `cpi`?

*Redovisa* uppgift 1-4, och er förutsägelse och mätning i uppgift 3.

---

## Del 20 - Lång tidsfördröjning

### Mål
Konstruera en fördröjning på en halv sekund, exakt på cykeln, och få en lysdiod att blinka en gång
per sekund.

### Bakgrund
Metoden, en 16-bitars inre loop i en yttre 8-bitars loop, och formeln `M(4N + 4)` finns i
[L10 Appendix A.10](../../lectures/L10/appendix/a_ascii_and_16bit.md#a10-en-lång-tidsfördröjning).
Exemplet där blinkar med en sekunds halvperiod; här ska det gå dubbelt så fort.

### Programmet
Fyll i de två konstanterna.

```asm
.include "m328Pdef.inc"

.equ OUTER_TURNS = ?                ; Work these two out before you run anything.
.equ INNER_TURNS = ?

.org 0x0000
    rjmp main

main:
    sbi DDRB, 5                     ; PB5, Arduino pin 13, is an output.
    ldi r17, 0b00100000             ; The mask that selects bit 5.

loop:
    in r16, PORTB                   ; Toggle PB5.
    eor r16, r17
    out PORTB, r16

delay_begin:
    ldi r20, OUTER_TURNS
delay_outer:
    ldi r24, low(INNER_TURNS)
    ldi r25, high(INNER_TURNS)
delay_inner:
    sbiw r24, 1
    brne delay_inner
    dec r20
    brne delay_outer
delay_end:
    rjmp loop
```

### Uppgifter
1. **Räkna först.** Hur många cykler är en halv sekund vid 16 MHz? Välj `INNER_TURNS` så att ett
   varv i den yttre loopen tar 200 000 cykler, och räkna ut `OUTER_TURNS`. Skriv upp uträkningen.
2. **Mät.** Sätt stoppurets frekvens till 16 MHz, sätt en brytpunkt på `delay_begin` och en på
   `delay_end`, och mät tiden mellan dem. *Förutsäg* stoppurets värde innan ni kör.
3. **Hela perioden.** Hur lång är en hel blinkperiod, från en tändning till nästa, räknat i cykler?
   Varför är den inte exakt en sekund? Hur mycket fel är den, i mikrosekunder?
4. **En annan tid.** Ändra till en fjärdedels sekund. Vilken av de två konstanterna ändrar ni, och
   till vad?

> **Tips.** Simulatorn behöver en stund för att köra åtta miljoner cykler. Använd **Continue**
> (**F5**) mellan brytpunkterna, inte **Step Into**.

### Frågor
* Varför är det enklare att välja ett "jämnt" antal cykler för den yttre loopen först, och räkna ut
  antalet varv sedan?
* Vad händer om `OUTER_TURNS` sätts till 0?

*Redovisa* uträkningen och mätningen.

---

## Del 21 - Inporten PORTD (PIND)

### Mål
Läsa knappar på port D och styra lysdioder på port B utifrån dem, och bygga logiska funktioner i
mjukvara.

### Bakgrund
Pull-up-motståndet och varför en nedtryckt knapp läses som 0 finns i
[L10 Appendix B.2](../../lectures/L10/appendix/b_input_port.md#b2-knappen-och-pull-up-motståndet),
att läsa hela porten i [B.3](../../lectures/L10/appendix/b_input_port.md#b3-att-läsa-hela-porten)
och `sbic`/`sbis` i
[B.4](../../lectures/L10/appendix/b_input_port.md#b4-att-testa-en-enda-bit-sbic-och-sbis). Så
simuleras en knapp:
[info/microchip_studio.md, avsnitt 4.5](../../info/microchip_studio.md#45-simulera-en-ingång).

I hela delen sitter knapparna mellan stiftet och jord, och de inbyggda pull-uparna används. En
**tom** ruta i `PIND` är alltså en **nedtryckt** knapp.

### Uppgifter
1. **Knapparna på lysdioderna.** Skriv av programmet `buttons_to_leds.asm` från
   [B.3](../../lectures/L10/appendix/b_input_port.md#b3-att-läsa-hela-porten). Kör till loopen,
   stoppa, och ändra `PIND` för hand. *Förutsäg* `PORTB` för varje rad innan ni stegar:

   | `PIND` | Nedtryckta knappar | `PORTB`, förutsagt | `PORTB`, i simulatorn |
   |--------|--------------------|--------------------|-----------------------|
   | `0b11111111` | | | |
   | `0b11111011` | | | |
   | `0b11110011` | | | |
   | `0b01111110` | | | |

2. **En knapp, en lysdiod.** Skriv ett program där lysdioden på PB5 lyser så länge knappen på PD2
   hålls nedtryckt, med `sbic` eller `sbis` och utan att läsa hela porten.
3. **AND och OR i mjukvara.** Två knappar, på PD2 och PD3. Lysdioden på PB0 ska lysa när **båda** är
   nedtryckta, och lysdioden på PB1 när **minst en** är det. Det är samma två funktioner som
   seriekopplingen och parallellkopplingen i [Labb 1](../lab1/README.md).

   Rita en flödesplan först. Fyll sedan i sanningstabellen, med förutsägelsen före simuleringen:

   | PD2 | PD3 | PB0 (AND) | PB1 (OR) |
   |-----|-----|-----------|----------|
   | släppt | släppt | | |
   | släppt | nedtryckt | | |
   | nedtryckt | släppt | | |
   | nedtryckt | nedtryckt | | |

4. **Extra.** Lägg till lysdioden på PB2, som ska lysa när **exakt en** av knapparna är nedtryckt.
   Vilken grind från [L02](../../lectures/L02/README.md) är det? Vilken koppling i Labb 1 gjorde
   samma sak?

### Frågor
* Vad läser programmet på en ingång utan pull-up, när knappen är släppt?
* I uppgift 3 behövs `com` och `andi` innan jämförelsen. Vad gör var och en av dem, och vad går fel
  om man hoppar över `andi`?
* Varför är det enklare att ändra funktionen i uppgift 3 än i Labb 1?

*Redovisa* uppgift 3, med sanningstabellen, i simulatorn.

---

## Del 22 - Subrutiner

### Mål
Flytta en fördröjning till en subrutin, se returadressen på stacken, och skriva en subrutin som tar
en parameter.

### Bakgrund
`rcall`, `ret`, stacken och stackpekaren finns i
[L10 Appendix C.2-C.3](../../lectures/L10/appendix/c_subroutines_and_stack.md#c3-stacken-och-stackpekaren),
subrutinen `delay_ms` med parameter i
[C.4](../../lectures/L10/appendix/c_subroutines_and_stack.md#c4-en-subrutin-med-parameter-delay_ms),
och en subrutin som anropar en annan i
[C.7](../../lectures/L10/appendix/c_subroutines_and_stack.md#c7-subrutiner-som-anropar-subrutiner).

Från och med den här delen ska varje program som använder `rcall` börja med att initiera
stackpekaren, med de fyra raderna i C.3.

### Uppgifter
1. **Fördröjningen blir en subrutin.** Ta programmet från del 20. Flytta fördröjningen, från
   `delay_begin` till och med `brne delay_outer`, till en subrutin `delay_500ms` som slutar med
   `ret`, och anropa den med `rcall` där fördröjningen stod. Lägg till initieringen av `SP`.
   Programmet ska blinka precis som förut.
2. **Returadressen.** *Förutsäg* `SP` före `rcall`, i början av subrutinen och efter `ret`. Leta upp
   adressen till instruktionen efter `rcall` i listfilen (`.lss`,
   [L07 Appendix B.7](../../lectures/L07/appendix/b_assembly_language.md#b7-listfilen)). Stega in i
   subrutinen med **F11** och läs de två översta bytena i stacken i fönstret Memory (**data IRAM**,
   adress `0x08FE`-`0x08FF`). Är det returadressen? Vilken byte ligger var?
3. **En parameter.** Skriv av `delay_ms` från
   [C.4](../../lectures/L10/appendix/c_subroutines_and_stack.md#c4-en-subrutin-med-parameter-delay_ms).
   Skriv om `delay_500ms` så att den laddar `r24` med 250 och anropar `delay_ms` två gånger. Glöm
   inte att `delay_500ms` själv ändrar `r24`, och alltså ska spara det.
4. **Järnvägsövergången.** Ändra huvudprogrammet så att lysdioderna på PB0 och PB1 blinkar växelvis,
   en halv sekund var, som vid en järnvägsövergång.
5. **Mät ett anrop.** *Förutsäg* hur många cykler ett anrop av `delay_500ms` tar, från `rcall` till
   instruktionen efter, med formeln för `delay_ms` och cyklerna för `rcall`, `push`, `ldi`, `pop`
   och `ret`. Mät sedan med stoppuret.
6. **Den djupaste punkten.** Stoppa programmet mitt i `delay_ms`, när den har anropats från
   `delay_500ms`. *Förutsäg* `SP` först, och kontrollera. Hur många byte ligger på stacken, och vad
   är var och en?

### Frågor
* Vad skulle hända om `delay_ms` inte sparade `r24`?
* `rcall` kostar 3 cykler och `ret` 4. Är det ett argument mot att använda subrutiner?

*Redovisa* uppgift 2, 4 och 5.

---

## Del 23 - Använda stacken som lagringsplats

### Mål
Använda `push` och `pop` för att spara register, förstå varför ordningen spelar roll, och se vad som
händer när stacken inte stämmer.

### Bakgrund
`push`, `pop` och sist in, först ut finns i
[L10 Appendix C.5](../../lectures/L10/appendix/c_subroutines_and_stack.md#c5-push-och-pop), och
kursens regel om att spara det man ändrar i
[C.6](../../lectures/L10/appendix/c_subroutines_and_stack.md#c6-kursens-regel-spara-det-du-ändrar).

### Programmet
Huvudprogrammet räknar i `r16` hur många gånger det har anropat `flash_all`, och slutar efter tre
gånger. Subrutinen `flash_all` tänder alla lysdioder på port B i 100 ms och släcker dem i 100 ms,
och använder själv `r16` till något helt annat. Den saknar `push` och `pop`, med flit.

```asm
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ldi r16, high(RAMEND)
    out SPH, r16
    ldi r16, low(RAMEND)
    out SPL, r16

    ldi r16, 0xFF
    out DDRB, r16                   ; Port B: all outputs.

    clr r16                         ; r16 counts the flashes.
loop:
    inc r16
    rcall flash_all
    cpi r16, 3
    brne loop
    out PORTB, r16                  ; Show the count.
end:
    rjmp end

flash_all:
    ldi r16, 0xFF                   ; All LEDs on ...
    out PORTB, r16
    ldi r24, 100
    rcall delay_ms                  ; ... for 100 ms ...
    clr r16                         ; ... and off ...
    out PORTB, r16
    ldi r24, 100
    rcall delay_ms                  ; ... for 100 ms.
    ret

; Copy delay_ms from L10 Appendix C.4 here.
```

### Uppgifter
1. **Byt plats med stacken.** Ladda `r20` med `0x55` och `r21` med `0xAA` i ett eget litet program.
   Lägg dem på stacken med `push r20`, `push r21`, och hämta dem med `pop r20`, `pop r21`.
   *Förutsäg* värdena i `r20` och `r21` efteråt, och `SP` efter varje instruktion.
2. **Felet.** Kör programmet ovan. *Förutsäg* först vad det gör. Hur många gånger blinkar det? Stega
   igenom ett varv i loopen och följ `r16`. Förklara vad som går fel.
3. **Rättningen.** Lägg till `push` och `pop` i `flash_all` så att subrutinen följer kursens regel.
   Vilka register måste sparas? Programmet ska nu blinka tre gånger och sedan visa talet 3 på
   lysdioderna.
4. **Djupet.** Stoppa programmet mitt i den första `delay_ms`. *Förutsäg* `SP`, och kontrollera. Hur
   många byte ligger på stacken, och vad är var och en?
5. **Fel ordning.** Byt plats på de två `pop` i `flash_all`, så att de inte längre står i omvänd
   ordning mot `push`. Vad händer? Förklara med stacken.
6. **En pop för lite.** Ta bort en av `pop`-instruktionerna. Stega fram till `ret` i `flash_all` och
   läs `SP`. Stega en gång till: vart hoppar programmet? Förklara med stacken.

### Frågor
* Varför måste `pop` göras i omvänd ordning mot `push`?
* Felet i uppgift 6 syns tydligare än felet i uppgift 5. Varför är det i själva verket en fördel?

*Redovisa* uppgift 2, 3 och 4.

---
