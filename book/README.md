# Boken

Kursen satt som bok med LuaLaTeX: tolv kapitel, ett per pass, och därefter som bilagor de tre
laborationshandledningarna, guiden till Microchip Studio, referensbladet med AVR-instruktionerna,
det skriftliga provet med övningsprovet och dess lösningsförslag, och sist lösningsförslagen till
övningarna.

Boken har inga datum, veckor, klassnamn eller skolnamn, så att den kan användas år efter år.

---

## Att bygga den

```bash
sudo apt -y install make texlive-luatex texlive-latex-extra texlive-lang-european \
                    fonts-texgyre fonts-texgyre-math fonts-dejavu-core poppler-utils
python3 -m venv .venv                                # En gång: miljön figurerna ritas i,
.venv/bin/pip install -r diagrams/requirements.txt   # samma som `make diagrams` använder.
make -C book                   # Skriver book/digitalteknik.pdf, daterad i dag.
make -C book VERSION=v1.0.0    # Samma sak, med utgåvans namn på titelsidan.
make -C book part PART=04      # Bara förordet och kapitel 4 med dess lösningar, i build/part-04/.
make -C book figures           # Bara figurerna, till book/build/figures.
make -C book clean             # Tar bort book/build/ och PDF:en.
```

`texlive-lang-european` ger den svenska avstavningen. Utan den byggs boken ändå, men utan
avstavning, och polyglossia varnar för det.

Bygget ritar först alla figurer som [`diagrams/build.py`](../diagrams/build.py) känner till som
vektor-PDF:er, med [`figures.py`](./figures.py), och kopierar exempelprogrammen till
`build/code/` utan det testblock som CI läser i slutet av dem. Sedan körs LuaLaTeX två gånger, så
att innehållsförteckningen och korsreferenserna hinner sätta sig. Till sist skrivs de överfulla och
underfulla rader och de varningar som finns i loggen ut, och bygget misslyckas om någon referens
är odefinierad.

`make part` bygger en bit av boken för sig: ett kapitel (`PART=01` till `PART=12`, med kapitlets
lösningsförslag), eller en bilaga (`lab1`, `lab2`, `lab3`, `studio`, `avr`, `exam`, `answers`).
Bitarna som hoppas över räknas ändå, så att kapitlet får samma nummer som i hela boken. Referenser
till andra bitar blir odefinierade och listas; hela boken är kontrollen av att inga finns kvar.

---

## Att publicera en ny utgåva

Varje utgåva publiceras som en release på GitHub. Pusha en tagg med utgåvans versionsnummer, till
exempel `v1.0.0`:

```bash
git tag v1.0.0
git push origin v1.0.0
```

[Book-arbetsflödet](../.github/workflows/book.yml) bygger då PDF:en med taggen på titelsidan och
lägger den i en release med samma namn.

---

## Vad som finns var

```text
book.tex             Boken: förord, tolv kapitel och bilagorna, i ordning.
dtbook.sty           Alla visuella beslut: sida, typsnitt, färger, kod, figurer, övningar.
dtbook.lua           Hur \code{...} sätter kod och tal i löptext.
figures.py           Ritar figurerna i diagrams/ som vektor-PDF:er, till build/figures.
front/               Titelsidor och förord.
chapters/NN/         Kapitel NN: chapter.tex (inledningen), en fil per teoriappendix i passet
                     LNN, summary.tex (sammanfattningen) och exercises.tex (övningarna).
back/lab1.tex        Bilaga A: Labb 1, från labs/lab1/README.md.
back/lab2.tex        Bilaga B: Labb 2, från labs/lab2/README.md.
back/lab3/           Bilaga C: Labb 3, från labs/lab3/, en fil per handledning.
back/studio.tex      Bilaga D: Microchip Studio, från info/microchip_studio.md.
back/avr.tex         Bilaga E: referensbladet, från info/avr_instructions.md.
back/exam/           Bilaga F-H: det skriftliga provet, övningsprovet och dess lösningsförslag.
back/answers/        Bilaga I: lösningsförslagen till övningarna, en fil per kapitel.
```

Varje `.tex`-fil som är satt från kursmaterialet börjar med en kommentar som säger vilken källa den
kommer från, till exempel:

```tex
% Section 1.1, from lectures/L01/appendix/a_number_systems.md.
```

---

## Att uppdatera innehållet

Kursmaterialet är källan, och boken följer det. **Tre sorters innehåll beter sig olika:**

* **Figurerna uppdaterar sig själva.** Boken ritar varje figur från samma kod i `diagrams/` som
  PNG-bilderna i passen, så en ändrad figur finns i boken vid nästa bygge. Skärmbilderna under
  `info/images/` tas med som de PNG-filer de är.
* **Exempelprogrammen som trycks i sin helhet uppdaterar sig själva.** Boken läser filerna under
  `lectures/*/examples/` och `labs/lab3/code/` direkt (`\asmfile{...}`).
* **Texten och kodsnuttarna i den gör det inte.** Ett kapitels text är en satt kopia av passets
  Markdown. När du ändrar ett appendix eller en README, gör samma ändring i den `.tex`-fil vars
  huvudkommentar pekar på den. Detsamma gäller `labs/`, `info/microchip_studio.md`,
  `info/avr_instructions.md` och `exam/`.

Några konventioner, så att en ändring ser ut som resten av boken:

* Kodblock: `asmcode` (AVR-assembler) och `console` (text). Ett textblock med tecken utanför
  ASCII, till exempel ·, → eller å, ä och ö, eller en uppställd uträkning som en binär addition
  med minnessiffror, är en `textdrawing`, som behåller varje kolumn. Ett ```` ```math ````-block är
  `\[ ... \]`.
* Kod i löptext: `\code{...}`, skriven precis som i källan. Inuti den skrivs `%` som `\%`, en
  ensam klammer som `\{` eller `\}`, och `#` som `\#` i en rubrik eller en bildtext.
* Referenser: `\secref{c4:a3}` är avsnittet som är satt från A.3 i L04, `\secref{c2:app:b}` är hela
  Appendix B i L02, `övning~\ref{c6:ex:4}` är övning 4 i L06 (i boken övning 6.4), och
  `kapitel~\ref{c8:ch}` är kapitlet från L08. Bilagorna heter `app:lab1`, `app:lab2`, `app:lab3`,
  `app:studio`, `app:avr`, `app:exam`, `app:practice`, `app:practice:answers` och `app:answers`.
* Figurer: `\bookfigure{namn}{Bildtext.}{etikett}` för en figur som `diagrams/build.py` ritar, med
  dess namn där (`build.py --list`), och `\bookimage{bredd}{sökväg}{Bildtext.}{etikett}` för en
  skärmbild. Figurerna har sin egen förklarande text, så bildtexten är kort.
* Övningar: `\exercise{Titel}{Sort}` med sorterna `Förståelse`, `Räkna för hand`,
  `Konstruktion`, `Program`, `Kontroll` och `Fördjupning`; `parts` för delarna a), b) ...
  (`\begin{parts}[start=5]` för att fortsätta på e) efter en mellanliggande text), och `\task` för
  en del med egen rubrik.
* Laborationer: `\labtask{Uppgift 3}{OR}`, `\prep{F1}`, `\redovisa{...}` och `filltable` för en
  tabell som fylls i för hand.
* Lösningsförslag: `\answer{c2:ex:1}{Titel}` för en övning och `\pt{a}` för en del, i
  `back/answers/cNN.tex`. En ny övning som inte är ett program behöver sitt lösningsförslag där.
* Ett nytt appendix i ett pass blir en ny fil i `chapters/NN/`, som `\input` från kapitlets
  `chapter.tex`.

---

## Skillnader mot kursmaterialet

Boken följer kursmaterialet, med några avsiktliga undantag:

* **Inga datum, veckor, klassnamn eller skolnamn.** Schemat i `info/README.md` är inte med, och
  där en övning använder klassens namn som data (texten i övning 1.10 a) och övningsprovets titel)
  är det utbytt mot något neutralt. Filens huvudkommentar säger var.
* **Lösningsförslagen gäller bara övningar som inte är program.** Uträkningar, konstruktioner,
  förklaringar och de delar av en programövning som görs på papper, som en förutsägelse eller en
  cykelräkning, har sina lösningar i bilaga I. Programmen som övningarna ber om, och
  lösningsprogrammen till Labb 3, finns bara i kursmaterialet.
* **Det skriftliga provet och dess lösningar är inte med.** De är lärarens och publiceras aldrig
  (se `.gitignore`); boken har bara beskrivningen av provet och övningsprovet.
* **Passens föreläsningsupplägg är inte med.** Minutplanen för varje pass är lärarens och finns i
  passets README.
* **Kapitel 3 och 5 har egna titlar.** Passen L03 och L05 heter som sina laborationer, men i boken
  är laborationshandledningarna bilagor med just de namnen, så kapitlen heter efter sitt eget
  innehåll: *Analys och felsökning av kontaktnät* och *Felsökning av grindnät*.

---

## Licens

Boken, dess text och figurer och PDF:en som byggs av dem, är licensierad under
[CC BY 4.0](../LICENSE), liksom kursmaterialet den är satt från. Den här katalogens byggfiler
(`dtbook.sty`, `dtbook.lua`, `figures.py` och `Makefile`) är licensierade under
[MIT-licensen](../LICENSE-CODE), liksom all kod i kursen, och under den får också programmen som
är tryckta i boken användas.

---
