# L07 - Mikrodatorn och Microchip Studio

## Agenda
* ATmega328P: mikrodatorn från L06:s blockschema, som en verklig krets på ett Arduino Uno-kort.
* De 32 registren, och varför bara hälften av dem kan laddas med en konstant.
* Statusregistret, programräknaren och de tre minnena.
* Vad en instruktion är: `ldi r16, 0x2A` isärplockad till de sexton bitar den blir.
* Assemblerspråkets byggstenar: instruktioner, operander, etiketter, kommentarer och direktiv.
* Talformat: samma tal skrivet decimalt, binärt och hexadecimalt.
* Microchip Studio: projekt, assemblering, felmeddelanden och simulering.
* **Labb 3 startar**: del 1.1, 1.2 och 2.

---

## Föreläsningsupplägg
Ungefär halva passet är genomgång och halva laboration, i den här ordningen:
1. **Från blockschema till krets** (10 min). L06:s mikrodator, nu med namn och siffror:
   ATmega328P, 32 register, 32 kB flash, 2 kB SRAM, 16 MHz.
2. **Registren, SREG och minnena** (20 min), läst ur figurerna i
   [Appendix A](./appendix/a_avr_core.md). Inget program körs ännu; poängen är att veta vad man
   skriver *för*.
3. **En instruktion isärplockad** (10 min). `ldi r16, 0x2A` är sexton bitar, och varje bit har en
   uppgift. Förutsäg ordet innan det visas.
4. **Assemblerspråket** (15 min). En rad i fyra delar, direktiven, talformaten, och de första åtta
   instruktionerna.
5. **Live i Microchip Studio** (25 min). Ett nytt projekt skapas,
   [`first_program.asm`](./examples/first_program.asm) skrivs, byggs och stegas, med en förutsägelse
   före varje steg. Ett fel läggs in med flit, och felmeddelandet läses.
6. **Labb 3, del 1.1, 1.2 och 2** (90 min), i par, enligt
   [labs/lab3/a_first_steps.md](../../labs/lab3/a_first_steps.md).

Två förutsägelser att göra innan något körs:
* vilket 16-bitars ord `ldi r16, 0x2A` blir, utifrån kodningen ensam;
* vad `r18` innehåller efter `mov r18, r16` följt av `inc r18`, när `r16` är 5.

---

## Före föreläsningen
* **Installera Microchip Studio** enligt [info/microchip_studio.md](../../info/microchip_studio.md),
  avsnitt 1. Installationen tar tid och ska vara klar före passet.
* Läs [Appendix A](./appendix/a_avr_core.md) och [Appendix B](./appendix/b_assembly_language.md).
* Repetera mikrodatorns blockschema i [L06 Appendix B](../L06/appendix/b_microcomputer.md) och
  omvandlingen mellan talsystem i [L01](../L01/README.md).

---

## Efter föreläsningen
* Läs [Appendix C](./appendix/c_microchip_studio_simulator.md), om hur simulatorn används.
* Arbeta igenom [Appendix D](./appendix/d_exercises.md), och kontrollera svaren mot
  [Appendix E](./appendix/e_solutions.md).
* Gör klart Labb 3, del 1.1, 1.2 och 2, om ni inte hann på passet.

---

## Det här ska du kunna efteråt
* Beskriva ATmega328P:s delar, register, statusregister, programräknare och minnen, och koppla dem
  till mikrodatorns blockschema.
* Säga vilka register `ldi` kan ladda, och förklara varför utifrån instruktionens kodning.
* Förklara skillnaden mellan programminnet och dataminnet.
* Läsa en rad assembler och peka ut etikett, instruktion, operander och kommentar.
* Skriva samma tal decimalt, binärt och hexadecimalt i ett program.
* Skapa ett projekt i Microchip Studio, bygga det, rätta felen, och stega programmet i
  simulatorn.
* Förutsäga registrens värden efter varje instruktion i ett kort program, och kontrollera
  förutsägelsen i simulatorn.

---

## Frågor att testa dig själv med
* Varför kan `ldi` ladda `r16` men inte `r15`? Hur löser du det om du ändå behöver en konstant i
  `r5`?
* Den gula pilen i simulatorn står på `inc r18`. Har `inc r18` körts?
* Vad händer om du tar bort raden `rjmp end` sist i programmet?
* `ldi r16, 200`, `ldi r16, 0b11001000` och `ldi r16, 0xC8`: vad skiljer maskinkoden åt?
* Vad är skillnaden mellan en instruktion och ett direktiv? Blir `.def counter = r16` någon
  maskinkod?
* Ett program assembleras utan fel men ger fel resultat. Vad säger det om vad assemblern
  kontrollerar?

---

## Referens
* [Appendix A](./appendix/a_avr_core.md): mikrodatorn ATmega328P.
* [Appendix B](./appendix/b_assembly_language.md): assemblerspråket.
* [Appendix C](./appendix/c_microchip_studio_simulator.md): simulering i Microchip Studio.
* [Appendix D](./appendix/d_exercises.md): övningarna.
* [Appendix E](./appendix/e_solutions.md): lösningsförslagen.
* [Exempelprogrammen](./examples/): `first_program.asm` och `number_formats.asm`.
* [info/microchip_studio.md](../../info/microchip_studio.md): installation, projekt och simulator.
* [info/avr_instructions.md](../../info/avr_instructions.md): referensbladet med instruktionerna.
* [Labb 3](../../labs/lab3/README.md): laborationen som börjar i det här passet.
* [ATmega328P
  datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
  och [AVR Instruction Set
  Manual](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf):
  källorna till varje siffra i mikrodatordelen.

---

## Nästa föreläsning
* Addition och subtraktion i registren, och vad som händer när resultatet inte får plats.
* Tvåkomplement: hur samma byte kan vara 255 eller -1.
* Flaggorna i SREG: vad varje instruktion lämnar efter sig.
* Logiska operationer, skift och rotation.
* Utporten: de första lysdioderna, i simulatorns I/O-fönster.

---
