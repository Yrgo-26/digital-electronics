# Labb 3 - Mikrodatorn

## Mål
I Labb 3 programmerar du mikrodatorn ATmega328P i assembler. Du börjar med att ladda ett tal i ett
register och slutar med ett trafikljus som körs på ett riktigt Arduino Uno-kort. På vägen använder
du allt kursens mikrodatordel tar upp: talformat, aritmetik och flaggor, logiska operationer,
skift, villkorliga hopp, loopar, tidsfördröjningar, in- och utportar, subrutiner och stacken.

Efter laborationen ska du kunna:
* skapa, bygga, rätta och simulera ett assemblerprogram i Microchip Studio;
* förutsäga vad ett kort program gör med register, flaggor och portar, och kontrollera det i
  simulatorn;
* skriva program med beslut, loopar och tidsfördröjningar utifrån en flödesplan;
* programmera mikrodatorn att styra ett styrobjekt: lysdioder som tänds och släcks, och en knapp
  som läses av.

---

## Upplägg
Labb 3 löper över de fem mikrodatorpassen,
[L07](../../lectures/L07/README.md)-[L11](../../lectures/L11/README.md). Varje pass börjar med en
genomgång, och resten av passet är laborationstid. Laborationen består av många små delar som görs
**i ordning, så långt ni hinner**. Delarna bygger på varandra, så hoppa inte över någon.

* **Arbeta i par**, vid en dator med Microchip Studio installerat
  ([info/microchip_studio.md](../../info/microchip_studio.md)). Byt den som skriver vid varje ny
  del.
* **Ett projekt per del.** Döp projektet efter delen, till exempel `lab3_06` för del 6, så att ni
  kan öppna det igen vid redovisningen.
* **Förutsäg innan ni simulerar.** Varje del ber er skriva ned vad ni väntar er innan ni stegar. Gör
  det på riktigt, på papper eller i en kommentar i programmet. Det är förutsägelsen som visar om ni
  har förstått, och en avvikelse är det snabbaste sättet att hitta ett fel ([L07 Appendix
  C.3](../../lectures/L07/appendix/c_microchip_studio_simulator.md#c3-förutsäg-före-varje-steg)).
* **Redovisa** för läraren vid varje ställe som är markerat *Redovisa*. Visa programmet i
  simulatorn och förklara det; båda i paret ska kunna svara på frågor.

Nästan allt görs i simulatorn. Arduino-kortet behövs först i slutuppgiften, i L11.

---

## Programmallen
Varje program utgår från [mallen](./code/template.asm). Kopiera in den i `main.asm` när projektet
är skapat, och skriv programmet mellan `main:` och `end:`.

```asm
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

main:
    ; Write your program here.

end:
    rjmp end                        ; Stay here forever: there is nothing to return to.
```

Vad varje rad gör förklaras i [L07 Appendix
B.6](../../lectures/L07/appendix/b_assembly_language.md#b6-programmets-skelett). Instruktionerna
finns samlade på [referensbladet](../../info/avr_instructions.md).

---

## Delarna
Numreringen följer den laborationssamling kursen bygger på. Del 13 ingår inte, så numreringen
hoppar från 12 till 14.

| Del | Innehåll | Pass | Handledning |
|-----|----------|------|-------------|
| 1.1 | Microchip Studio: skapa, skriva, spara, assemblera, simulera | L07 | [a_first_steps.md](./a_first_steps.md) |
| 1.2 | Öppna, ändra, rätta, assemblera, simulera | L07 | [a_first_steps.md](./a_first_steps.md) |
| 2 | Decimalt, binärt eller hexadecimalt | L07 | [a_first_steps.md](./a_first_steps.md) |
| 3 | Addition | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 4 | Subtraktion | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 5 | Addition och subtraktion decimalt, binärt och hexadecimalt | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 6 | Utporten PORTB, inc, I/O-simulering och .def | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 7 | Logiska operationer | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 8 | Rotationer och skift | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 9 | Aritmetisk rundgång | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 10 | Flaggorna i SREG | L08 | [b_arithmetic_and_logic.md](./b_arithmetic_and_logic.md) |
| 11 | Vitsen med flaggor: jämförelse med cp | L09 | [c_program_flow.md](./c_program_flow.md) |
| 12 | Flödesplan och villkorliga hopp | L09 | [c_program_flow.md](./c_program_flow.md) |
| 14 | Loop med visst antal varv | L09 | [c_program_flow.md](./c_program_flow.md) |
| 15 | Kort tidsfördröjning | L09 | [c_program_flow.md](./c_program_flow.md) |
| 16 | Längre tidsfördröjning | L09 | [c_program_flow.md](./c_program_flow.md) |
| 17 | Flervalssituationer och omarbetning av flödesplaner | L09 | [c_program_flow.md](./c_program_flow.md) |
| 18 | ASCII-koder för hexadecimala siffertecken | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| 19 | 16-bitarsoperationer | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| 20 | Lång tidsfördröjning | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| 21 | Inporten PORTD (PIND) | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| 22 | Subrutiner | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| 23 | Använda stacken som lagringsplats | L10 | [d_io_and_subroutines.md](./d_io_and_subroutines.md) |
| A | Slutuppgift del A: trafikljuset | L11 | [e_final_task.md](./e_final_task.md) |
| B | Slutuppgift del B: övergångsställe | L11 | [e_final_task.md](./e_final_task.md) |

Varje pass hör ihop med en del av laborationen, men ni behöver inte bli klara med alla delar på
samma pass. Fortsätt där ni slutade nästa gång.

---

## Redovisning och bedömning

| Laboration | Krav för G | Krav för VG |
|------------|------------|-------------|
| Labb 3 | Del 1.1-12, 14-16, 21 och slutuppgiften del A | Samtliga delar 1.1-23 och slutuppgiften del B |

En del är godkänd när programmet är redovisat för läraren i simulatorn, eller på kortet i
slutuppgiften, och båda i paret kan förklara det. Skriv upp vilka delar som är redovisade, och
spara projekten tills kursen är slut.

---

## När något inte fungerar
* **Bygg om och läs det första felet** i Error List ([L07 Appendix
  C.4](../../lectures/L07/appendix/c_microchip_studio_simulator.md#c4-felmeddelanden)).
* **Stega fram till felet.** Leta upp den första instruktion där registren inte blir det ni
  förutsade. Felet sitter där eller strax före.
* **Ändra en sak i taget**, och bygg om efter varje ändring.
* **Fråga.** Läraren hjälper hellre till tidigt än ser er fastna i en halvtimme.

Vanliga fel samlas i tabellen i
[info/microchip_studio.md](../../info/microchip_studio.md#6-vanliga-fel).

---
