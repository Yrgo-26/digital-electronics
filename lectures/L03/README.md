# L03 - Labb 1: Kopplingsnät

## Agenda
* Genomgång av labbstationen: aggregatet, tryckknapparnas kontaktelement och lampan.
* Säkerhet och arbetssätt: rita först, koppla med spänningen frånslagen, förutsäg innan du mäter.
* **Labb 1**: AND, OR, NOT, NAND, NOR, XOR och XNOR med två tryckknappar och en lampa på 24 V.
* Syntes: från en sanningstabell till ett kontaktnät med så få kontakter som möjligt.
* Analys: från ett färdigt kontaktnät till dess uttryck, och vidare till ett mindre nät.
* Felsökning: vad man gör när lampan inte gör som schemat säger.

---

## Föreläsningsupplägg
Passet är till största delen laborationstid, i par vid stationerna:
1. **Genomgång** (ca 30 min). Labbens upplägg och redovisning, säkerhet, och stationens delar:
   hur man hittar ett kontaktelements anslutningar och avgör om det är slutande eller brytande.
   Hur ett strömvägsschema översätts till sladdar, och hur man felsöker med
   [Appendix A](./appendix/a_contact_network_analysis.md) som stöd.
2. **Labb 1** (ca 2 h 15 min). Uppgift 1-8 i
   [laborationshandledningen](../../labs/lab1/README.md), i ordning. Varje uppgift redovisas för
   läraren när den är klar, inte alla på en gång i slutet.
3. **Avslutning** (ca 15 min). Återställ stationen, och en kort genomgång av uppgift 8: vad det
   innebär att två kontaktnät med olika utseende är samma funktion.

Den som blir klar med uppgift 1-8 före passets slut gör den frivilliga uppgift 9, och därefter
övningarna i [Appendix B](./appendix/b_exercises.md).

---

## Före föreläsningen
* Läs [L02 Appendix B](../L02/appendix/b_contact_networks.md) om kontaktnät, om du inte redan har
  gjort det.
* Läs hela [laborationshandledningen](../../labs/lab1/README.md).
* **Gör förberedelseuppgifterna F1-F4** i handledningen. De ska vara klara när passet börjar, och
  läraren tittar på dem innan ni börjar koppla.
* Läs [Appendix A](./appendix/a_contact_network_analysis.md), åtminstone A.1-A.4.

---

## Efter föreläsningen
* Gör klart de uppgifter i Labb 1 som inte hanns med. Resterande uppgifter redovisas i början av
  nästa laborationspass, [L05](../L05/README.md), efter överenskommelse med läraren.
* Arbeta igenom [Appendix B](./appendix/b_exercises.md). Kontrollera dina svar mot
  [Appendix C](./appendix/c_solutions.md) när lösningsförslagen har publicerats.

---

## Det här ska du kunna efteråt
* Avgöra vilka anslutningar på en tryckknapp som är slutande och vilka som är brytande, både med
  hjälp av märkningen och genom mätning.
* Koppla upp ett kontaktnät efter ett strömvägsschema, och kontrollera det mot en sanningstabell.
* Realisera AND, OR, NOT, NAND, NOR, XOR och XNOR med kontakter.
* Ta fram ett kontaktnät ur en sanningstabell, via ett förenklat uttryck.
* Analysera ett kontaktnät: ta fram dess uttryck och sanningstabell, och hitta ett mindre nät med
  samma funktion.
* Felsöka ett kontaktnät systematiskt, med en lampa eller en multimeter.

---

## Frågor att testa dig själv med
* Varför ska ett kontaktnät kopplas med spänningen frånslagen, fast 24 V inte är farligt att röra?
* Hur avgör du med en lampa och ett aggregat om ett kontaktelement är slutande eller brytande?
* Två kontaktnät ser helt olika ut. Hur avgör du om de gör samma sak?
* I uppgift 8 går det att ta bort en kontakt utan att funktionen ändras. Hur kan en kontakt vara
  onödig, när den ju faktiskt påverkar strömmen?
* Lampan lyser aldrig, vad du än trycker på. Var börjar du leta, och varför just där?
* Varför används en stoppknapps brytande kontakt, och inte dess slutande, i en maskins stoppkrets?

---

## Referens
* [Labb 1 - Kopplingsnät](../../labs/lab1/README.md): laborationshandledningen.
* [Appendix A](./appendix/a_contact_network_analysis.md): analys och felsökning av kontaktnät.
* [Appendix B](./appendix/b_exercises.md): övningarna.
* [Appendix C](./appendix/c_solutions.md): lösningsförslagen.
* [L02 Appendix B](../L02/appendix/b_contact_networks.md): kontaktnätens grunder.
* [Laborationer](../../labs/README.md): arbetssätt, säkerhet och redovisning för alla labbar.

---

## Nästa föreläsning
* Karnaughdiagram: ett systematiskt sätt att hitta det minsta nätet, i stället för att leta med
  räknelagarna.
* Syntes av kombinatoriska nät, från specifikation till grindnät.
* NAND- och NOR-nät.
* IC-kretsar ur 74-serien: benplacering, datablad och kopplingsdäck, inför Labb 2.

---
