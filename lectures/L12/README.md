# L12 - Repetition och skriftligt prov

## Agenda
* Repetition av kursen, lärandemål för lärandemål, med korta frågor i helklass.
* Frågestund: det som fortfarande är oklart.
* **Skriftligt prov**, två timmar, individuellt och utan miniräknare.

---

## Föreläsningsupplägg
Passet har två delar med en paus emellan:
1. **Repetition** (40 min). Kursens lärandemål gås igenom i den ordning
   [Appendix A](./appendix/a_review.md) har dem: talsystem och koder, grindar och boolesk algebra,
   Karnaughdiagram, mikrodatorns uppbyggnad och assemblerprogrammering. Till varje område hör en
   eller två frågor från [Appendix B](./appendix/b_exercises.md), som görs på plats och gås igenom.
2. **Frågestund** (10 min). Frågor om det som fortfarande är oklart, och om provets form.
3. **Paus** (10 min).
4. **Skriftligt prov** (2 h). Provet delas ut tillsammans med
   [referensbladet](../../info/avr_instructions.md) för AVR-instruktionerna. Inga andra hjälpmedel
   än penna, suddgummi och linjal.

Provets form, poäng och betygsgränser står i [exam/README.md](../../exam/README.md).

---

## Före föreläsningen
* Gör [övningsprovet](../../exam/practice_exam.md) under två timmar, utan miniräknare, och rätta det
  mot [lösningsförslagen](../../exam/practice_exam_solutions.md).
* Gå igenom [Appendix A](./appendix/a_review.md) och bocka av listorna "Kan du ...?". Läs om det du
  inte kan.
* Ta med frågor till frågestunden. En fråga som ställs före provet är värd mer än en som ställs
  efter.

---

## Efter föreläsningen
* Provet rättas och återlämnas tillsammans med lösningsförslaget.
* Laborationer som inte är redovisade redovisas enligt Yrgos rutiner för restlaborationer; se
  [kursinformationen](../../info/README.md#examination).

---

## Det här ska du kunna efteråt
Kursplanens lärandemål. Efter kursen ska du kunna:
* förklara grindar och logiska funktioner;
* beskriva binära, hexadecimala och decimala talsystem, och omvandla talvärden mellan dem;
* beskriva logisk algebra och förenklingar av booleska uttryck;
* redogöra för mikrodatorns uppbyggnad på blockschemanivå;
* syntetisera digitala kombinatoriska nät med IC-kretsar och kontakter;
* använda Karnaughdiagram för analys och minimering av booleska uttryck;
* använda assemblerspråk för att programmera en mikrodator, och programmera den att styra
  styrobjekt;
* analysera digitala kombinatoriska nät.

---

## Frågor att testa dig själv med
* Vilket tal är `0xB6` decimalt, och hur ser det ut binärt?
* Vad säger De Morgans lagar, och varför kan varje logisk funktion byggas av enbart NAND-grindar?
* Varför står raderna i ett Karnaughdiagram i ordningen 00, 01, 11, 10?
* Vad gör programräknaren, och vad händer med den vid ett `rcall`?
* Efter `ldi r16, 200` och `subi r16, 201`: vad är `r16`, och vad är `C`?
* En loop med `dec` och `brne` går 100 varv. Hur många cykler tar den, och hur lång tid är det vid
  16 MHz?
* Varför läses en nedtryckt knapp som noll, och vad behövs för att den ska läsas som något alls när
  den är släppt?

---

## Referens
* [Appendix A](./appendix/a_review.md): repetitionen, ordnad efter lärandemål.
* [Appendix B](./appendix/b_exercises.md): repetitionsuppgifter i provets stil.
* [Appendix C](./appendix/c_solutions.md): lösningsförslagen.
* [exam/README.md](../../exam/README.md): provets form, poäng och bedömning.
* [Övningsprovet](../../exam/practice_exam.md), med
  [lösningsförslag](../../exam/practice_exam_solutions.md).
* [Referensbladet](../../info/avr_instructions.md), som delas ut på provet.

---

## Efter kursen
Kursen har gått från ettor och nollor till en mikrodator som styr ett trafikljus. Varje steg på
vägen finns kvar i det du har byggt: grindarna finns i ALU:n, vipporna i registren och
programräknaren, kontaktnätens logik i programmets villkorliga hopp.

Vill du vidare finns några naturliga nästa steg:
* **PLC-programmering.** Kontaktnät och stegdiagram från L02, med samma idé om ingångar, beslut och
  utgångar som i L11, i den form industrin använder.
* **C för mikrokontroller.** Samma ATmega328P och samma register, `DDRB`, `PORTB` och `PIND`, men i
  ett språk där kompilatorn skriver assemblern åt dig. Den som har skrivit assembler vet vad
  kompilatorn gör.
* **Programmerbar logik.** Grindnät och vippor beskrivna i ett hårdvarubeskrivande språk, och körda
  på en FPGA.

Spara projekten från Labb 3. Ett program som fungerar är den bästa referensen när nästa program ska
skrivas.

---
