# L02 - Logiska grindar, boolesk algebra och kontaktnät

## Agenda
* De logiska grindarna NOT, AND, OR, NAND, NOR, XOR och XNOR, deras sanningstabeller och symboler.
* Boolesk algebra: notationen, räknelagarna och De Morgans lagar.
* Från sanningstabell till uttryck, och från uttryck till grindnät.
* Analys: från ett färdigt grindnät till dess sanningstabell.
* CircuitVerse: att bygga och simulera ett grindnät i webbläsaren.
* Kontaktnät: samma logik byggd med tryckknappar, en lampa och 24 V, inför Labb 1.
* Reläet, och en krets som minns: självhållningen.

---

## Föreläsningsupplägg
Passet byggs kring ett enda exempel, bromsassistenten, som först blir ett grindnät och sedan ett
kontaktnät. I den här ordningen:
1. **Grindarna** (ca 25 min). Sanningstabell, symbol och uttryck för var och en, i båda
   symbolstandarderna.
2. **Boolesk algebra** (ca 30 min). Notationen, räknelagarna och De Morgan, med varje lag
   kontrollerad mot en sanningstabell. Övning 3 och 4 görs på plats.
3. **Bromsassistenten** (ca 35 min). Från ett krav i tre meningar till en sanningstabell, ett
   förenklat uttryck och ett grindnät med fyra grindar, byggt och simulerat live i
   [CircuitVerse](https://circuitverse.org/simulator).
4. **Analys** (ca 15 min). Ett grindnät du inte har byggt själv, läst tillbaka till en
   sanningstabell med hjälp av mellansignaler.
5. **Kontaktnät** (ca 45 min). Slutande och brytande kontakter, serie som AND och parallell som
   OR. Bromsassistenten igen, nu som kontaktnät. Reläet och självhållningen, och en glimt av hur
   samma kopplingar ritas i en PLC.
6. **Inför Labb 1** (ca 15 min). Vad förberedelseuppgifterna går ut på, och hur labbstationen ser
   ut.

---

## Före föreläsningen
* Läs [Appendix A](./appendix/a_logic_gates.md), åtminstone A.1-A.6.
* Läs kravet på bromsassistenten i
  [A.10](./appendix/a_logic_gates.md#a10-föreläsningens-krets-bromsassistenten) och försök ta fram
  ett uttryck för den själv, innan du läser härledningen. Ta med ditt svar till passet.
* Öppna [CircuitVerse](https://circuitverse.org/simulator) och kontrollera att simulatorn startar i
  din webbläsare. Inget behöver installeras.

---

## Efter föreläsningen
* Läs [Appendix B](./appendix/b_contact_networks.md) om kontaktnät. Det är förberedelsen inför
  [Labb 1](../../labs/lab1/README.md) i nästa pass.
* Arbeta igenom [Appendix C](./appendix/c_exercises.md). Kontrollera dina svar mot
  [Appendix D](./appendix/d_solutions.md) när lösningsförslagen har publicerats.
* Gör förberedelseuppgifterna i [Labb 1](../../labs/lab1/README.md#förberedelser). Utan dem hinner
  du inte klart på labbpasset.

---

## Det här ska du kunna efteråt
* Rita symbolen för varje grundgrind, i ANSI- och i IEC-form, och ange dess sanningstabell och
  uttryck.
* Skriva ett booleskt uttryck med kursens notation, och förenkla det med räknelagarna och De
  Morgans lagar.
* Ta fram ett uttryck i SP-form ur en sanningstabell, och realisera det som ett grindnät.
* Analysera ett grindnät: ta fram dess uttryck och sanningstabell med hjälp av mellansignaler.
* Bygga och simulera ett grindnät i CircuitVerse, och kontrollera det mot en sanningstabell.
* Översätta mellan ett uttryck och ett kontaktnät: serie är AND, parallell är OR, brytande kontakt
  är NOT.
* Förklara hur ett relä med självhållning kan minnas att det har startats.

---

## Frågor att testa dig själv med
* Vilken grind ger `1` bara när alla ingångar är `1`? Vilken ger `0` bara när alla ingångar är
  `0`?
* Varför är `A + A'B` lika med `A + B`? Visa det både med en sanningstabell och med ord.
* Hur flyttar De Morgan en inversion genom en grind, och varför betyder det att en NAND-grind kan
  bygga vilken funktion som helst?
* I bromsassistenten läggs förarens pedal in med OR sist, i stället för att gå genom
  felhanteringslogiken. Vad går sönder om du kopplar den tvärtom?
* Varför behöver en XOR-funktion med tryckknappar både den slutande och den brytande kontakten i
  varje knapp?
* Vad händer i självhållningskretsen om stoppknappen av misstag kopplas med sin slutande kontakt i
  stället för sin brytande?

---

## Referens
* [Appendix A](./appendix/a_logic_gates.md): logiska grindar och boolesk algebra.
* [Appendix B](./appendix/b_contact_networks.md): kontaktnät.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* [CircuitVerse](https://circuitverse.org/simulator): den webbläsarbaserade simulatorn som används
  för att bygga och testa grindnät i L02-L06.
* [Labb 1](../../labs/lab1/README.md): laborationshandledningen till nästa pass.

---

## Nästa föreläsning
* **Labb 1 - Kopplingsnät**: logiska funktioner byggda med två tryckknappar och en lampa på 24 V.
* Att analysera ett kontaktnät man inte har ritat själv, och att hitta felet när lampan inte gör
  som den ska.
* Förberedelseuppgifterna i labbhandledningen ska vara klara när passet börjar.

---
