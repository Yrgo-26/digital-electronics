# L11 - Styrobjekt på riktig hårdvara

## Agenda
* Styrobjekt: ingångar, beslut och utgångar, och varför mikrodatorn har tagit över efter reläer.
* Lysdioden och förkopplingsmotståndet, räknat med Ohms lag.
* Större laster: en transistor som drar ett relä, som tänder lampan på 24 V från Labb 1.
* Knappar som studsar, och avstudsning med en kort väntan.
* Arduino Uno-kortet, och hur programmet förs över från Microchip Studio.
* Från flödesplan till program: vägarbetsljuset som genomarbetat exempel.
* **Labb 3** slutförs: slutuppgiften, trafikljuset och övergångsstället, på kortet.

---

## Föreläsningsupplägg
Passet är till största delen laborationstid, med en kort genomgång först:
1. **Från simulatorn till verkligheten** (10 min). Ingångar, beslut, utgångar: samma bild som i Labb
   1 och Labb 2, med ett program i mitten.
2. **Utgångar** (10 min). Strömmen genom en lysdiod räknas ut på tavlan. Reläkopplingen visas, och
   varför dioden behövs.
3. **Knappar som studsar** (5 min). [`press_counter.asm`](./examples/press_counter.asm) körs på ett
   kort, först med och sedan utan väntan, och antalet tryck jämförs.
4. **Vägarbetsljuset** (20 min). Tabellen, flödesplanen och programmet
   [`roadwork_light.asm`](./examples/roadwork_light.asm) byggs upp i den ordningen. Programmet
   testas i simulatorn med `QUARTER_MS` = 1 och förs sedan över till kortet, live.
5. **Labb 3: slutuppgiften och det som återstår** (2 h 15 min), i par, enligt
   [labs/lab3/e_final_task.md](../../labs/lab3/e_final_task.md). Den som inte är klar med del 1.1-23
   gör klart dem först. Redovisningen av Labb 3 avslutas i slutet av passet.

Två förutsägelser att göra innan något körs:
* hur stor strömmen genom en röd lysdiod med 220 Ω blir, och vad multimetern kommer att visa;
* hur många tryck `press_counter.asm` räknar för fem tryck när väntan är borttagen.

---

## Före föreläsningen
* Gör klart Labb 3, del 22. Slutuppgiften bygger på subrutiner.
* Läs [Appendix A](./appendix/a_control_objects.md) och [Appendix B](./appendix/b_traffic_light.md).
* Installera Arduino IDE och gör inställningen i
  [info/microchip_studio.md, avsnitt 5](../../info/microchip_studio.md#5-programmera-ett-arduino-kort-från-microchip-studio)
  hemma, om du har egen dator. Då går passet till att programmera, inte till att installera.
* Rita flödesplanen för slutuppgiftens del A. Den ska redovisas innan programmet skrivs.

---

## Efter föreläsningen
* Arbeta igenom [Appendix C](./appendix/c_exercises.md), och kontrollera svaren mot
  [Appendix D](./appendix/d_solutions.md).
* Se till att alla delar av Labb 3 som krävs för ert betyg är redovisade. Kraven står i
  [kursinformationen](../../info/README.md#examination).
* Förbered det skriftliga provet i [L12](../L12/README.md), med
  [övningsprovet](../../exam/practice_exam.md).

---

## Det här ska du kunna efteråt
* Beskriva ett styrsystem som ingångar, beslut och utgångar, och peka ut dem i ett exempel.
* Räkna ut förkopplingsmotståndet för en lysdiod, och förklara varför det behövs.
* Förklara hur en transistor och ett relä låter mikrodatorn styra en last på 24 V, och vad dioden
  över spolen gör.
* Förklara varför en knapp studsar, när det spelar roll, och hur en kort väntan löser det.
* Gå från en tillståndstabell till en flödesplan och ett program, och testa programmet först i
  simulatorn och sedan på ett riktigt kort.
* Felsöka ett program på kortet: skilja ett programfel från ett kopplingsfel.

---

## Frågor att testa dig själv med
* Varför får en lysdiod aldrig kopplas direkt mellan ett stift och jord?
* Ett stift tål 40 mA. Varför styrs ett relä ändå genom en transistor?
* Ett program som räknar knapptryck räknar för många, men bara på kortet, aldrig i simulatorn.
  Varför?
* Vad händer om `QUARTER_MS` står kvar på 1 när programmet förs över till kortet?
* Programmet räknar en sekund exakt på cykeln. Varför kan trafikljuset ändå gå fel med en halv
  procent?
* Varför skriver `out PORTB, r16` hela porten på en gång, och varför är det en fördel i ett
  trafikljus?

---

## Referens
* [Appendix A](./appendix/a_control_objects.md): styrobjekt, lysdioder, reläer, studsande knappar
  och kortet.
* [Appendix B](./appendix/b_traffic_light.md): vägarbetsljuset, från flödesplan till program.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* [Exempelprogrammen](./examples/): `roadwork_light.asm` och `press_counter.asm`, kontrollerade i
  simulatorn.
* [labs/lab3/e_final_task.md](../../labs/lab3/e_final_task.md): slutuppgiften.
* [info/microchip_studio.md, avsnitt 5](../../info/microchip_studio.md#5-programmera-ett-arduino-kort-från-microchip-studio):
  att föra över programmet till kortet.
* [ATmega328P datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf),
  för stiftens strömgränser.

---

## Nästa föreläsning
* Repetition av hela kursen, lärandemål för lärandemål.
* Det skriftliga provet: två timmar, utan miniräknare, med referensbladet för AVR-instruktionerna.

---
