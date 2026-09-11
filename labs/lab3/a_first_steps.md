# Labb 3 - Del 1.1, 1.2 och 2: Första stegen

Delarna hör till [L07](../../lectures/L07/README.md). Läs
[L07 Appendix B](../../lectures/L07/appendix/b_assembly_language.md) och
[Appendix C](../../lectures/L07/appendix/c_microchip_studio_simulator.md) innan ni börjar, och ha
[info/microchip_studio.md](../../info/microchip_studio.md) öppen bredvid.

---

## Del 1.1 - Microchip Studio: skapa, skriva, spara, assemblera, simulera

### Mål
Skapa ett assemblerprojekt, skriva ett program, bygga det och stega igenom det i simulatorn.

### Bakgrund
Arbetsgången, skriv, bygg, förutsäg, stega och jämför, beskrivs i
[L07 Appendix C.1](../../lectures/L07/appendix/c_microchip_studio_simulator.md#c1-arbetsgången).
Instruktionerna i programmet står i
[L07 Appendix B.5](../../lectures/L07/appendix/b_assembly_language.md#b5-de-första-instruktionerna).

### Programmet

```asm
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ldi r16, 10                     ; r16 = 10
    ldi r17, 20                     ; r17 = 20
    mov r18, r16                    ; r18 = r16
    inc r18                         ; r18 = r18 + 1
    inc r18                         ; r18 = r18 + 1
    dec r17                         ; r17 = r17 - 1

end:
    rjmp end
```

### Uppgifter
1. Skapa ett projekt med namnet `lab3_01_1` enligt [info/microchip_studio.md, avsnitt
   2](../../info/microchip_studio.md#2-skapa-ett-assemblerprojekt).
2. Ersätt innehållet i `main.asm` med programmet ovan. **Skriv av det** i stället för att klistra
   in: det är så ni lär er hur en rad är uppbyggd. Kommentarerna kan ni hoppa över.
3. Spara med **Ctrl+S**.
4. Bygg med **F7**. Läs utskriften i fönstret Output: står det `0 errors`? Om inte, rätta raden
   Error List pekar på och bygg om.
5. Välj simulatorn som verktyg
   ([avsnitt 4.1](../../info/microchip_studio.md#41-välj-simulatorn)) och starta med
   **Debug → Start Debugging and Break** (**Alt+F5**). Öppna fönstret **Processor Status**.
6. **Innan ni stegar:** fyll i tabellen nedan med registrens värden efter varje instruktion,
   decimalt och hexadecimalt.

   | Efter | `r16` | `r17` | `r18` |
   |-------|-------|-------|-------|
   | `ldi r16, 10` | | | |
   | `ldi r17, 20` | | | |
   | `mov r18, r16` | | | |
   | `inc r18` | | | |
   | `inc r18` | | | |
   | `dec r17` | | | |

7. Stega med **F11**, en instruktion i taget, och jämför Processor Status med tabellen efter varje
   steg. Lägg märke till att registret som just ändrades visas i rött.
8. Läs av **Program Counter** vid varje steg. Med hur mycket ökar den för varje instruktion?
9. När den gula pilen står på `rjmp end`: vad visar **Cycle Counter**? Räkna ut värdet för hand
   först, med hjälp av [L07 Appendix
   C.5](../../lectures/L07/appendix/c_microchip_studio_simulator.md#c5-cykelräknaren).

### Frågor
* Den gula pilen står på `inc r18`. Har `inc r18` körts ännu?
* Ändras `r16` av instruktionen `mov r18, r16`?

*Redovisa* tabellen och simuleringen för läraren.

---

## Del 1.2 - Öppna, ändra, rätta, assemblera, simulera

### Mål
Öppna ett befintligt projekt, ändra programmet, och rätta fel med hjälp av felmeddelandena.

### Bakgrund
De vanligaste felmeddelandena, och hur de rättas, står i
[L07 Appendix C.4](../../lectures/L07/appendix/c_microchip_studio_simulator.md#c4-felmeddelanden).

### Uppgifter
1. Stäng Microchip Studio och starta det igen. Öppna projektet från del 1.1, antingen från listan
   över senaste projekt på startsidan eller med **File → Open → Project/Solution...**
2. Ändra programmet:
   * `r16` ska laddas med 25 i stället för 10;
   * lägg till raden `mov r19, r17` efter `dec r17`.
3. **Förutsäg** värdena i `r16`-`r19` när programmet når `end`. Bygg, simulera och kontrollera.
4. Lägg nu till de här fyra raderna direkt efter `mov r19, r17`. De innehåller fyra fel med flit:

   ```asm
       ldi r16 7
       ldi r5, 3
       inc r19, 2
       rjmp ennd
   ```

   Meningen med raderna är: ladda 7 i `r16`, ladda 3 i något register, öka `r19` med två, och hoppa
   till `end`.
5. Bygg. Läs det första felet i **Error List**, dubbelklicka på det, rätta raden och bygg om.
   Fortsätt tills programmet byggs utan fel. Skriv för varje fel ned vad meddelandet sa och hur ni
   rättade det.
6. **Förutsäg** värdena i `r16`-`r20` när programmet når `end`. Simulera och kontrollera.

### Frågor
* Hur många gånger behövde ni bygga om innan alla fel var borta? Fick ni alla fyra felen på en
  gång?
* Varför kan `inc` inte öka med två på en gång?

*Redovisa* det rättade programmet och de fyra felmeddelandena.

---

## Del 2 - Decimalt, binärt eller hexadecimalt

### Mål
Skriva tal i ett program decimalt, binärt och hexadecimalt, och läsa dem i simulatorn.

### Bakgrund
Talformaten står i [L07 Appendix
B.4](../../lectures/L07/appendix/b_assembly_language.md#b4-talformat) och omvandlingen mellan
talsystemen i [L01](../../lectures/L01/README.md).

### Uppgifter
1. Skriv ett program som laddar talet 200 i `r16` decimalt, i `r17` binärt och i `r18`
   hexadecimalt. Räkna ut det binära och det hexadecimala skrivsättet för hand.
   **Förutsäg** hur Processor Status visar de tre registren. Simulera och kontrollera.
2. Fyll i de tomma rutorna i tabellen **för hand**:

   | Register | Decimalt | Binärt | Hexadecimalt |
   |----------|----------|--------|--------------|
   | `r19` | 9 | | |
   | `r20` | | `0b00001111` | |
   | `r21` | | | `0x10` |
   | `r22` | 100 | | |
   | `r23` | | `0b01111111` | |
   | `r24` | | | `0x80` |
   | `r25` | 255 | | |

3. Lägg till en `ldi` per rad i programmet, som laddar registret med talet **i det skrivsätt
   tabellen ger det**: `ldi r19, 9`, `ldi r20, 0b00001111`, och så vidare. Simulera och kontrollera
   att Processor Status visar det hexadecimala värde ni räknade ut på varje rad.
4. Lägg till `ldi r26, '0'` och `ldi r27, 'A'`. Vilka värden får registren? Ett tecken lagras som
   ett tal, dess ASCII-kod; det återkommer i del 18.
5. Välj för varje rad i tabellen vilket skrivsätt som passar bäst om talet är
   * ett antal varv i en loop;
   * ett mönster av lysdioder som ska lysa.

### Frågor
* Blir maskinkoden olika för `ldi r16, 200` och `ldi r16, 0xC8`? Titta i listfilen om ni är osäkra
  ([L07 Appendix B.7](../../lectures/L07/appendix/b_assembly_language.md#b7-listfilen)).

*Redovisa* tabellen och simuleringen.

---
