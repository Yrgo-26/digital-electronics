# L05 - Labb 2: Grindnät med IC-kretsar

## Agenda
* Kort genomgång: kopplingsdäcket, kretsens riktning, matningen och redovisningen.
* **Labb 2-1**: grindnät med AND-, OR- och inverterarkretsar, från minimerat uttryck till fungerande
  krets.
* **Labb 2-2**: samma sorts nät med enbart NAND, och en titt på NOR.
* Felsökning: förutsäg, mät, jämför, i stället för att flytta sladdar på måfå.

---

## Föreläsningsupplägg
Tre timmar, i denna ordning:
1. **Genomgång** (20 min). Stationen och dess strömbrytare och lysdioder, kretsarna och deras
   riktning, matningen först, kopplingslistan, och säkerheten: en krets som blir varm är felkopplad.
   Arbetsgången för felsökning i [Appendix A](./appendix/a_troubleshooting.md), visad på ett nät
   med ett avsiktligt fel.
2. **Labb 2-1** (75 min), i par. Uppgift 1-4 i [labbhandledningen](../../labs/lab2/README.md).
   Redovisa varje uppgift när den är klar.
3. **Rast.**
4. **Labb 2-2** (65 min), i par. Uppgift 1-3, och uppgift 4 för den som hinner.
5. **Avslutning** (10 min). Sista redovisningarna, och vad nästa pass handlar om: kretsar som kan
   minnas.

Den som blir klar tidigt gör uppgift 4 i Labb 2-2, eller övningarna i
[Appendix B](./appendix/b_exercises.md).

---

## Före föreläsningen
* Gör **alla förberedelser** F1-F5 i [labbhandledningen](../../labs/lab2/README.md#förberedelser):
  sanningstabeller, Karnaughdiagram, NAND-nät, simulering i CircuitVerse och en kopplingslista för
  varje uppgift. De är en del av redovisningen, och utan dem hinner du inte klart.
* Repetera [L04 Appendix B](../L04/appendix/b_integrated_circuits.md): benplaceringen, logiknivåerna
  och kopplingsdäcket.
* Läs [Appendix A](./appendix/a_troubleshooting.md), om felsökning.

---

## Efter föreläsningen
* Arbeta igenom [Appendix B](./appendix/b_exercises.md), och jämför med
  [Appendix C](./appendix/c_solutions.md) när lösningsförslagen har publicerats. Kontrolluppgiften,
  övning 10, bygger på mätningen i Labb 2-1 uppgift 1.
* Om någon uppgift inte hann redovisas: tala med läraren om när den kan göras klart.

---

## Det här ska du kunna efteråt
* Koppla upp ett grindnät med 74HC-kretsar på ett kopplingsdäck, med matning, ingångar och utgång,
  enligt en grindtilldelning och en kopplingslista.
* Verifiera ett nät mot dess sanningstabell, rad för rad, med förväntat och uppmätt värde.
* Bygga NOT, AND och OR av enbart NAND-grindar, och bygga ett nät med enbart NAND.
* Mäta en logisk nivå med en multimeter och avgöra om den är 0, 1 eller ogiltig.
* Felsöka ett nät systematiskt: matningen först, sedan signalen grind för grind, och läsa ut ur
  sanningstabellen var felet troligen sitter.

---

## Frågor att testa dig själv med
* Varför ska matningen mätas först, även när nätet delvis verkar fungera?
* En utgång visar 2,4 V. Vad kan det betyda?
* Ett nät är fel på exakt de rader där en viss AND-term ska göra utgången till 1. Var mäter du
  först?
* Varför kan en 74HC32 sitta där det ska vara en 74HC08 utan att du märker det på alla rader?
* Varför är 74HC02 den krets flest kopplar fel, och vad händer om den kopplas som en 74HC00?
* `X = AB + C` med enbart NAND har en grind mer än med AND och OR. Vad vinner du ändå?

---

## Referens
* [Labb 2](../../labs/lab2/README.md): labbhandledningen.
* [Appendix A](./appendix/a_troubleshooting.md): felsökning av grindnät.
* [Appendix B](./appendix/b_exercises.md): övningarna.
* [Appendix C](./appendix/c_solutions.md): lösningsförslagen.
* [L04 Appendix A](../L04/appendix/a_karnaugh_maps.md): Karnaughdiagram och NAND- och NOR-nät.
* [L04 Appendix B](../L04/appendix/b_integrated_circuits.md): IC-kretsar, benplaceringar och
  kopplingsdäcket.

---

## Nästa föreläsning
* Sekvensnät: kretsar som minns, från reläets självhållning till SR-låset.
* D-låset och D-vippan, klockan och flanken.
* Register, räknare och skiftregister, byggda av vippor.
* Mikrodatorns uppbyggnad på blockschemanivå, och hur varje block går tillbaka till grindar och
  vippor.

---
