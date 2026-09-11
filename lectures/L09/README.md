# L09 - Programflöde, loopar och tidsfördröjningar

## Agenda
* Flödesplaner: att rita ett program innan det skrivs, med fem symboler.
* Jämförelser: `cp`, `cpi` och `tst`, och varför en jämförelse är en subtraktion utan resultat.
* Villkorliga hopp: `breq`, `brne`, `brlo`, `brsh` och de andra, och om-annars i assembler.
* Tal med och utan tecken: när `brlo` och när `brlt`.
* Loopar med ett bestämt antal varv, med räknaren i ett register.
* Tidsfördröjningar, räknade exakt från klockcykler och kontrollerade med simulatorns stoppur.
* Flerval, och att arbeta om en flödesplan så att programmet får en väg in och en väg ut.
* Labb 3, del 11, 12 och 14-17.

---

## Föreläsningsupplägg
Ungefär halva passet är genomgång och halva laboration, i den här ordningen:
1. **Flödesplanen** (10 min). De fem symbolerna, och värmaren ritad innan den skrivs.
2. **Jämförelse och hopp** (20 min). `cpi` följt av `brlo`, steg för steg i simulatorn, med
   flaggorna i Processor Status. Värmaren i [`compare_branch.asm`](./examples/compare_branch.asm),
   och det `rjmp` som håller isär grenarna.
3. **Med eller utan tecken** (5 min). -5 jämfört med 3: två hopp, två svar.
4. **Loopen** (15 min). Summan 1 + ... + 10 i [`count_loop.asm`](./examples/count_loop.asm): `dec`
   och `brne` räcker, och startvärdet 0 ger 256 varv.
5. **Tidsfördröjningar** (25 min). Cykeltabellen, fördröjningen i
   [`short_delay.asm`](./examples/short_delay.asm) räknad rad för rad, mätt med stoppuret, och sedan
   två loopar i varandra för nästan 10 ms.
6. **Flerval och omarbetning** (10 min). Lägesväljaren i [`menu.asm`](./examples/menu.asm), och
   varför alla grenar ska mötas i samma ruta.
7. **Labb 3, del 11, 12 och 14-17** (90 min), enligt
   [labs/lab3/c_program_flow.md](../../labs/lab3/c_program_flow.md).

Två förutsägelser att göra innan något körs:
* hur många gånger `brne` körs, och hur många av dem den hoppar, i en loop som går 200 varv;
* hur många klockcykler fördröjningen i `short_delay.asm` tar, och hur lång tid det är vid 16 MHz.

---

## Före föreläsningen
* Läs [Appendix A](./appendix/a_flowcharts_and_branches.md).
* Repetera flaggorna i [L08 Appendix A.6](../L08/appendix/a_arithmetic_and_flags.md#a6-flaggorna).
* Gör klart Labb 3, del 3-10, om ni inte hann i L08.

---

## Efter föreläsningen
* Läs [Appendix B](./appendix/b_loops_and_delays.md).
* Arbeta igenom [Appendix C](./appendix/c_exercises.md), och kontrollera svaren mot
  [Appendix D](./appendix/d_solutions.md).
* Fortsätt med Labb 3, del 11, 12 och 14-17.

---

## Det här ska du kunna efteråt
* Rita en flödesplan för ett program med beslut och loopar, och översätta den till assembler.
* Förklara vad `cp` och `cpi` gör med flaggorna, och välja rätt villkorligt hopp för ett villkor.
* Skriva om-annars, och förklara varför den första grenen slutar med ett `rjmp`.
* Välja mellan hopp för tal utan tecken och tal med tecken.
* Skriva en loop som går ett bestämt antal varv, och säga hur många varv den går för startvärdet 0.
* Räkna ut hur många klockcykler en fördröjning tar, och välja konstanter för en önskad tid.
* Mäta en tid i simulatorn med brytpunkter och stoppuret, och förklara en skillnad mot räkningen.
* Skriva ett flerval med en gemensam utgång.

---

## Frågor att testa dig själv med
* `cp r16, r17` följt av `brlo`: hoppar programmet om `r16` är mindre än `r17`, eller tvärtom?
* Varför behövs ingen `cpi` före `brne` i en loop som räknar ned med `dec`?
* Vad händer om `rjmp` efter den första grenen i ett om-annars saknas?
* En loop räknar ned från startvärdet 0. Hur många varv går den?
* Fördröjningen `ldi r18, 200` / `dec r18` / `brne` tar 600 cykler, inte 599 och inte 800. Varför?
* Varför går det inte att göra en fördröjning på en sekund med två loopar i varandra?
* Hur mäter du i simulatorn hur lång tid en del av programmet tar?

---

## Referens
* [Appendix A](./appendix/a_flowcharts_and_branches.md): flödesplaner, jämförelser och villkorliga
  hopp.
* [Appendix B](./appendix/b_loops_and_delays.md): loopar och tidsfördröjningar.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* [Exempelprogrammen](./examples/): `compare_branch.asm`, `count_loop.asm`, `short_delay.asm`,
  `long_delay.asm` och `menu.asm`.
* [info/avr_instructions.md](../../info/avr_instructions.md): referensbladet, med alla hopp och
  varje instruktions antal klockcykler.
* [info/microchip_studio.md, avsnitt
  4.4](../../info/microchip_studio.md#44-brytpunkter-och-cykelräknaren): brytpunkter och stoppuret.
* [Labb 3, del 11, 12 och 14-17](../../labs/lab3/c_program_flow.md).

---

## Nästa föreläsning
* ASCII-koder: att göra om ett tal till tecken.
* Tal med 16 bitar, och en fördröjning på en hel sekund.
* Inporten: att läsa knappar med `PIND`, och varför en nedtryckt knapp läses som noll.
* Subrutiner: att skriva fördröjningen en gång och anropa den många gånger.
* Stacken: var returadressen hamnar, och hur register sparas med `push` och `pop`.

---
