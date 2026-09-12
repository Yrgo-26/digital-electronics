# Kursinformation - Digitalteknik

## Lärare
Jonas Granath ([jonas.granath12@gmail.com](mailto:jonas.granath12@gmail.com))

---

## Kursupplägg och material
Erik Pihl ([erik.axel.pihl@gmail.com](mailto:erik.axel.pihl@gmail.com))

---

## Kursplan
Digitalteknik, 36 timmar.

### Kursens huvudsakliga innehåll
I kursen behandlas binära koder, grindar, booleska uttryck, logiska kretsar och strömkontakter.
IC-kretsar och mikrodatorprogrammering är centrala delar. I kursen genomförs ett flertal
laborationer.

### Kunskaper
Efter kursen ska den studerande kunna:
* förklara grindar och logiska funktioner
* beskriva binära, hexadecimala och decimala talsystem
* beskriva logisk algebra och förenklingar av booleska uttryck
* redogöra för mikrodatorns uppbyggnad på blockschemanivå

### Färdigheter
Efter kursen ska den studerande kunna:
* omvandla talvärden mellan olika talsystem
* syntetisera digitala kombinatoriska nät med IC-kretsar och kontakter
* använda Karnaughdiagram för analys och minimering av booleska uttryck
* använda assemblerspråk för att programmera en mikrodator
* programmera mikrodatorn till att kontrollera styrobjekt

### Kompetenser
Efter kursen ska den studerande kunna:
* analysera digitala kombinatoriska nät

---

## Förkunskaper
Inga förkunskaper i elektronik eller programmering förutsätts. Det räcker med matematik på
gymnasienivå: potenser, och de fyra räknesätten utan miniräknare.

Kursen går snabbt. Tolv pass om tre timmar rymmer fyra ämnen som var och en skulle kunna fylla en
egen kurs, så varje pass förutsätter att det föregående är läst och att dess övningar är gjorda.

---

## Schema
Tolv pass om tre timmar, måndag, tisdag och onsdag vecka 44-47.

| Vecka | Dag | Datum | Pass | Ämne |
|-------|-----|-------|------|------|
| 44 | Mån | 26/10 | [L01](../lectures/L01/README.md) | Kursintroduktion, talsystem och binära koder |
| 44 | Tis | 27/10 | [L02](../lectures/L02/README.md) | Logiska grindar, boolesk algebra och kontaktnät |
| 44 | Ons | 28/10 | [L03](../lectures/L03/README.md) | **Labb 1** - Kopplingsnät |
| 45 | Mån | 2/11  | [L04](../lectures/L04/README.md) | Karnaughdiagram och IC-kretsar |
| 45 | Tis | 3/11  | [L05](../lectures/L05/README.md) | **Labb 2-1 och 2-2** - Grindnät med IC-kretsar |
| 45 | Ons | 4/11  | [L06](../lectures/L06/README.md) | Sekvensnät, vippor och mikrodatorns uppbyggnad |
| 46 | Mån | 9/11  | [L07](../lectures/L07/README.md) | Mikrodatorn och Microchip Studio - **Labb 3** startar |
| 46 | Tis | 10/11 | [L08](../lectures/L08/README.md) | Aritmetik, logik och flaggor - Labb 3 |
| 46 | Ons | 11/11 | [L09](../lectures/L09/README.md) | Programflöde, loopar och tidsfördröjningar - Labb 3 |
| 47 | Mån | 16/11 | [L10](../lectures/L10/README.md) | Inporten, subrutiner och stacken - Labb 3 |
| 47 | Tis | 17/11 | [L11](../lectures/L11/README.md) | Styrobjekt på riktig hårdvara - Labb 3 slutförs |
| 47 | Ons | 18/11 | [L12](../lectures/L12/README.md) | Repetition och **skriftligt prov** |

### Passens form
* **Föreläsningspass** (L01, L02, L04, L06): genomgång från katedern med exempel som byggs live,
  varvat med övningar som görs på plats och gås igenom i helklass.
* **Laborationspass** (L03, L05): en kort genomgång av utrustning och säkerhet, och därefter
  laboration i par vid stationerna.
* **Mikrodatorpass** (L07-L10): ungefär en och en halv timmes genomgång, med program som skrivs och
  körs live i Microchip Studio, och därefter Labb 3 i par.
* **L11** är till största delen laborationstid: Labb 3 slutförs, och slutuppgiften körs på ett
  riktigt kort.
* **L12** är repetition och det skriftliga provet.

---

## Laborationer
Laborationerna görs i par och redovisas för läraren under passet. Varje laboration har
**förberedelseuppgifter**, som ska vara gjorda före passet: utan dem hinner man inte klart.

| Laboration | Pass | Innehåll | Handledning |
|------------|------|----------|-------------|
| Labb 1 | L03 | Kopplingsnät: logiska funktioner med tryckknappar och en lampa på 24 V | [labs/lab1](../labs/lab1/README.md) |
| Labb 2-1 | L05 | Grindnät med AND-, OR- och inverterarkretsar på kopplingsdäck | [labs/lab2](../labs/lab2/README.md) |
| Labb 2-2 | L05 | Samma nät med enbart NAND- respektive NOR-kretsar | [labs/lab2](../labs/lab2/README.md) |
| Labb 3 | L07-L11 | Mikrodatorn: assemblerprogrammering av ATmega328P, del 1.1-23 och slutuppgift | [labs/lab3](../labs/lab3/README.md) |

Labb 3 består av många små delar som görs i ordning, så långt man hinner. Vilka delar som krävs för
godkänt står under [Examination](#examination).

---

## Lärandemål
Var varje lärandemål undervisas, och var det examineras.

| Lärandemål | Undervisas | Examineras |
|------------|------------|------------|
| Förklara grindar och logiska funktioner | L02, L04 | Labb 1, Labb 2, prov |
| Beskriva binära, hexadecimala och decimala talsystem | L01 | Prov |
| Beskriva logisk algebra och förenklingar av booleska uttryck | L02, L04 | Prov |
| Redogöra för mikrodatorns uppbyggnad på blockschemanivå | L06, L07 | Prov |
| Omvandla talvärden mellan olika talsystem | L01, L07, L08 | Prov, Labb 3 |
| Syntetisera digitala kombinatoriska nät med IC-kretsar och kontakter | L02-L05 | Labb 1, Labb 2 |
| Använda Karnaughdiagram för analys och minimering av booleska uttryck | L04 | Labb 2, prov |
| Använda assemblerspråk för att programmera en mikrodator | L07-L10 | Labb 3, prov |
| Programmera mikrodatorn till att kontrollera styrobjekt | L08, L10, L11 | Labb 3 |
| Analysera digitala kombinatoriska nät | L02-L05 | Labb 1, Labb 2, prov |

Sekvensnät och vippor (L06) ingår inte i kursplanens lärandemål. De tas med för att mikrodatorn
annars blir en svart låda: register, programräknare och minne är vippor, och det är den kopplingen
som gör blockschemat begripligt. På provet förekommer vippor bara som en del av mikrodatorns
uppbyggnad.

---

## Examination

### Upplägg
* **Labb 1** och **Labb 2** bedöms med **U/G**.
* **Labb 3** bedöms med **U/G/VG**.
* Ett **skriftligt prov** i [L12](../lectures/L12/README.md), två timmar, bedöms med **U/G/VG**.

### Laborationerna
En laboration är godkänd när samtliga uppgifter för godkänt är redovisade för läraren, och båda i
paret kan förklara lösningen. Redovisning sker under passen.

| Laboration | Krav för G | Krav för VG |
|------------|------------|-------------|
| Labb 1 | Uppgift 1-8 | - |
| Labb 2 | Labb 2-1 uppgift 1-4 och Labb 2-2 uppgift 1-3 | - |
| Labb 3 | Del 1.1-12, 14-16, 21 och slutuppgiften del A | Samtliga delar 1.1-23 och slutuppgiften del B |

### Det skriftliga provet
* Två timmar, individuellt, utan miniräknare. Ett referensblad med AVR-instruktionerna delas ut
  tillsammans med provet.
* Provet omfattar talsystem, grindar och boolesk algebra, Karnaughdiagram, analys av
  kombinatoriska nät, mikrodatorns uppbyggnad och läsning och skrivning av enkla assemblerprogram.
* 40 poäng totalt: **G** kräver 20 poäng, **VG** kräver 30 poäng.
* Ett [övningsprov](../exam/README.md) med lösningsförslag finns att träna på.

### Slutbetyg

| Betyg | Krav |
|-------|------|
| G | Samtliga laborationer godkända och godkänt skriftligt prov. |
| VG | Samtliga laborationer godkända, VG på Labb 3 och VG på det skriftliga provet. |

För godkänt betyg krävs att alla kursens lärandemål är uppnådda. Omprov och restlaborationer
genomförs enligt Yrgos rutiner.

---

## Kursmaterial

### Litteratur
Kursmaterialet finns samlat i det här repot. Varje pass har ett `README.md` och en katalog
`appendix/`:
* de första appendixen är **kursmaterialet**, med genomarbetade exempel;
* det näst sista är **övningarna**;
* det sista är **lösningsförslagen**, som publiceras efter passet.

Laborationshandledningarna finns under [labs/](../labs/README.md). Allt det här finns också
satt som en bok, med lösningsförslagen till övningarna som inte är program; se
[book/](../book/README.md).

Två externa dokument används som referens i mikrodatordelen:
* [ATmega328P datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
* [AVR Instruction Set Manual](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)

### Hjälpmedel
Inga miniräknare på provet. Under kursen går det bra att kontrollera omvandlingar med
miniräknaren i Windows, i läget **Programmerare**, men räkna alltid för hand först.

---

### Programvara
* **[CircuitVerse](https://circuitverse.org/simulator)** - gratis, webbläsarbaserad logiksimulator,
  där grindnät byggs och testas innan de kopplas upp. Inget att installera.
* **[Microchip Studio 7](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio)** -
  gratis utvecklingsmiljö för AVR, där programmen i Labb 3 skrivs, assembleras och simuleras.
  Installeras före [L07](../lectures/L07/README.md) enligt
  [microchip_studio.md](./microchip_studio.md). Microchip Studio finns bara för Windows; den som har
  en Mac använder skolans datorer eller en virtuell Windowsmaskin.
* **[Arduino IDE](https://www.arduino.cc/en/software)** - används en enda gång, i
  [L11](../lectures/L11/README.md), för att ta fram kommandot som programmerar kortet. Se
  [microchip_studio.md](./microchip_studio.md#5-programmera-ett-arduino-kort-från-microchip-studio).

---

### Hårdvara
Utrustningen finns på skolan.

**Labb 1**, 14 stationer, var och en med:
* ett 24 V DC-aggregat;
* två 4-poliga tryckknappar med både slutande (NO) och brytande (NC) kontakter;
* en glödlampa för 24 V;
* kopplingssladdar;
* en multimeter, för felsökning ([L03 Appendix A](../lectures/L03/appendix/a_contact_network_analysis.md)).

**Labb 2**, 14 stationer, var och en med:
* ett kopplingsdäck med kringutrustning: 5 V-matning, strömbrytare eller knappar för ingångarna och
  lysdioder för utgångarna;
* IC-kretsar: 74HC08 (AND), 74HC32 (OR) och 74HC04 (inverterare) till Labb 2-1, 74HC00 (NAND) och
  74HC02 (NOR) till Labb 2-2;
* kopplingstråd, och en multimeter.

**Labb 3**, per par:
* ett Arduino Uno-kort (ATmega328P) med USB-kabel;
* ett kopplingsdäck, tre lysdioder (röd, gul, grön) med förkopplingsmotstånd på 220-330 Ω, en
  tryckknapp och kopplingstråd.

Det mesta av Labb 3 görs i simulatorn i Microchip Studio. Kortet behövs först i
[L11](../lectures/L11/README.md).

---
