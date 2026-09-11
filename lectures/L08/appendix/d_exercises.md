# Appendix D - Övningar

> **Så kontrollerar du ditt arbete.** Övningarna märkta **Program** och **Kontroll** görs i
> Microchip Studio: skriv programmet, bygg och stega, och läs registren i Processor Status och
> portarna i I/O-fönstret. Skriv ned din förutsägelse innan du stegar.
>
> Övriga övningar görs med papper och penna, utan miniräknare. Lösningsförslag finns i
> [Appendix E](./e_solutions.md).

Varje övning är märkt med sin sort. Det finns en **Kontroll** i det här passet, övning 5.

---

## 1. Binär addition för hand
**Räkna för hand.**

Addera binärt, kolumn för kolumn med minnessiffror, och ange resultatet i en byte, hexadecimalt,
och värdet på `C` efteråt.

**a)** `0b00101101 + 0b00010111`

**b)** `0x9C + 0x7A`

**c)** `0x0F + 0x01`. Vilken flagga, utöver `Z`, `N` och `C`, sätts här, och varför?

---

## 2. Mätaren slår om
**Förståelse.**

`r16` innehåller 253 och `C` är 0. Programmet kör `inc r16` fem gånger i rad.

**a)** Vilket värde har `r16` efter varje `inc`?

**b)** Efter vilken `inc` är `Z = 1`? Vad är `Z` när alla fem är körda?

**c)** Vad är `C` efter den femte `inc`? Varför?

**d)** Hur skulle du ändra programmet så att `C` blir 1 när räknaren slår om från 255 till 0?

---

## 3. Negativa tal
**Räkna för hand.**

**a)** Skriv -1, -10, -100 och -128 som byte i tvåkomplement, hexadecimalt. Visa metoden "invertera
och lägg till 1" för -10.

**b)** Vilka tal med tecken är `0xF0`, `0x81` och `0x7F`?

**c)** Vad blir `neg r16` om `r16` är `0x01`, `0x80` respektive `0x00`? Ett av svaren är
överraskande. Vilket, och varför?

---

## 4. Addera en konstant
**Program.**

**a)** Skriv ett program som laddar 40 i `r16` och sedan adderar 25 till det, utan att använda ett
andra register.

**b)** Lägg till instruktioner som laddar 30 i `r17` och drar ifrån 100.

**c)** Förutsäg `r16`, `r17` och `C` när programmet är klart. Simulera och kontrollera.

---

## 5. Flaggorna
**Kontroll.** *Förutsäg för hand, kontrollera i simulatorn, förklara skillnaderna.*

**a)** Fyll i tabellen **för hand**: resultatet hexadecimalt och flaggorna `C`, `Z`, `N`, `V` och
`S` efter varje operation. Operationerna görs var för sig, inte efter varandra.

| Operation | Resultat | C | Z | N | V | S |
|-----------|----------|---|---|---|---|---|
| `0x50 + 0x50` (`add`) | | | | | | |
| `0xF0 + 0x20` (`add`) | | | | | | |
| `0x30 - 0x30` (`sub`) | | | | | | |
| `0x00 - 0x01` (`sub`) | | | | | | |
| `0x80 - 0x01` (`sub`) | | | | | | |
| `0xFF + 1` med `inc`, när `C` är 1 före | | | | | | |

**b)** Skriv ett program som gör de sex operationerna i ordning, med en etikett efter varje, som i
[`flags_demo.asm`](../examples/flags_demo.asm). Sätt `C` till 1 före den sista med instruktionen
`sec` (*set carry*).

**c)** Kör fram till varje etikett och jämför SREG med tabellen. Stämde allt? Förklara varje ruta
där du hade fel, och säg vilken regel i [Appendix A](./a_arithmetic_and_flags.md) du hade missat.

---

## 6. Masker
**Räkna för hand.**

`r16` innehåller `0b11010011`. Vad blir `r16` efter var och en av instruktionerna nedan? Varje
instruktion utgår från `0b11010011`.

**a)** `andi r16, 0xF0`

**b)** `ori r16, 0x0C`

**c)** `eor r16, r24`, där `r24` innehåller `0xFF`

**d)** `com r16`. Jämför med **c)**.

---

## 7. Välj rätt mask
**Konstruktion.**

Skriv en instruktion, eller två om det behövs, som gör följande med `r16` och lämnar alla andra
bitar orörda:

**a)** ettställer bit 0 och bit 1;

**b)** nollställer bit 7;

**c)** inverterar bit 4-7;

**d)** nollställer alla bitar utom bit 3;

**e)** nollställer bit 0-3 och ettställer bit 7.

---

## 8. Skift och rotation
**Räkna för hand.**

**a)** `r16` innehåller `0b00000110`. Vad blir den efter två `lsl`? Vilket tal har den
multiplicerats med?

**b)** `r17` innehåller `0b10000001`. Vad blir `r17` och `C` efter en `lsr`?

**c)** `r18` innehåller `0xF8`, det vill säga -8. Vad blir den efter en `asr`, och efter en `lsr`?
Vilket av svaren är -8 / 2?

**d)** `r19` innehåller `0b11000000` och `C` är 0. Vad blir `r19` och `C` efter var och en av tre
`rol` i rad?

---

## 9. Lysdioder på port B
**Program.**

**a)** Skriv ett program som gör port B till utport och tänder lysdioderna på PB0, PB2 och PB4 med
en enda `out`.

**b)** Skriv om programmet så att samma tre lysdioder tänds med `sbi`, en i taget, i stället.

**c)** Lägg till instruktioner som släcker PB2 med `cbi`, och sedan tänder PB7 med mönstret läs,
ändra, skriv ([Appendix C.5](./c_output_port.md#c5-ändra-några-stift-med-en-mask)).

**d)** Förutsäg `PORTB` efter programmet, binärt. Kontrollera i I/O-fönstret.

---

## 10. Läs programmet
**Förståelse.**

Förutsäg `PORTB`, binärt, efter var och en av de markerade raderna.

```asm
.def leds = r16
.def temp = r17

main:
    ser temp
    out DDRB, temp
    ldi leds, 0b00001111
    out PORTB, leds                 ; (1)
    lsl leds
    lsl leds
    out PORTB, leds                 ; (2)
    sbi PORTB, 0                    ; (3)
    com leds
    out PORTB, leds                 ; (4)
    cbi PORTB, 7                    ; (5)
end:
    rjmp end
```

---

## 11. Multiplicera med tio
**Program.** *(fördjupning)*

Processorn har ingen instruktion som multiplicerar med 10, men 10x = 8x + 2x, och multiplikation med
2 och 8 är skift.

**a)** Skriv ett program som laddar ett tal x i `r16` och räknar ut 10x i `r16`, med `mov`, `lsl`
och `add`.

**b)** Prova med x = 7. Vad blir resultatet, decimalt och hexadecimalt?

**c)** Upp till vilket x ger programmet rätt svar? Vad händer för större x?

---

## 12. När är det overflow?
**Förståelse.** *(fördjupning)*

**a)** `0x40 + 0x40` ger `V = 1`, men `0xC0 + 0xC0` ger `V = 0`. Förklara båda genom att läsa talen
med tecken.

**b)** Vad blir `C` i de två fallen? Förklara genom att läsa talen utan tecken.

**c)** Formulera med egna ord en regel för när en addition ger `V = 1`.

---
