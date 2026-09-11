# L01 - Talsystem och binära koder

## Agenda
* Kursintroduktion: upplägg, laborationer, examination och verktyg.
* Digitalt och analogt: varför nästan all teknik i dag räknar med ettor och nollor.
* Positionssystem: det decimala, det binära och det hexadecimala talsystemet.
* Omvandling mellan decimalt, binärt och hexadecimalt, för hand.
* Bitar, byte och talområden: hur stora tal som ryms i 4, 8 och 16 bitar.
* Binär addition, och vad som händer när summan inte ryms.
* Binära koder: BCD, Graykod, ASCII, 7-segmentkod och paritetsbit.

---

## Föreläsningsupplägg
Passet varvar genomgång med korta övningar som görs på plats, i den här ordningen:
1. **Kursintroduktion** (ca 30 min). Kursens tre delar, schemat, de tre laborationerna,
   examinationen, och hur kursmaterialet i det här repot är upplagt. Se
   [kursinformationen](../../info/README.md).
2. **Digitalt och analogt** (ca 10 min). Varför en signal med bara två tillstånd tål brus, och
   varför det gör den till grunden för all modern elektronik.
3. **Positionssystem och det binära talsystemet** (ca 30 min). Talet 250 plockas isär i
   decimalt, och samma tanke tillämpas på talbasen 2. Övning 1 och 2 görs på plats.
4. **Det hexadecimala talsystemet och omvandlingar** (ca 40 min). Varför fyra bitar blir en
   hexadecimal siffra, och alla sex omvandlingsriktningar. Övning 3-5 görs på plats.
5. **Binär addition** (ca 15 min). Samma uppställning som på lågstadiet, med talbasen 2.
6. **Binära koder** (ca 30 min). BCD, Graykod, ASCII, 7-segmentkoden och paritetsbiten, med
   exempel på var de används.
7. **Sammanfattning** (ca 10 min), och en genomgång av kontrolluppgiften, som görs efter passet.

---

## Före föreläsningen
* Läs igenom [kursinformationen](../../info/README.md), särskilt schemat och examinationen.
* Läs [Appendix A](./appendix/a_number_systems.md), åtminstone A.1-A.3. Resten gås igenom under
  passet.
* Inget behöver installeras till det här passet.

---

## Efter föreläsningen
* Läs [Appendix B](./appendix/b_binary_codes.md) om binära koder.
* Arbeta igenom [Appendix C](./appendix/c_exercises.md). Kontrollera dina svar mot
  [Appendix D](./appendix/d_solutions.md) när lösningsförslagen har publicerats.
* Talsystemen används i resten av kursen, och de sitter först när du har räknat många
  omvandlingar själv. Räkna hellre för många än för få.

---

## Det här ska du kunna efteråt
* Förklara skillnaden mellan en digital och en analog signal, och varför digitala signaler tål
  brus.
* Beskriva det decimala, det binära och det hexadecimala talsystemet: talbas, siffror och
  positionernas vikter.
* Omvandla tal mellan decimalt, binärt och hexadecimalt för hand, i alla riktningar.
* Ange hur många olika värden ett tal med *n* bitar kan anta, och vilket det största är.
* Addera två binära tal, och avgöra om summan ryms i åtta bitar.
* Beskriva BCD, Graykod, ASCII och 7-segmentkod, och koda och avkoda tal och tecken i dem.
* Beräkna en jämn paritetsbit, och förklara vilka fel den upptäcker.

---

## Frågor att testa dig själv med
* Varför har den minst signifikanta positionen vikten 1 i *alla* talsystem?
* Hur ser du direkt på ett binärt tal om det är jämnt eller udda?
* Varför används hexadecimala tal till att skriva binära tal, och inte decimala?
* Talet `0x100` är ett större tal än `0xFF`, men bara med ett. Hur många bitar behövs för var och
  ett av dem?
* Vad händer med ett binärt tal när du lägger till en nolla längst till höger? Jämför med vad
  som händer med ett decimalt tal.
* Tecknet `'7'` och talet 7 är olika saker i en dator. Vad skiljer dem åt, och hur gör du om det
  ena till det andra?
* I vilken kod ändras exakt en bit mellan två på varandra följande tal, och varför är det
  användbart?

---

## Referens
* [Appendix A](./appendix/a_number_systems.md): talsystem, omvandlingar och binär addition.
* [Appendix B](./appendix/b_binary_codes.md): binära koder.
* [Appendix C](./appendix/c_exercises.md): övningarna.
* [Appendix D](./appendix/d_solutions.md): lösningsförslagen.
* Kalkylatorn i Windows, i läget **Programmerare**, visar samma tal decimalt, binärt och
  hexadecimalt samtidigt. Använd den för att kontrollera dina svar, aldrig för att ta fram dem.

---

## Nästa föreläsning
* Logiska grindar: NOT, AND, OR, NAND, NOR, XOR och XNOR, och deras sanningstabeller.
* Boolesk algebra: notationen, räknelagarna och De Morgans lagar.
* Från sanningstabell till grindnät, och från grindnät tillbaka till sanningstabell.
* Samma logik byggd med strömkontakter på 24 V, inför Labb 1.

---
