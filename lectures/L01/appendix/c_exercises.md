# Appendix C - Övningar

> **Så kontrollerar du ditt arbete.** Alla övningar här räknas med papper och penna. Räkna varje
> omvandling för hand först, och kontrollera den sedan genom att räkna tillbaka åt andra hållet:
> ett binärt tal du har räknat fram ur ett decimalt ska ge samma decimala tal när du summerar
> vikterna. Den kontrollen hittar nästan alla fel, och den finns alltid till hands, också på
> provet.
>
> Lösningsförslagen finns i [Appendix D](./d_solutions.md) när de har publicerats. Där visas också
> de vanligaste felaktiga svaren, och varför de är fel.
>
> Varje övning är märkt med sin sort. Övning 13 är passets **kontrolluppgift**: där räknar du för
> hand och kontrollerar med kalkylatorn i Windows.

---

## 1. Positionssystem
**Förståelse.**

**a)** Talet 4072 är decimalt. Ange för varje siffra dess position, dess vikt och det värde den
bidrar med.

**b)** I ett talsystem med talbasen 5 finns bara siffrorna 0-4. Vilken vikt har position 2 där?
Vilket decimalt tal är $243_5$?

**c)** Förklara med egna ord varför den högra positionen har vikten 1 oavsett talbas.

---

## 2. Från binärt till decimalt
**Räkna för hand.**

Omvandla till decimalt. Använd viktraden 128, 64, 32, 16, 8, 4, 2, 1.

**a)** `1101`

**b)** `1 0000`

**c)** `0110 0100`

**d)** `1000 0001`

**e)** `1111 1111`

**f)** `1101 0110`

---

## 3. Från decimalt till binärt
**Räkna för hand.**

Omvandla till binärt. Använd vikttabellen för a)-c) och division med 2 för d)-f), och kontrollera
varje svar genom att räkna tillbaka.

**a)** 13

**b)** 37

**c)** 100

**d)** 200

**e)** 255

**f)** 1000

---

## 4. Binärt och hexadecimalt
**Räkna för hand.**

Omvandla från binärt till hexadecimalt:

**a)** `1010 1111`

**b)** `0011 1100`

**c)** `1 1110`

**d)** `11 1110 1000`

Omvandla från hexadecimalt till binärt:

**e)** `0x7F`

**f)** `0xC3`

**g)** `0x2A5`

---

## 5. Hexadecimalt och decimalt
**Räkna för hand.**

Omvandla från hexadecimalt till decimalt:

**a)** `0x2A`

**b)** `0xFF`

**c)** `0x100`

**d)** `0x3E8`

Omvandla från decimalt till hexadecimalt, med valfri metod:

**e)** 75

**f)** 160

**g)** 4095

---

## 6. Bitar och talområden
**Förståelse.**

**a)** Hur många olika värden kan ett tal med 4, 8, 12 respektive 16 bitar anta, och vilket är det
största?

**b)** Hur många bitar behövs minst för att kunna representera 1000 olika värden?

**c)** En nivågivare i en tank ska rapportera nivån i hela steg från 0 till 200. Hur många bitar
behövs? Hur många av kombinationerna blir då oanvända?

**d)** Utan att räkna ut värdet: är `1011 0111` ett jämnt eller ett udda tal? Är det större eller
mindre än 128? Motivera.

---

## 7. Binär addition
**Räkna för hand.**

Addera de 8-bitars binära talen. Skriv ut minnessiffrorna, och kontrollera varje summa genom att
göra om talen till decimalt.

**a)** `0011 1010 + 0001 0110`

**b)** `0111 1111 + 0000 0001`

**c)** `1100 1000 + 0110 0100`

**d)** Vilken av summorna i a)-c) ryms inte i åtta bitar? Vad blir kvar i ett 8-bitars register,
och vad hände med resten?

---

## 8. BCD
**Räkna för hand.**

**a)** Koda talet 47 i BCD. Koda det sedan som ett 8-bitars binärt tal, och jämför.

**b)** Koda årtalet 2026 i BCD. Hur många bitar behövs?

**c)** Vilket decimalt tal är `1001 0011` i BCD? Vilket tal är samma bitmönster som binärt tal?

**d)** Är `0110 1010` ett giltigt BCD-tal? Motivera.

---

## 9. Graykod
**Förståelse.**

**a)** Bygg Graykoden med tre bitar genom att spegla tvåbitarskoden `00, 01, 11, 10`, enligt
[B.3](./b_binary_codes.md#b3-graykod).

**b)** Hur många bitar ändras när en binär räknare går från 7 till 0 (`111` till `000`)? Hur många
ändras mellan motsvarande Graykoder?

**c)** En vinkelgivare med tre bitar står mellan läge 1 och läge 2. Förklara vad styrsystemet kan
läsa under övergången om givaren använder vanlig binärkod, och vad det kan läsa om den använder
Graykod.

---

## 10. ASCII
**Räkna för hand.**

Använd tabellen i [B.4](./b_binary_codes.md#b4-ascii).

**a)** Skriv texten `AI26` som ASCII-koder, hexadecimalt.

**b)** Vilken text är ASCII-koderna `0x48 0x65 0x6A`? (`e` ligger på `0x65`, och bokstäverna ligger
i ordning.)

**c)** Hur mycket skiljer `a` och `A`? Vilken enda bit skiljer dem åt?

**d)** Ett program har läst in siffertecknet `7` från ett tangentbord. Hur får programmet fram
talet 7 ur det? Och hur gör det om talet 3 till tecknet `3`?

---

## 11. 7-segmentkod
**Konstruktion.**

Använd bitordningen g f e d c b a från [B.5](./b_binary_codes.md#b5-7-segmentkod).

**a)** Vilka segment ska lysa för den hexadecimala siffran `E`? Ange koden binärt och
hexadecimalt.

**b)** En display får koden `0x6D`. Vilken siffra visas?

**c)** Segment g har gått sönder och lyser aldrig. Vilka siffror går då inte längre att skilja
från någon annan siffra? Vilka ser bara konstiga ut?

---

## 12. Paritetsbit
**Räkna för hand.**

Använd jämn paritet: paritetsbiten väljs så att det totala antalet ettor blir jämnt, och den
skickas som bit 7 framför de sju ASCII-bitarna.

**a)** Ange den byte som skickas för tecknen `B`, `C` och `G`.

**b)** En mottagare får byten `1100 0001`. Har ett fel inträffat? Kan mottagaren veta vilket
tecken som skulle ha skickats?

**c)** Visa med ett eget exempel att två felaktiga bitar i samma byte inte upptäcks.

---

## 13. Kontroll: för hand, och sedan med kalkylatorn
**Kontroll.** *Räkna för hand, kontrollera med ett verktyg, och förklara det du ser.*

Gör delarna i ordning, och skriv ned varje svar innan du går vidare. Poängen går förlorad om du
tittar i kalkylatorn först.

**a) För hand.** Omvandla 173 till binärt och hexadecimalt, `0x3E8` till decimalt och binärt, och
`0b1100 1010` till decimalt och hexadecimalt.

**b) Med kalkylatorn.** Öppna kalkylatorn i Windows och välj läget **Programmerare**. Skriv in
vart och ett av talen i det talsystem det är givet i (klicka först på `DEC`, `HEX` eller `BIN`),
och läs av de andra två. Stämmer dina svar? Om inte: hitta felet i din uträkning, inte bara
rätt svar.

**c) Något du inte kan förklara än.** Välj `DEC`, skriv `-1` (tryck `1` och sedan `+/-`), och läs
av `HEX` och `BIN`. Byt sedan ordlängd med knappen där det står `QWORD` tills det står `BYTE`, och
läs av igen. Skriv ned vad du ser i båda fallen.

**d)** Vilket positivt tal har samma bitmönster som det kalkylatorn visade för `-1` i läget
`BYTE`? Gissa varför datorn skriver `-1` just så. Svaret, som heter **tvåkomplement**, kommer i
[L08](../../L08/README.md).

---

## 14. Att lägga till en nolla *(fördjupning)*
**Förståelse.**

**a)** `0b1011` är 11. Vilket tal är `0b10110`, där en nolla har lagts till längst till höger? Och
`0b101100`?

**b)** Formulera en regel: vad händer med värdet på ett binärt tal när alla bitar flyttas ett steg
åt vänster och en nolla fylls på från höger?

**c)** Vad händer i stället med värdet om den högra biten tas bort och alla bitar flyttas ett steg
åt höger? Pröva med `0b1011` och `0b1010`.

**d)** Vad motsvarar det att lägga till en nolla längst till höger i ett hexadecimalt tal? Pröva
med `0x2A`.

Mikrodatorn i kursen har instruktioner som gör exakt det här med ett register, och du kommer att
använda dem i [L08](../../L08/README.md).

---
