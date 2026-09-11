# L04 - Karnaughdiagram och IC-kretsar

## Agenda
* Varför ett korrekt nät inte räcker: det ska också vara litet.
* Karnaughdiagram för två, tre och fyra ingångar: Graykoden, grupperna och avläsningen.
* Kanter, hörn och don't care, de tre ställen där minimering oftast går fel.
* Syntes av ett kombinatoriskt nät: från specifikation till minimerat grindnät.
* Nät med enbart NAND eller enbart NOR, och varför de sparar kretsar.
* IC-kretsar ur 74-serien: kapsel, benplacering, datablad och logiknivåer.
* Kopplingsdäcket, lysdioder och ingångar som aldrig får flyta.
* Förberedelse för Labb 2 i nästa pass.

---

## Föreläsningsupplägg
Tre timmar, i denna ordning:
1. **Ett korrekt nät som är för stort** (15 min). Sanningstabellen i
   [A.1](./appendix/a_karnaugh_maps.md#a1-varför-minimera), läst av på L02:s sätt: nio grindar.
   Samma funktion med två. Hur hittar man de två utan att gissa?
2. **Karnaughdiagrammet, live** (45 min). Diagrammets form och Graykoden, sedan exemplet från A.3
   steg för steg: fylla i, gruppera, läsa av, kontrollera. Därefter kanterna och hörnen (A.5) och
   don't care (A.6), med övningarna 2-4 och 7 gjorda på plats och genomgångna i helklass.
3. **Från specifikation till nät** (30 min). Tankens larm, majoritetskretsen i A.7, hela vägen till
   ett grindnät i CircuitVerse. Sedan heladderaren (A.8), där diagrammet inte kan förenkla något,
   och vad det betyder.
4. **Rast.**
5. **NAND och NOR** (20 min). Samma nät med enbart NAND (A.9): en grind mer, en krets mindre.
6. **IC-kretsar på kopplingsdäck** (40 min). En 74HC08 och en 74HC32 i handen: hacket, ben 1, VCC
   och GND, benplaceringen och databladet. Kopplingsdäcket, en lysdiod med motstånd och en ingång
   med pull-down. `X = AB + C` kopplas upp från katedern med hjälp av en grindtilldelning och en
   kopplingslista (B.7), och får fel med flit: en flytande ingång.
7. **Förberedelse för Labb 2** (10 min). Genomgång av labbhandledningen och vad som ska vara klart
   före nästa pass.

---

## Före föreläsningen
* Repetera [L02 Appendix A](../L02/appendix/a_logic_gates.md): räknelagarna, De Morgans lagar och
  hur ett uttryck läses av ur en sanningstabell.
* Läs [Appendix A](./appendix/a_karnaugh_maps.md), avsnitt A.1-A.4.

---

## Efter föreläsningen
* Läs resten av [Appendix A](./appendix/a_karnaugh_maps.md) och hela
  [Appendix B](./appendix/b_integrated_circuits.md).
* Arbeta igenom [Appendix C](./appendix/c_exercises.md), och jämför med
  [Appendix D](./appendix/d_solutions.md) när lösningsförslagen har publicerats.
* Gör förberedelserna till [Labb 2](../../labs/lab2/README.md). De ska vara klara när L05 börjar.

---

## Det här ska du kunna efteråt
* Rita ett Karnaughdiagram för en funktion med två, tre eller fyra ingångar, med rubrikerna i
  Graykod.
* Ringa in grupper av ettor efter reglerna, också över kanter och i hörn, och läsa av ett minimerat
  uttryck på summa av produkter-form.
* Använda don't care för kombinationer som aldrig förekommer.
* Syntetisera ett kombinatoriskt nät från en beskrivning i ord: sanningstabell, Karnaughdiagram,
  minimerat uttryck, grindnät, kontroll.
* Göra om ett nät till enbart NAND-grindar eller enbart NOR-grindar.
* Hitta ben 1, VCC, GND och varje grinds ben på en 74HC-krets, med hjälp av databladet.
* Räkna ut ett förkopplingsmotstånd för en lysdiod, och förklara varför en ingång aldrig får
  lämnas flytande.
* Planera en uppkoppling med en grindtilldelning och en kopplingslista.

---

## Frågor att testa dig själv med
* Varför måste rubrikerna i ett Karnaughdiagram stå i Graykod? Vad går fel med vanlig binär
  ordning?
* En grupp om fyra rutor i ett diagram med fyra ingångar: hur många ingångar blir kvar i termen?
* Ett diagram där ettorna bildar ett schackmönster går inte att förenkla. Vilken grind beräknar
  en sådan funktion?
* När får en X-ruta ingå i en grupp, och måste den täckas?
* Ett NAND-nät har ofta fler grindar än AND-OR-nätet för samma funktion. Varför kan det ändå vara
  billigare att bygga?
* Vilket ben är VCC och vilket är GND på en 74HC08? Och på en 74HC02? Vad skiljer 74HC02 från de
  andra?
* Varför är en okopplad ingång på en HC-krets ett fel, även om kretsen verkar fungera?

---

## Referens
* [Appendix A](./appendix/a_karnaugh_maps.md): Karnaughdiagram, syntes och NAND- och NOR-nät.
* [Appendix B](./appendix/b_integrated_circuits.md): IC-kretsar, datablad, kopplingsdäck och
  planering av en uppkoppling.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* [Labb 2](../../labs/lab2/README.md): laborationen i nästa pass.
* [CircuitVerse](https://circuitverse.org/simulator): simulatorn där varje nät byggs och testas
  innan det kopplas upp.
* Datablad för kretsarna, till exempel från Texas Instruments:
  [SN74HC00](https://www.ti.com/lit/ds/symlink/sn74hc00.pdf),
  [SN74HC02](https://www.ti.com/lit/ds/symlink/sn74hc02.pdf),
  [SN74HC04](https://www.ti.com/lit/ds/symlink/sn74hc04.pdf),
  [SN74HC08](https://www.ti.com/lit/ds/symlink/sn74hc08.pdf),
  [SN74HC32](https://www.ti.com/lit/ds/symlink/sn74hc32.pdf).

---

## Nästa föreläsning
* **Labb 2-1**: grindnät med AND-, OR- och inverterarkretsar på kopplingsdäck.
* **Labb 2-2**: samma nät med enbart NAND och enbart NOR.
* Felsökning av ett grindnät som inte gör vad det ska, systematiskt i stället för på måfå.

---
