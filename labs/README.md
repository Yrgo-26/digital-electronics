# Laborationer

Kursen har tre laborationer. Labb 1 och Labb 2 görs på varsitt pass; Labb 3 löper över de fem
mikrodatorpassen.

| Laboration | Pass | Innehåll |
|------------|------|----------|
| [Labb 1 - Kopplingsnät](./lab1/README.md) | L03 | Logiska funktioner med tryckknappar och en lampa på 24 V. |
| [Labb 2 - Grindnät med IC-kretsar](./lab2/README.md) | L05 | 2-1: AND, OR och inverterare. 2-2: enbart NAND respektive NOR. |
| [Labb 3 - Mikrodatorn](./lab3/README.md) | L07-L11 | Assemblerprogrammering av ATmega328P, i simulatorn och på ett Arduino Uno-kort. |

---

## Så går en laboration till
* **Förbered dig hemma.** Varje handledning börjar med förberedelseuppgifter: sanningstabeller,
  uttryck och kopplingsscheman som ska vara klara när passet börjar. Utan dem hinner man inte klart,
  och det är den enskilt vanligaste orsaken till att en laboration inte blir godkänd på passet.
* **Arbeta i par**, och byt roll: den ena kopplar eller skriver, den andra kontrollerar mot
  schemat. Båda ska kunna förklara lösningen.
* **Förutsäg, sedan kontrollera.** Skriv ned vad du förväntar dig innan du slår på strömmen eller
  kör programmet. En avvikelse mellan förutsägelse och resultat är information: den säger att
  schemat, kopplingen eller programmet har ett fel, och att du nu vet var du ska leta.
* **Redovisa för läraren** varje uppgift som är markerad med *Redovisa*. Läraren prickar av den i
  redovisningslistan.

---

## Säkerhet
* Koppla **alltid** med spänningen frånslagen, och slå på först när kopplingen är kontrollerad.
* 24 V DC är ingen farlig spänning att beröra, men en kortslutning kan ge stora strömmar, heta
  sladdar och en bränd säkring i aggregatet. En glödlampa blir dessutom varm.
* Koppla aldrig 24 V till kopplingsdäcket eller till Arduino-kortet. IC-kretsarna och
  mikrodatorn ska matas med 5 V, och 24 V förstör dem på ett ögonblick.
* IC-kretsar vänds lätt fel. En krets som blir varm är felvänd eller felkopplad: bryt matningen
  direkt.

---

## Redovisning och bedömning
Vilka uppgifter som krävs för godkänt, och för VG på Labb 3, står i
[kursinformationen](../info/README.md#examination).

---
