# Föreläsningsmaterial

Kursen består av tolv pass om tre timmar. De fem första handlar om kombinatoriska nät, det sjätte
om vippor och om hur en mikrodator är uppbyggd, de fem därpå om mikrodatorn och
assemblerprogrammering, och det tolfte är repetition och skriftligt prov.

---

## Del 1 - Digitala kombinatoriska nät
* [L01](./L01/README.md): Talsystem och binära koder - positionssystem, omvandling mellan
  decimalt, binärt och hexadecimalt, binär addition, BCD, Graykod och ASCII.
* [L02](./L02/README.md): Logiska grindar, boolesk algebra och kontaktnät - grindar och
  sanningstabeller, räknelagarna och De Morgan, och samma logik byggd med kontakter.
* [L03](./L03/README.md): **Labb 1** - Kopplingsnät med tryckknappar och en lampa på 24 V.
* [L04](./L04/README.md): Karnaughdiagram och IC-kretsar - minimering, syntes av kombinatoriska
  nät, NAND och NOR, och 74-seriens kretsar på kopplingsdäck.
* [L05](./L05/README.md): **Labb 2-1 och 2-2** - Grindnät med IC-kretsar.

---

## Del 2 - Från vippa till mikrodator
* [L06](./L06/README.md): Sekvensnät, vippor och mikrodatorns uppbyggnad - SR-låset, D-vippan,
  register och räknare, och mikrodatorns blockschema.

---

## Del 3 - Mikrodatorn och assemblerprogrammering
* [L07](./L07/README.md): Mikrodatorn och Microchip Studio - ATmega328P, register och minnen,
  assemblerspråkets byggstenar, och det första programmet i simulatorn. **Labb 3** startar.
* [L08](./L08/README.md): Aritmetik, logik och flaggor - addition och subtraktion, tvåkomplement,
  flaggorna i SREG, logiska operationer, skift och rotation, och utporten.
* [L09](./L09/README.md): Programflöde, loopar och tidsfördröjningar - flödesplaner, jämförelser
  och villkorliga hopp, loopar, och fördröjningar beräknade från klockcykler.
* [L10](./L10/README.md): Inporten, subrutiner och stacken - ASCII, 16-bitarstal, att läsa
  knappar, subrutiner och stacken som lagringsplats.
* [L11](./L11/README.md): Styrobjekt på riktig hårdvara - ett trafikljus, från flödesplan till
  program på ett Arduino Uno-kort. **Labb 3** slutförs.

---

## Examination
* [L12](./L12/README.md): Repetition och **skriftligt prov**.

---

## Hur ett pass är upplagt
Varje pass har samma form:

```text
lectures/LNN/
├── README.md       Vad passet tar upp, vad du läser före och gör efter.
└── appendix/       Kursmaterialet, övningarna och lösningsförslagen.
```

**Appendixen är kursmaterialet.** README-filen är kartan; appendixen är terrängen. Läs dem i
ordning.

**Appendixens bokstäver följer en regel.** Teoriappendixen kommer först, så många bokstäver som
materialet behöver. Därefter alltid:
* det **näst sista** appendixet är **övningarna**, och
* det **sista** appendixet är **lösningsförslagen**.

Så du hittar alltid övningarna och svaren genom att räkna bakifrån. Lösningsförslagen publiceras
efter passet: fram till dess är övningarna det sista appendixet.

---

## Övningarnas sorter
Varje övning är märkt med sin sort:

| Sort | Vad den ber dig göra |
|------|----------------------|
| **Förståelse** | Förklara något från appendixet med egna ord. Inga verktyg. |
| **Räkna för hand** | Räkna ut något på papper: en omvandling, en förenkling, en cykelräkning. |
| **Konstruktion** | Ta fram en lösning: ett grindnät, ett kontaktnät, en flödesplan. |
| **Program** | Skriv assembler, och kör det i simulatorn. |
| **Kontroll** | En per pass. Se nedan. |

**Kontrolluppgiften är kursens signaturövning.** Du räknar ut ett svar för hand, du kontrollerar det
med ett verktyg, i CircuitVerse, i simulatorn eller på labbstationen, och du förklarar varför de två
stämmer, eller varför de inte gör det. Att förutsäga ett beteende och sedan kontrollera det är den
färdighet resten av kursen vilar på.

---
