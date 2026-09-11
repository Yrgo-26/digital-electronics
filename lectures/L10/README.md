# L10 - Inporten, subrutiner och stacken

## Agenda
* Tecken är tal: ASCII-koder, och hur en byte blir två tecken med `swap` och `andi`.
* Tal större än 255: registerpar, `add`/`adc`, `sub`/`sbc`, `adiw`, `sbiw` och `movw`.
* En lång tidsfördröjning, exakt en sekund, med en 16-bitars loop.
* Inporten: `DDRD`, pull-up-motståndet och `PIND`, och varför en nedtryckt knapp läses som noll.
* Att testa en enda bit med `sbic` och `sbis`, och att vänta på en knapp.
* Subrutiner: `rcall`, `ret` och returadressen på stacken.
* Stacken som lagringsplats: `push`, `pop`, och kursens regel om att spara det man ändrar.
* **Labb 3**, del 18-23.

---

## Föreläsningsupplägg
Ungefär halva passet är genomgång och halva laboration, i den här ordningen:
1. **Från tal till text** (15 min). ASCII-tabellen och luckan mellan `'9'` och `'A'`.
   [`hex_to_ascii.asm`](./examples/hex_to_ascii.asm) stegas i simulatorn, med en förutsägelse före
   varje steg. Lägg märke till att samma fem rader står två gånger; det kommer vi tillbaka till.
2. **16 bitar** (15 min). Additionen 1000 + 2000 för hand, med minnessiffra, och sedan i
   [`add16.asm`](./examples/add16.asm). Vad händer om `adc` byts mot `add`?
3. **En sekund** (15 min). Cykelräkningen för
   [`one_second_delay.asm`](./examples/one_second_delay.asm) görs på tavlan, och stoppuret i
   simulatorn får bekräfta 16 000 000 cykler.
4. **Knappen** (15 min). Kopplingen med pull-up ritas, och
   [`led_follows_button.asm`](./examples/led_follows_button.asm) körs med knappen simulerad i
   I/O-fönstret.
5. **Subrutiner och stacken** (25 min). [`blink_subroutine.asm`](./examples/blink_subroutine.asm):
   `rcall` stegas med Memory-fönstret öppet, så att returadressen syns när den läggs på stacken, och
   de tre registren som `delay_ms` sparar ovanpå den. Sist
   [`push_pop.asm`](./examples/push_pop.asm), där två register byter värden.
6. **Labb 3, del 18-23** (90 min), i par, enligt
   [labs/lab3/d_io_and_subroutines.md](../../labs/lab3/d_io_and_subroutines.md).

Två förutsägelser att göra innan något körs:
* vilken text byten `0x3C` blir, och vilken byte varje tecken är;
* vad `SP` är mitt i `delay_ms`, när returadressen och tre register ligger på stacken.

---

## Före föreläsningen
* Gör klart Labb 3 till och med del 17. Den här föreläsningen använder loopar och villkorliga hopp
  från [L09](../L09/README.md) hela tiden.
* Läs [Appendix A](./appendix/a_ascii_and_16bit.md) och [Appendix B](./appendix/b_input_port.md).
* Repetera ASCII i [L01 Appendix B](../L01/appendix/b_binary_codes.md) och utporten i
  [L08 Appendix C](../L08/appendix/c_output_port.md).

---

## Efter föreläsningen
* Läs [Appendix C](./appendix/c_subroutines_and_stack.md), om subrutiner och stacken.
* Arbeta igenom [Appendix D](./appendix/d_exercises.md), och kontrollera svaren mot
  [Appendix E](./appendix/e_solutions.md).
* Gör klart Labb 3, del 18-23, om ni inte hann på passet. Del 21 krävs för godkänt.

---

## Det här ska du kunna efteråt
* Göra om ett värde 0-15 till sitt hexadecimala tecken och tillbaka, och en byte till två tecken.
* Skriva ett 16-bitars tal som två byte, och addera, subtrahera och jämföra 16-bitarstal med
  `add`/`adc`, `sub`/`sbc` och `cpi`/`cpc`.
* Räkna ut konstanterna för en fördröjning på en given tid, och kontrollera resultatet med stoppuret
  i simulatorn.
* Ställa in ett stift som ingång med pull-up, läsa det med `in` eller `sbic`/`sbis`, och förklara
  varför en nedtryckt knapp läses som noll.
* Skriva en subrutin, anropa den med `rcall`, och förklara vad som händer med stacken och `SP` vid
  `rcall`, `push`, `pop` och `ret`.
* Följa kursens regel: en subrutin sparar varje register den ändrar, och återställer dem i omvänd
  ordning.

---

## Frågor att testa dig själv med
* Varför behövs sju extra när värdet 12 ska bli tecknet `'C'`, men inte när 7 ska bli `'7'`?
* Ett 16-bitars resultat är exakt 256 för litet. Vilken instruktion har troligen bytts ut, och mot
  vilken?
* Varför fungerar `sbiw r24, 1` men inte `sbiw r20, 1`?
* En knapp mot jord läses som 1 när den är släppt. Vad är det som håller stiftet högt?
* `sbic PIND, 2` följt av `rjmp released`: vilket läge har knappen när `rjmp` hoppas över?
* `rcall` körs när `SP` är `0x08FF`. Var ligger returadressens två byte, och vad är `SP` sedan?
* En subrutin gör `push r16`, `push r17`, `pop r16`, `pop r17`. Vad händer med registren?
* Varför kan `delay_500ms` anropa `delay_ms` två gånger i rad utan att ladda om `r24` emellan?

---

## Referens
* [Appendix A](./appendix/a_ascii_and_16bit.md): ASCII-koder, 16-bitarstal och den långa
  fördröjningen.
* [Appendix B](./appendix/b_input_port.md): inporten, knappar och `sbic`/`sbis`.
* [Appendix C](./appendix/c_subroutines_and_stack.md): subrutiner, stacken, `push` och `pop`.
* [Appendix D](./appendix/d_exercises.md): övningarna.
* [Appendix E](./appendix/e_solutions.md): lösningsförslagen.
* [Exempelprogrammen](./examples/): alla program i appendixen, kontrollerade i simulatorn.
* [Referensbladet](../../info/avr_instructions.md) med kursens instruktioner.
* [info/microchip_studio.md](../../info/microchip_studio.md): hur en ingång simuleras (avsnitt 4.5)
  och hur stoppuret används (avsnitt 4.4).

---

## Nästa föreläsning
* Styrobjekt i verkligheten: lysdioder, knappar som studsar, och ett relä som styr en lampa på 24 V.
* Programmet flyttas från simulatorn till ett riktigt Arduino Uno-kort.
* Från flödesplan till program: ett trafikljus, steg för steg.
* Labb 3 slutförs med slutuppgiften, trafikljuset och övergångsstället.

---
