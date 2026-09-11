# Skriftligt prov

Kursen avslutas med ett skriftligt prov i [L12](../lectures/L12/README.md). Här står hur provet är
upplagt, vad det omfattar och hur det bedöms. Ett övningsprov med lösningsförslag finns att träna
på:

```text
practice_exam.md              Övningsprovet, bara frågorna. Gör det under två timmar.
practice_exam_solutions.md    Lösningsförslag med poäng per deluppgift.
```

Själva provet och dess lösningar är lärarens och ingår inte i det publicerade kursmaterialet.

---

## Provets form
* **Två timmar**, individuellt, i L12.
* **Hjälpmedel:** penna, suddgummi och linjal. Ingen miniräknare. Ett
  [referensblad med AVR-instruktionerna](../info/avr_instructions.md) delas ut tillsammans med
  provet; det är samma blad som använts under kursen.
* **40 poäng**, fördelade på sex frågor. Varje fråga har deluppgifter, och poängen står vid varje
  deluppgift.
* Svaren skrivs på separata papper, med en ny fråga på ett nytt papper.

### Betygsgränser

| Betyg | Poäng |
|-------|-------|
| U | under 20 |
| G | 20-29 |
| VG | 30-40 |

Slutbetyget på kursen bygger på provet och laborationerna tillsammans, se
[kursinformationen](../info/README.md#examination).

---

## Vad provet omfattar
Provet omfattar hela kursen utom sekvensnät och vippor, som förekommer bara som en del av
mikrodatorns uppbyggnad. Frågorna är desamma till form och poäng på varje prov:

| Fråga | Område | Pass | Lärandemål | Poäng |
|-------|--------|------|------------|-------|
| 1 | Talsystem och koder | L01 | beskriva talsystem; omvandla talvärden | 8 |
| 2 | Grindar och boolesk algebra | L02 | förklara grindar; beskriva logisk algebra och förenkling | 8 |
| 3 | Karnaughdiagram | L04 | använda Karnaughdiagram för minimering | 6 |
| 4 | Analys av ett kombinatoriskt nät, grindnät eller kontaktnät | L02-L05 | analysera digitala kombinatoriska nät | 6 |
| 5 | Mikrodatorns uppbyggnad | L06-L07 | redogöra för mikrodatorns uppbyggnad | 4 |
| 6 | Assemblerprogrammering | L07-L10 | använda assemblerspråk för att programmera en mikrodator | 8 |
| | | | | **40** |

Lärandemålen om att syntetisera nät med IC-kretsar och kontakter, och att styra styrobjekt,
examineras i laborationerna, där de hör hemma.

Assemblerfrågorna gäller ATmega328P med klockfrekvensen 16 MHz, och de instruktioner som står på
referensbladet. Ingen fråga kräver att en instruktionskod eller en cykeltid kan utantill; det som
behövs står på bladet.

---

## Hur provet bedöms
* **Metoden ger poäng.** En korrekt uträkning med ett slarvfel är värd mer än ett rätt svar utan
  uträkning. Ett svar utan uträkning kan få full poäng bara där frågan inte ber om någon.
* **Följdfel kostar en gång.** Om en deluppgift bygger på svaret i en tidigare, och det svaret var
  fel, bedöms den senare deluppgiften utifrån det felaktiga svaret. Ett fel i en sanningstabell som
  förs vidare till ett Karnaughdiagram kostar poäng i tabellen, inte i diagrammet.
* **Talsystemet ska synas.** Ett svar som `2C` utan skrivsätt är tvetydigt och ger inte full poäng.
  Skriv `0x2C`, `0010 1100` eller 44.
* **Program bedöms efter vad de gör, inte efter stavningen.** Ett program som skulle fungera men har
  ett felstavat registernamn eller ett saknat kommatecken förlorar ingenting. Ett program som läser
  fel bit, eller glömmer att en knapp är aktivt låg, förlorar de poäng den delen gäller.
* **Namngivna fällor.** Några deluppgifter finns till för att se om ett vanligt misstag undviks,
  till exempel en flagga som en instruktion inte ändrar, eller en Karnaughaxel i binär ordning i
  stället för Graykod. Lösningsförslagen säger var fällorna finns, och ett svar som går i en fälla
  förlorar de poäng som fällan gäller, inte hela deluppgiftens.

---
