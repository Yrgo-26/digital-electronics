# Digitalteknik - AI26
Kursrepo för **Digitalteknik** med klassen AI26, ht26: tolv pass om tre timmar, vecka 44-47.

Kursen tar dig från ettor och nollor till en mikrodator som styr något i verkligheten. Först
talsystem, logiska grindar och boolesk algebra, byggda både med strömkontakter på 24 V och med
IC-kretsar på kopplingsdäck. Sedan vippan, den byggsten som ger en krets minne, och därifrån
mikrodatorn: en ATmega328P som programmeras i assembler, först i simulatorn och till sist på ett
riktigt kort där den styr lysdioder och läser av en knapp.

---

## Om kursen

### Del 1: Digitala kombinatoriska nät (L01-L05)
Binära, hexadecimala och decimala tal och omvandling mellan dem. Logiska grindar, sanningstabeller
och boolesk algebra, och hur ett uttryck förenklas, algebraiskt och med Karnaughdiagram. Samma logik
realiseras på två sätt: med tryckknappar och en lampa på 24 V i **Labb 1**, och med IC-kretsar ur
74-serien på kopplingsdäck i **Labb 2**.

### Del 2: Från vippa till mikrodator (L06)
Sekvensnät och vippor: hur en krets kan minnas. Register, räknare och minne är vippor, och
mikrodatorn är register och minne kring en aritmetisk enhet, byggd av de grindar del 1 handlade om.
Passet slutar i mikrodatorns blockschema.

### Del 3: Mikrodatorn och assemblerprogrammering (L07-L11)
ATmega328P programmeras i assembler i Microchip Studio: talformat, aritmetik och flaggor, logiska
operationer, villkorliga hopp, loopar och tidsfördröjningar, in- och utportar, subrutiner och
stacken. **Labb 3** löper genom alla fem passen, och avslutas med ett styrobjekt, ett trafikljus,
som körs på ett Arduino Uno-kort.

### Examination (L12)
Laborationerna redovisas under passen, och kursen avslutas med ett skriftligt prov. Se
[kursinformationen](./info/README.md#examination).

---

## Efter kursen
Du ska kunna:
* Förklara grindar och logiska funktioner, och beskriva logisk algebra och förenkling av booleska
  uttryck.
* Beskriva det binära, det hexadecimala och det decimala talsystemet, och omvandla tal mellan dem.
* Syntetisera ett digitalt kombinatoriskt nät, med IC-kretsar och med kontakter, och använda
  Karnaughdiagram för att analysera och minimera det.
* Analysera ett digitalt kombinatoriskt nät: från krets till uttryck till sanningstabell.
* Redogöra för mikrodatorns uppbyggnad på blockschemanivå.
* Använda assemblerspråk för att programmera en mikrodator, och programmera den att styra ett
  styrobjekt.

Kopplingen mellan kursplanens lärandemål och kursens pass och laborationer finns i
[kursinformationen](./info/README.md#lärandemål).

---

## Struktur

```text
info/        Kursinformation: kursplan, schema, examination, programvara och hårdvara.
lectures/    Per pass: README, och appendix/ med teori, övningar och lösningsförslag.
labs/        Laborationshandledningarna till Labb 1, Labb 2 och Labb 3.
exam/        Information om det skriftliga provet, och ett övningsprov.
diagrams/    Python-källor till kursens figurer.
book/        Kursen satt som bok med LuaLaTeX; `make -C book` bygger PDF:en.
ci/          Kontrollskript: assemblering och simulering av programmen, länkar, konventioner.
```

Varje pass har samma form. `README.md` är kartan: vad passet tar upp, vad du läser före och gör
efter. Appendixen är innehållet, och läses i ordning. Det näst sista appendixet är alltid
**övningarna** och det sista **lösningsförslagen**, som publiceras efter respektive pass.

---

## Boken
Hela kursen finns också som bok, [Digitalteknik](./book/digitalteknik.pdf). Den byggs från
källorna i [`book/`](./book/README.md), där det också står hur du bygger den själv
(`make -C book`) och hur en ny utgåva publiceras.

---

## Att bygga
Kursens assemblerprogram assembleras med `avra`, som tar samma syntax som Microchip Studio, och de
program som anger ett förväntat resultat körs i simulatorn `simavr` och kontrolleras mot det.

```bash
make help        # Lista alla mål.
make build       # Assemblera alla assemblerprogram.
make test        # Assemblera och simulera; kontrollera varje @expect-rad.
make lint        # Markdown-länkar och kursens konventioner.
make diagrams    # Rita om figurerna (kräver .venv, se diagrams/README.md).
```

Verktygen installeras med apt på WSL/Ubuntu:

```bash
sudo apt -y update
sudo apt -y install git make gcc python3 avra simavr libsimavr-dev libelf-dev
```

Inget av detta behövs för att gå kursen. Deltagarna skriver och kör sina program i Microchip Studio
enligt [info/microchip_studio.md](./info/microchip_studio.md); verktygen här finns för att
kursmaterialet ska kunna kontrolleras.

---

## Licens
Kursmaterialet är licensierat under [CC BY 4.0](./LICENSE) - Jonas Granath och Erik Pihl. Det
gäller också boken i `book/`, dess text och figurer och PDF:en som byggs av dem.

Källkoden, det vill säga assemblerprogrammen, skripten under `ci/`, Python-koden under `diagrams/`
och bokens byggfiler (`dtbook.sty`, `dtbook.lua`, `figures.py` och dess `Makefile`), är
licensierad under [MIT](./LICENSE-CODE), eftersom CC BY 4.0 inte är avsedd för mjukvara.
Assemblerprogrammen som är tryckta i passen och i boken får också användas under MIT-licensen.

---
