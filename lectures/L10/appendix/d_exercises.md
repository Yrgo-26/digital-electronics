# Appendix D - Övningar

> **Så kontrollerar du ditt arbete.** Övningarna märkta **Program** skrivs i Microchip Studio och
> kontrolleras i simulatorn: förutsäg vad som ska hända, stega, och jämför. Knappar simuleras genom
> att biten i `PIND` ändras för hand i fönstret I/O ([info/microchip_studio.md, avsnitt
> 4.5](../../../info/microchip_studio.md#45-simulera-en-ingång)).
>
> Övningarna märkta **Räkna för hand** och **Förståelse** görs på papper, utan miniräknare, och
> kontrolleras mot [Appendix E](./e_solutions.md). Gör varje övning innan du läser lösningen. Där en
> övning har ett troligt felsvar tar lösningen upp det också, och säger varför det är fel.
>
> Instruktionerna finns på [referensbladet](../../../info/avr_instructions.md).

Varje övning är märkt med sin sort. Exakt en övning är en **Kontroll**, och i det här passet är det
övning 11.

---

## 1. Tecken och koder
**Räkna för hand.**

Använd tabellen i [A.1](./a_ascii_and_16bit.md#a1-tecken-är-också-tal).

**a)** Vilka ASCII-koder har tecknen `'5'`, `'9'`, `'E'` och `'F'`? Svara hexadecimalt.

**b)** Vilket tal blir kvar när ASCII-koden för `'8'` minskas med ASCII-koden för `'0'`?

**c)** Förklara med en mening varför omvandlingen av värdena 10-15 behöver sju extra, men inte
omvandlingen av 0-9.

**d)** Raden `ldi r16, 'E'` och raden `ldi r16, 0x45` assembleras till exakt samma maskinkod. Varför
skriver man ändå ibland den första?

---

## 2. En byte blir text
**Räkna för hand.**

Programmet i [A.3](./a_ascii_and_16bit.md#a3-en-byte-blir-två-tecken) körs med `ldi r16, 0x9E` i
stället för `0x3C`.

**a)** Fyll i värdet i `r24` efter varje instruktion för den höga nibblen: `mov`, `swap`, `andi`,
och sedan det som `cpi`/`brlo` bestämmer. Vilket värde får `r20`?

**b)** Gör samma sak för den låga nibblen. Vilket värde får `r21`?

**c)** Vilken text står i minnet om programmet avslutas med `sts 0x0100, r20` och `sts 0x0101, r21`?

**d)** Gör om a-c för `ldi r16, 0x5A`.

---

## 3. Från tecken till värde
**Räkna för hand.**

Använd koden i [A.4](./a_ascii_and_16bit.md#a4-tillbaka-från-tecken-till-värde).

**a)** Följ tecknet `'B'` (`0x42`) genom koden. Vilket värde får `r22`?

**b)** Följ tecknet `'4'`.

**c)** *(fördjupning)* Någon skriver ett litet `b` på tangentbordet, ASCII `0x62`. Vilket värde
lämnar koden i `r22`, och varför är det fel? Föreslå en ändring som hanterar små bokstäver.

---

## 4. Registerpar
**Räkna för hand.**

**a)** Skriv talen 2500, 256, 255 och 40 000 som 16-bitars tal i hexadecimal form, och ange vad
`low()` och `high()` blir för vart och ett.

**b)** `r25` innehåller `0x12` och `r24` innehåller `0x34`. Vilket decimalt tal är `r25:r24`?

**c)** Vilket är det största tal ett registerpar kan hålla? Varför just det?

---

## 5. Addition och subtraktion med 16 bitar
**Räkna för hand.**

**a)** `r25:r24` = `0x12F0` och `r23:r22` = `0x0A20`. Följ `add r24, r22` och `adc r25, r23` steg
för steg, som i [A.7](./a_ascii_and_16bit.md#a7-addition-och-subtraktion-med-16-bitar): vad blir
`r24`, `C` och `r25`? Kontrollera svaret genom att räkna om båda talen och summan decimalt.

**b)** Någon skriver `add r25, r23` i stället för `adc r25, r23`. Vilket svar blir det då, och med
hur mycket är det fel?

**c)** `r21:r20` = `0x0100`, alltså 256. Följ `ldi r22, 1`, `ldi r23, 0`, `sub r20, r22` och
`sbc r21, r23`. Vad blir `r20`, `C` och `r21`, och vilket tal är resultatet?

**d)** Någon vill göra samma sak kortare, med `sbiw r20, 1`. Varför går det inte att assemblera, och
vilket registerpar hade fungerat?

---

## 6. En fördröjning på 10 ms
**Räkna för hand.**

**a)** Hur många klockcykler är 10 ms vid 16 MHz?

**b)** En enda 16-bitars loop med `sbiw` och `brne`, som i
[A.10](./a_ascii_and_16bit.md#a10-en-lång-tidsfördröjning), plus de två `ldi` före den. Hur många
varv `N` ska loopen gå för att hela fördröjningen ska bli så nära 10 ms som möjligt, och hur många
cykler blir det exakt?

**c)** Samma fördröjning med subrutinen `delay_ms` från
[C.4](./c_subroutines_and_stack.md#c4-en-subrutin-med-parameter-delay_ms): vilket värde ska `r24`
ha, och hur många cykler tar anropet?

**d)** Vilken av de två är närmast 10 ms? Vilken skulle du välja i ett program, och varför?

---

## 7. Knappen som läses baklänges
**Förståelse.**

En knapp är kopplad mellan PD2 och jord, som i
[B.2](./b_input_port.md#b2-knappen-och-pull-up-motståndet).

**a)** Förklara, med pull-up-motståndet, varför `PIND` bit 2 läses som 0 när knappen är nedtryckt.

**b)** Programmet glömmer att slå på pull-upen (`sbi PORTD, 2`). Vad läser programmet när knappen är
släppt? Varför är det svårt att hitta det felet genom att prova?

**c)** Varför innehåller `buttons_to_leds.asm` instruktionen `com`? Vad hade lysdioderna visat utan
den, när ingen knapp är nedtryckt?

---

## 8. Följ programmet
**Räkna för hand.**

Programmet i [B.3](./b_input_port.md#b3-att-läsa-hela-porten) läser `PIND` och visar det inverterade
värdet på `PORTB`.

**a)** `PIND` läses som `0b11111011`. Vilka knappar är nedtryckta, och vad blir `PORTB`?

**b)** Programmet ändras så att `andi r16, 0xF0` läggs in mellan `com` och `out`. Vad blir `PORTB`
nu för samma `PIND`? Och för `PIND` = `0b01101111`?

**c)** Hur många gånger per sekund ungefär läser loopen porten vid 16 MHz? Räkna cyklerna för de
fyra instruktionerna i loopen.

---

## 9. Start och stopp med självhållning
**Program.**

I [L02](../../L02/README.md) byggdes en start/stopp-krets med ett relä som håller sig självt: ett
tryck på startknappen drar reläet, och det förblir draget när knappen släpps, tills stoppknappen
trycks. Samma funktion ska nu skrivas som ett program.

* Startknappen sitter på PD2 och stoppknappen på PD3, båda mot jord med pull-up.
* En "motor", en lysdiod på PB0, startar när startknappen trycks, och fortsätter gå när knappen
  släpps.
* Motorn stannar när stoppknappen trycks.
* Om båda knapparna hålls nedtryckta samtidigt ska motorn **stå still**: stopp går före start, av
  säkerhetsskäl.

**a)** Rita en flödesplan innan du skriver någon kod.

**b)** Skriv programmet, med `sbic` eller `sbis`.

**c)** Testa i simulatorn alla fyra fallen: start, släpp start, stopp, och båda samtidigt.

**d)** Var i programmet finns "minnet", det som motsvarar reläets självhållning?

---

## 10. rcall, ret och stacken
**Förståelse.**

**a)** Beskriv de två saker `rcall` gör, i den ordning den gör dem.

**b)** Varför behöver `ret` stacken? Kunde returadressen ha sparats i ett av de 32 registren i
stället?

**c)** `SP` är `0x08FF` när ett `rcall` körs. Vad är `SP` när subrutinen börjar? Och efter `ret`?

**d)** Efter `ret` ligger returadressen kvar i minnet. Varför är det inget problem?

---

## 11. Kontroll: förutsäg stacken
**Kontroll.** *Förutsäg för hand, kontrollera i simulatorn, förklara skillnaden.*

Programmet nedan anropar en subrutin som lägger två register på stacken. Adresserna i programminnet
kommer från listfilen och står i kommentarerna.

```asm
.include "m328Pdef.inc"

.org 0x0000
    rjmp main                       ; 0x0000

main:
    ldi r16, high(RAMEND)           ; 0x0001
    out SPH, r16                    ; 0x0002
    ldi r16, low(RAMEND)            ; 0x0003
    out SPL, r16                    ; 0x0004
    ldi r16, 0xA5                   ; 0x0005
    ldi r17, 0x3C                   ; 0x0006
    rcall save_two                  ; 0x0007
end:
    rjmp end                        ; 0x0008

save_two:
    push r16                        ; 0x0009
    push r17                        ; 0x000A
here:
    pop r17                         ; 0x000B
    pop r16
    ret
```

**a) För hand.** När programmet står på etiketten `here`, alltså efter de två `push`: vilket värde
har `SP`, och vilka byte ligger på adresserna `0x08FF`, `0x08FE`, `0x08FD` och `0x08FC`? Skriv upp
svaret innan du går vidare.

**b) I simulatorn.** Skriv in programmet, sätt en brytpunkt på `pop r17` och kör dit. Läs `SP` i
Processor Status och bytena i fönstret Memory med **data IRAM** valt.

**c) Jämför.** Stämmer din förutsägelse? Den vanligaste avvikelsen är att returadressens två byte
står i fel ordning, eller att `SP` är en byte fel. Om ditt svar skiljer sig: vilket av de två felen
var det, och varför?

**d)** Stega vidare till instruktionen efter `ret`. Vilket värde har `SP` nu, och vilka av de fyra
bytena har ändrats?

---

## 12. Hitta felet
**Förståelse.** *(fördjupning)*

**a)** En subrutin börjar med `push r16` och `push r17`, och slutar med `pop r16`, `pop r17` och
`ret`. Den assembleras utan fel och återvänder rätt. Vad är fel, och hur märks det i programmet som
anropar den?

**b)** En annan subrutin börjar med `push r16` och `push r17`, men slutar med bara `pop r17` och
`ret`. Vad händer när `ret` körs? Varför märks felet mycket tydligare än i a)?

**c)** Hur kan du i simulatorn, med ett enda värde, se att en subrutin inte lämnar stacken som den
fann den?

---

## 13. Hela byten som text
**Program.** *(fördjupning)*

Skriv en subrutin `byte_to_ascii` som gör om byten i `r24` till två tecken: det för den höga nibblen
i `r24` och det för den låga i `r25`. Den ska använda `nibble_to_ascii` från
[C.9](./c_subroutines_and_stack.md#c9-hex-till-ascii-som-subrutin) och följa kursens regel om
register.

**a)** Vilka register ändrar `byte_to_ascii`, och vilka av dem måste sparas?

**b)** Skriv subrutinen och ett huvudprogram som anropar den med `0xB7` och lägger tecknen på adress
`0x0100` och `0x0101`.

**c)** Kontrollera i fönstret Memory att texten `B7` står där. Hur djup blir stacken som mest?

---
