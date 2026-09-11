# L08 - Aritmetik, logik och flaggor

## Agenda
* Addition och subtraktion i registren, och varför det inte finns någon `addi`.
* Aritmetisk rundgång: efter 255 kommer 0, och `inc` säger inte till.
* Tvåkomplement: hur samma byte kan vara 255 eller -1.
* Flaggorna i SREG: vad `C`, `Z`, `N`, `V`, `S` och `H` betyder, och vilka instruktioner som ändrar
  dem.
* Logiska operationer och masker: att ettställa, nollställa, invertera och testa enskilda bitar.
* Skift och rotation: multiplikation och division med 2, och ett rinnande ljus.
* Utporten: `DDRB`, `PORTB`, `out`, `sbi` och `cbi`, och portarna i simulatorns I/O-fönster.
* Labb 3, del 3-10.

---

## Föreläsningsupplägg
Ungefär halva passet är genomgång och halva laboration, i den här ordningen:
1. **Addition, som i L01, men i ett register** (10 min). 25 + 17 för hand, sedan i simulatorn.
2. **När summan inte får plats** (15 min). 200 + 100 blir 44, och carryflaggan tar hand om resten.
   Rundgången på urtavlan, och fällan: `inc` och `dec` ändrar inte `C`.
3. **Negativa tal** (15 min). Tvåkomplement, "invertera och lägg till 1", och varför samma `add`
   fungerar för båda tolkningarna.
4. **Flaggorna** (15 min). De fyra exemplen i [`flags_demo.asm`](./examples/flags_demo.asm):
   förutsäg varje flagga innan simulatorn visar den.
5. **Masker, skift och rotation** (15 min). Samma byte med tre masker; `lsl` som multiplikation; det
   rinnande ljuset i [`running_light.asm`](./examples/running_light.asm) och varför ett steg är
   mörkt.
6. **Utporten** (15 min). `DDRB` och `PORTB`, `out`, `sbi` och `cbi`, och en räknare som syns i
   I/O-fönstret.
7. **Labb 3, del 3-10** (90 min), enligt
   [labs/lab3/b_arithmetic_and_logic.md](../../labs/lab3/b_arithmetic_and_logic.md).

Två förutsägelser att göra innan något körs:
* vad `r16` och `C` blir efter `add` när `r16` = 200 och `r17` = 100;
* vilka flaggor som sätts av `0x7F + 0x01`, och särskilt om `V` blir 0 eller 1.

---

## Före föreläsningen
* Läs [Appendix A](./appendix/a_arithmetic_and_flags.md).
* Repetera binär addition i [L01 Appendix A](../L01/appendix/a_number_systems.md), och grindarnas
  sanningstabeller i [L02 Appendix A](../L02/appendix/a_logic_gates.md).
* Gör klart Labb 3, del 1.1, 1.2 och 2, om ni inte hann i L07.

---

## Efter föreläsningen
* Läs [Appendix B](./appendix/b_logic_and_shifts.md) och [Appendix C](./appendix/c_output_port.md).
* Arbeta igenom [Appendix D](./appendix/d_exercises.md), och kontrollera svaren mot
  [Appendix E](./appendix/e_solutions.md).
* Fortsätt med Labb 3, del 3-10.

---

## Det här ska du kunna efteråt
* Addera och subtrahera binärt för hand, och säga vad ett register och `C` innehåller efteråt.
* Förklara aritmetisk rundgång, och varför `inc` och `dec` inte ändrar `C`.
* Omvandla mellan ett negativt tal och dess tvåkomplement, och läsa samma byte med och utan tecken.
* Förutsäga `C`, `Z`, `N` och `V` efter en addition eller subtraktion, och förklara skillnaden
  mellan `C` och `V`.
* Välja mask och instruktion för att ettställa, nollställa, invertera eller testa enskilda bitar.
* Använda skift för att multiplicera och dividera med 2, och förklara skillnaden mellan `lsr` och
  `asr`.
* Göra en port till utport, och tända och släcka enskilda stift med `out`, `sbi` och `cbi`.

---

## Frågor att testa dig själv med
* `r16` är 255 och `C` är 0. Vad är `r16` och `C` efter `inc r16`? Och efter `add r16, r17` med
  `r17` = 1?
* Varför finns det ingen `addi`, och hur adderar man 5 till `r16` ändå?
* Byten `0xF6`: vilket tal är den utan tecken, och vilket med tecken?
* `0x80 - 0x01` ger `C = 0` men `V = 1`. Vad säger det om svaret, utan tecken och med tecken?
* Vilken instruktion och mask nollställer bit 7 i `r16` utan att röra de andra bitarna?
* Varför är ett av nio steg mörkt i det rinnande ljuset med `rol`?
* `out PORTB, r16` och `sbi PORTB, 3`: vad skiljer dem åt, när det gäller de andra sju stiften?

---

## Referens
* [Appendix A](./appendix/a_arithmetic_and_flags.md): aritmetik, tvåkomplement och flaggor.
* [Appendix B](./appendix/b_logic_and_shifts.md): logiska operationer, skift och rotation.
* [Appendix C](./appendix/c_output_port.md): utporten.
* [Appendix D](./appendix/d_exercises.md): övningarna.
* [Appendix E](./appendix/e_solutions.md): lösningsförslagen.
* [Exempelprogrammen](./examples/): `flags_demo.asm`, `masks.asm`, `running_light.asm` och
  `leds_on_portb.asm`.
* [info/avr_instructions.md](../../info/avr_instructions.md): referensbladet, med vilka flaggor
  varje instruktion ändrar.
* [Labb 3, del 3-10](../../labs/lab3/b_arithmetic_and_logic.md).

---

## Nästa föreläsning
* Flödesplaner: att rita ett program innan det skrivs.
* Jämförelser och villkorliga hopp: det flaggorna är till för.
* Loopar som går ett bestämt antal varv.
* Tidsfördröjningar, beräknade exakt från klockcykler och kontrollerade med simulatorns stoppur.

---
