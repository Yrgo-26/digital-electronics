# Figurer

Kursens figurer ritas med kod, så att en ändrad sanningstabell, en ny grupp i ett Karnaughdiagram
eller ett nytt kontaktnät är en ändring och en omritning snarare än ett nytt ritarbete. Figurerna
är incheckade som PNG-filer, eftersom GitHub visar kursmaterialet direkt från repot; ingenting här
körs när någon läser kursen.

---

## Installation

```bash
python3 -m venv .venv
.venv/bin/pip install -r diagrams/requirements.txt
```

---

## Att rita om

```bash
make diagrams                                    # alla figurer, in i kursträdet
.venv/bin/python diagrams/build.py --list        # vilka figurer som finns, och vart de skrivs
.venv/bin/python diagrams/build.py l04_kmap_3var # en figur
.venv/bin/python diagrams/build.py --outdir /tmp/preview   # förhandsgranska, utan att röra repot
```

**Titta på varje figur du ritar.** En figur som ritas utan fel kan ändå vara fel: en bildtext som
klipps i kanten, en etikett som krockar med en ledning, en grupp som ringar in fel ruta. Inget av
det syns i koden, och alla renderar utan felmeddelande.

---

## Uppbyggnad
Verktygsmodulerna ritar, figurmodulerna beskriver vad som ska ritas.

| Fil | Innehåll |
| --- | --- |
| `style.py` | Alla färger, linjetjocklekar, typsnitt och storlekar. En ändring där ändrar alla figurer. |
| `shapes.py` | Gemensamma primitiver: fylld ruta, klammer, pil, streckad ram. |
| `paths.py` | Vart figurerna skrivs: `lecture("L04")`, `lab("lab2")`, `info()`, `exam()`. |
| `kmap.py` | Karnaughdiagram med två till fyra variabler, med grupper som går runt kanterna. |
| `gates.py` | Logiska grindar, både ANSI-symboler (via schemdraw) och IEC-symboler. |
| `contacts.py` | Kontaktnät i strömvägsschema: tryckknappar, reläkontakter, lampor och spolar. |
| `waveform.py` | Tidsdiagram: flera signaler mot en gemensam tidsaxel. |
| `flowchart.py` | Flödesplaner med symbolerna ur ISO 5807. |
| `bitfield.py`, `regfile.py`, `memory.py`, `flow.py` | Register, registerfilen, minneskartor och blockdiagram, från QAcademys assemblerkurs. |
| `avr.py` | ATmega328P-figurerna som delas av L07-L11. |
| `l01.py` ... `l12.py`, `lab1.py` ... | Figurmodulerna, en per pass eller laboration. |

En figurmodul definierar en ordlista `FIGURES`, från figurens namn till figuren och de sökvägar den
ska skrivas till. `build.py` hittar alla moduler som har en sådan, så en ny figur kräver ingen
registrering någon annanstans. Figurnamnen börjar med passets eller labbens namn, `l04_` eller
`lab2_`, så att två moduler aldrig råkar använda samma namn.

---
