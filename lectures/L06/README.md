# L06 - Sekvensnät, vippor och mikrodatorns uppbyggnad

## Agenda
* Kretsar som minns: från reläets självhållning till SR-låset av två NOR-grindar.
* D-låset och D-vippan: nivåkänsligt mot flanktriggat, och vad klockan gör.
* Register, räknare och skiftregister, byggda av vippor.
* Mikrodatorns blockschema: CPU, register, ALU, styrenhet, programräknare, minnen, bussar, portar
  och klocka.
* Instruktionscykeln: hämta, avkoda, utför, sexton miljoner gånger i sekunden.
* ATmega328P på ett Arduino Uno-kort: mikrodatorn resten av kursen handlar om.

---

## Föreläsningsupplägg
Tre timmar, i denna ordning:
1. **Något som minns** (20 min). Självhållningen från L02, i
   [A.2](./appendix/a_sequential_logic.md#a2-minne-genom-återkoppling): samma knappläge, två olika
   resultat. Vad skiljer det från allt vi byggt sedan dess?
2. **SR-låset och D-låset i CircuitVerse** (30 min). Två NOR-grindar korskopplas live, och
   övning 2 görs på plats: förutsäg, tryck, jämför. Sedan D-låset, och dess svaghet.
3. **D-vippan och klockan** (20 min). Lås mot vippa i samma tidsdiagram
   ([A.5](./appendix/a_sequential_logic.md#a5-d-vippan-och-klockan)), och vad 16 MHz betyder i
   nanosekunder.
4. **Register, räknare, skiftregister** (20 min). Vippor sida vid sida, vippor som räknar, och
   vippor i kedja. Varje byggsten pekas ut där den kommer att dyka upp i mikrodatorn.
5. **Rast.**
6. **Mikrodatorns blockschema** (50 min). Blockschemat i
   [B.2](./appendix/b_microcomputer.md#b2-blockschemat) byggs upp block för block på tavlan, och
   varje block förklaras med det det är byggt av: ALU:n av heladderare, registren av vippor,
   programräknaren av en räknare. Instruktionscykeln stegas igenom för hand för ett program på
   tre rader.
7. **ATmega328P** (20 min). Ett Arduino Uno-kort i handen: var sitter blocken? Vad betyder 32 kB,
   2 kB och 16 MHz? Förberedelse inför L07: installera Microchip Studio.

---

## Före föreläsningen
* Repetera självhållningen i [L02 Appendix B](../L02/appendix/b_contact_networks.md).
* Läs [Appendix A](./appendix/a_sequential_logic.md), avsnitt A.1-A.5.

---

## Efter föreläsningen
* Läs resten av [Appendix A](./appendix/a_sequential_logic.md) och hela
  [Appendix B](./appendix/b_microcomputer.md). Blockschemat i Appendix B är ett lärandemål i
  kursplanen och kommer på provet.
* Arbeta igenom [Appendix C](./appendix/c_exercises.md), och jämför med
  [Appendix D](./appendix/d_solutions.md) när lösningsförslagen har publicerats.
* **Installera Microchip Studio** enligt [info/microchip_studio.md](../../info/microchip_studio.md),
  avsnitt 1. Installationen tar tid och ska vara klar när L07 börjar.

---

## Det här ska du kunna efteråt
* Förklara skillnaden mellan ett kombinatoriskt nät och ett sekvensnät, och känna igen vilket en
  krets är.
* Förklara hur återkoppling ger minne, med självhållningen och SR-låset som exempel.
* Beskriva skillnaden mellan ett D-lås och en D-vippa, och rita utgången för båda i ett tidsdiagram.
* Räkna ut klockperioden från klockfrekvensen, och tvärtom.
* Förklara vad ett register, en räknare och ett skiftregister är, och vad de är byggda av.
* Rita mikrodatorns blockschema och redogöra för vad varje block gör: CPU, styrenhet, register,
  ALU, statusregister, programräknare, programminne, dataminne, bussar, portar och klocka.
* Beskriva instruktionscykeln och följa ett kort program instruktion för instruktion.
* Redogöra för ATmega328P:s minnen och portar, och vad som skiljer flash, SRAM och EEPROM åt.

---

## Frågor att testa dig själv med
* Varför går det inte att skriva en vanlig sanningstabell för ett SR-lås?
* Vad vinner man på att en vippa bara läser `D` vid den stigande flanken?
* Hur lång är en klockcykel vid 16 MHz?
* En räknare med 8 vippor står på sitt högsta värde och får en klockflank till. Vad händer?
* Vilket block i mikrodatorn räknar, och vilket bestämmer vad som ska räknas?
* Vad är ett hopp i ett program, sett från programräknarens håll?
* Vilket av ATmega328P:s minnen tappar sitt innehåll när strömmen bryts, och varför gör inte de
  andra det?
* Vad är en utport, sett som en byggsten av vippor?

---

## Referens
* [Appendix A](./appendix/a_sequential_logic.md): sekvensnät och vippor.
* [Appendix B](./appendix/b_microcomputer.md): mikrodatorns uppbyggnad och ATmega328P.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* [CircuitVerse](https://circuitverse.org/simulator): simulatorn där låsen och vippan byggs.
* [ATmega328P datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf):
  kapitlet om AVR-kärnan har ett blockschema av samma slag som i Appendix B.

---

## Nästa föreläsning
* ATmega328P på nära håll: de 32 registren, statusregistret och de tre minnena.
* Assemblerspråket: instruktioner, operander, direktiv och etiketter, och hur en rad blir maskinkod.
* Microchip Studio: skapa ett projekt, assemblera, och stega genom programmet i simulatorn.
* **Labb 3** startar.

---
