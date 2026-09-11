# Appendix A - Repetition

## A.1 Så används det här appendixet
Kursen har gått fort: tolv pass, fyra ämnen. Det här appendixet går igenom dem igen, ordnat efter
kursplanens lärandemål, så att du kan se vad du kan och vad du behöver läsa om.

Varje avsnitt har tre delar:
* **Det viktigaste**, kort, med de metoder som provet bygger på.
* **Kan du ...?**, en lista att bocka av. Svara på varje fråga på papper, utan att titta, och
  kontrollera sedan mot länken.
* **Vanliga fel**, de misstag som oftast kostar poäng.

Provets form, poäng och betygsgränser står i [exam/README.md](../../../exam/README.md). Där finns
också ett [övningsprov](../../../exam/practice_exam.md) med lösningsförslag. Gör det under två
timmar, utan miniräknare, med [referensbladet](../../../info/avr_instructions.md) bredvid, precis
som på det riktiga provet.

---

## A.2 Talsystem och binära koder
*Lärandemål: beskriva binära, hexadecimala och decimala talsystem, och omvandla talvärden mellan
dem.* ([L01](../../L01/README.md))

### Det viktigaste
* I ett **positionssystem** är varje siffra värd siffran gånger talbasen upphöjd till positionen,
  räknat från 0 längst till höger. Binärt har basen 2, hexadecimalt 16.
* **Binärt till decimalt**: addera vikterna för ettorna. `1010 1110` = 128 + 32 + 8 + 4 + 2 = 174.
* **Decimalt till binärt**: dra av den största vikt som får plats, om och om igen, eller dela med 2
  och läs resterna nedifrån ([L01
  A.4](../../L01/appendix/a_number_systems.md#a4-från-decimalt-till-binärt)).
* **Binärt och hexadecimalt**: fyra bitar är en hexadecimal siffra. `1011 0110` = `0xB6`. Omvandla
  alltid mellan decimalt och hexadecimalt **via binärt** om du är osäker ([L01
  A.6](../../L01/appendix/a_number_systems.md#a6-omvandling-mellan-alla-tre)).
* **n bitar** räcker till `2^n` värden, 0 till `2^n - 1`: en byte till 0-255.
* **Binär addition** görs som för hand, med minnessiffra. En summa som inte får plats i åtta bitar
  lämnar en minnessiffra, carry ([L01
  A.7](../../L01/appendix/a_number_systems.md#a7-binär-addition)).
* **Koder**: BCD skriver varje decimal siffra med fyra bitar, Graykod ändrar en bit i taget, och
  ASCII ger varje tecken ett tal: `'0'` = `0x30`, `'A'` = `0x41` ([L01 Appendix
  B](../../L01/appendix/b_binary_codes.md)).

### Kan du ...?
* ... omvandla 1100 1011, 142 och `0x5E` till de två andra talsystemen, utan miniräknare?
* ... förklara varför en hexadecimal siffra motsvarar exakt fyra bitar?
* ... addera två 8-bitars tal binärt och säga om det blir en minnessiffra?
* ... skriva 59 i BCD, och säga varför BCD inte är samma sak som 59 binärt?
* ... ange ASCII-koderna för tecknen `'4'` och `'C'`?

### Vanliga fel
* Att räkna positionerna från 1 i stället för från 0, så att varje vikt blir dubbelt för stor.
* Att gruppera bitar i fyror från vänster. Grupperna räknas **från höger**: `1 0110` är `0x16`.
* Att tro att BCD för 59 är 59 binärt. BCD är `0101 1001`, binärt är `0011 1011`.

---

## A.3 Grindar, boolesk algebra och kontaktnät
*Lärandemål: förklara grindar och logiska funktioner; beskriva logisk algebra och förenklingar av
booleska uttryck.* ([L02](../../L02/README.md), [L03](../../L03/README.md))

### Det viktigaste
* Sju grindar: NOT, AND, OR, NAND, NOR, XOR och XNOR. NAND, NOR och XNOR är inverserna av AND, OR
  och XOR, och XOR är 1 när ingångarna är olika.
* **Notation**: `A'` för NOT, `AB` för AND, `A + B` för OR. NOT binder hårdast, sedan AND, sist OR.
* **Från sanningstabell till uttryck**: en AND-term per etta, med varje variabel direkt eller
  inverterad; OR:a ihop termerna. Det ger ett uttryck på **SP-form** ([L02
  A.6](../../L02/appendix/a_logic_gates.md#a6-från-sanningstabell-till-uttryck)).
* **Förenkla** genom att bryta ut det gemensamma och använda `A + A' = 1`. Tre lagar räcker långt:
  `A + AB = A`, `A + A'B = A + B` och De Morgan ([L02
  A.4](../../L02/appendix/a_logic_gates.md#a4-räknelagarna)).
* **De Morgan**: `(A + B)' = A'B'` och `(AB)' = A' + B'`. Bryt strecket, byt tecknet ([L02
  A.5](../../L02/appendix/a_logic_gates.md#a5-de-morgans-lagar)).
* **Analys av ett grindnät**: skriv uttrycket vid varje grinds utgång, från ingångarna mot utgången,
  och räkna sedan ut sanningstabellen rad för rad ([L02
  A.8](../../L02/appendix/a_logic_gates.md#a8-analys-från-grindnät-till-sanningstabell)).
* **Kontaktnät**: kontakter i serie är AND, parallellt OR, och en brytande kontakt är NOT. Lampan
  lyser när det finns en sluten väg från +24 V till 0 V ([L02 Appendix
  B](../../L02/appendix/b_contact_networks.md),
  [L03 Appendix A](../../L03/appendix/a_contact_network_analysis.md)).

### Kan du ...?
* ... rita symbolen och skriva sanningstabellen för var och en av de sju grindarna?
* ... läsa av ett uttryck på SP-form ur en sanningstabell med tre variabler?
* ... förenkla `AB + AB' + A'B` till två variabler, och säga vilken lag varje steg använder?
* ... skriva `(A + B)'` utan parentes, och bygga OR av enbart NAND-grindar?
* ... skriva uttrycket och sanningstabellen för ett grindnät eller ett kontaktnät du inte sett
  förut?
* ... rita ett kontaktnät för `S1(S2 + S3')`?

### Vanliga fel
* Att glömma att NOT binder hårdare än AND: `AB'` är `A(B')`, inte `(AB)'`.
* Att använda De Morgan halvt: invertera variablerna men glömma att byta AND mot OR.
* Att tro att en brytande kontakt är öppen: den är **sluten** tills knappen trycks.

---

## A.4 Karnaughdiagram och IC-kretsar
*Lärandemål: använda Karnaughdiagram för analys och minimering av booleska uttryck; syntetisera
digitala kombinatoriska nät med IC-kretsar och kontakter; analysera digitala kombinatoriska nät.*
([L04](../../L04/README.md), [L05](../../L05/README.md))

### Det viktigaste
* Ett **Karnaughdiagram** är sanningstabellen ritad så att grannrutor skiljer sig i exakt en
  variabel. Raderna och kolumnerna står i **Graykod**: 00, 01, 11, 10.
* **Gruppera** ettorna i rektanglar om 1, 2, 4 eller 8 rutor, så stora som möjligt och så få som
  möjligt. Grupper får överlappa och gå runt kanterna; de fyra hörnen är grannar ([L04
  A.3](../../L04/appendix/a_karnaugh_maps.md#a3-att-gruppera),
  [A.5](../../L04/appendix/a_karnaugh_maps.md#a5-kanter-och-hörn)).
* **Läs av** varje grupp som de variabler som är konstanta inom den. En grupp om fyra i ett diagram
  med fyra variabler ger en term med två variabler.
* **Don't care**, X, får räknas som 1 om det ger en större grupp, annars som 0.
* **NAND-nät**: ett uttryck på SP-form blir två nivåer NAND-grindar, eftersom `AB + CD` =
  `((AB)'(CD)')'`.
* **74-serien**: fyra grindar per kapsel (sex inverterare i 74HC04), VCC på ben 14 och GND på
  ben 7. Oanvända ingångar får aldrig flyta ([L04 Appendix
  B](../../L04/appendix/b_integrated_circuits.md)).
* **Felsökning**: matningen på varje krets först, sedan ingångarna, sedan signalen grind för grind
  ([L05 Appendix A](../../L05/appendix/a_troubleshooting.md)).

### Kan du ...?
* ... rita ett tomt Karnaughdiagram för fyra variabler, med Graykoden rätt på båda axlarna?
* ... fylla i det från en lista med mintermer, och gruppera det minimalt?
* ... förklara varför hörnen i ett diagram med fyra variabler kan bilda en grupp?
* ... räkna ut hur många 74HC-kretsar ett nät behöver?
* ... förklara vad som händer med en flytande ingång på en 74HC-krets?

### Vanliga fel
* Att skriva axlarna i vanlig binär ordning, 00, 01, 10, 11. Då är grannrutorna inte grannar.
* Att göra en grupp om tre, eller en grupp som inte är en rektangel.
* Att behålla en grupp vars alla ettor redan täcks av andra grupper.

---

## A.5 Mikrodatorns uppbyggnad
*Lärandemål: redogöra för mikrodatorns uppbyggnad på blockschemanivå.* ([L06](../../L06/README.md),
[L07](../../L07/README.md))

### Det viktigaste
* En **mikrodator** består av en **CPU**, **minne** och **in- och utportar**, sammankopplade med
  **bussar** och drivna av en **klocka** ([L06
  B.2](../../L06/appendix/b_microcomputer.md#b2-blockschemat)).
* **CPU:n** har en **ALU** som räknar, **register** som håller värdena den räknar med, och en
  **styrenhet** som avkodar instruktionerna och styr resten.
* **Programräknaren**, PC, pekar på nästa instruktion. Instruktionscykeln är **hämta, avkoda,
  utföra**, en gång per instruktion ([L06
  B.4](../../L06/appendix/b_microcomputer.md#b4-programräknaren-och-instruktionscykeln)).
* ATmega328P har **tre minnen**: programmet i flash, som finns kvar utan ström; variablerna och
  stacken i SRAM, som töms när strömmen bryts; och EEPROM ([L07
  A.5](../../L07/appendix/a_avr_core.md#a5-tre-minnen)).
* Varje block är byggt av det kursen redan har gått igenom: ALU:n av grindar, register och PC av
  vippor, minnet av tusentals lås med en adressavkodare ([L06
  B.10](../../L06/appendix/b_microcomputer.md#b10-från-grind-till-dator)).

### Kan du ...?
* ... rita mikrodatorns blockschema och säga vad varje block gör?
* ... beskriva vad som händer i hämta, avkoda och utföra för en instruktion som `inc r16`?
* ... säga vilket minne programmet ligger i, och vilket stacken ligger i, och vilket av dem som
  finns kvar när strömmen bryts?
* ... förklara vad en buss är, och nämna två?

### Vanliga fel
* Att blanda ihop registren med dataminnet. Registren är 32 byte inuti CPU:n; SRAM är 2048 byte
  utanför den.
* Att tro att programmet ligger i SRAM. Det ligger i flash.

---

## A.6 Assemblerprogrammering
*Lärandemål: använda assemblerspråk för att programmera en mikrodator.*
([L07](../../L07/README.md)-[L10](../../L10/README.md))

### Det viktigaste
* En rad assembler är en **etikett**, en **instruktion** med **operander**, och en **kommentar**.
  **Direktiv** som `.include`, `.org`, `.equ` och `.def` blir ingen maskinkod.
* `ldi` laddar en konstant, men bara i `r16`-`r31`. Tal skrivs decimalt, `0b...` eller `0x...`.
* **Aritmetik och flaggor**: `add`, `sub`, `inc`, `dec` och resten skriver flaggorna i SREG. `C` är
  minnessiffra eller lån, `Z` att resultatet blev noll, `N` att bit 7 är satt ([L08
  A.6](../../L08/appendix/a_arithmetic_and_flags.md#a6-flaggorna)). Åtta bitar går runt: 255 + 1
  blir 0.
* **Logik**: `and`/`andi` nollställer bitar, `or`/`ori` ettställer, `eor` inverterar, med en mask
  ([L08 B.2](../../L08/appendix/b_logic_and_shifts.md#b2-masker)). `lsl` multiplicerar med 2 och
  `lsr` delar med 2.
* **Hopp**: `cp`/`cpi` är en subtraktion som bara sparar flaggorna, och det villkorliga hoppet läser
  dem: `breq`, `brne`, `brlo`, `brsh` ([L09
  A.4](../../L09/appendix/a_flowcharts_and_branches.md#a4-villkorliga-hopp)).
* **Loopar och fördröjningar**: en loop med `dec` och `brne` tar 3 cykler per varv, utom det sista,
  som tar 2. Vid 16 MHz är en cykel 62,5 ns ([L09
  B.3](../../L09/appendix/b_loops_and_delays.md#b3-vad-en-instruktion-kostar-i-tid)).
* **Portar**: `DDRx` väljer riktning, `PORTx` sätter en utgång eller pull-upen på en ingång, `PINx`
  läser ([L08 C.2](../../L08/appendix/c_output_port.md#c2-tre-register-per-port),
  [L10 B.2](../../L10/appendix/b_input_port.md#b2-knappen-och-pull-up-motståndet)). En knapp mot
  jord med pull-up läses som 0 när den är nedtryckt.
* **Subrutiner och stacken**: `rcall` lägger returadressen på stacken och `ret` hämtar den. En
  subrutin sparar varje register den ändrar med `push`, och återställer dem med `pop` i omvänd
  ordning ([L10 Appendix C](../../L10/appendix/c_subroutines_and_stack.md)).

### Kan du ...?
* ... följa ett kort program instruktion för instruktion och ange registren och flaggorna `C`, `Z`
  och `N` efter varje rad?
* ... räkna ut hur många cykler en loop tar, och hur lång tid det är vid 16 MHz?
* ... skriva ett program som läser en knapp och tänder en lysdiod?
* ... skriva en jämförelse och ett villkorligt hopp för "om `r16` är minst 100"?
* ... säga vad `SP` är efter ett `rcall` och två `push`, när den var `0x08FF` från början?

### Vanliga fel
* Att tro att den gula pilen i simulatorn visar instruktionen som just kördes. Den visar nästa.
* Att lägga en instruktion som ändrar flaggorna mellan `cpi` och hoppet.
* Att glömma att `inc` och `dec` inte ändrar `C`, och att `andi` inte heller gör det.
* Att räkna en loops sista varv som alla andra. Det sista villkorliga hoppet hoppar inte, och tar en
  cykel mindre.
* Att glömma `com` när knappar mot jord läses, så att programmet gör precis tvärtom.

---

## A.7 Styrobjekt
*Lärandemål: programmera mikrodatorn till att kontrollera styrobjekt.* ([L11](../../L11/README.md))

### Det viktigaste
* Ett styrsystem läser **ingångar**, fattar **beslut** och sätter **utgångar**. En tillståndstabell
  och en flödesplan före koden gör programmet enkelt att skriva och att kontrollera ([L11 Appendix
  B](../../L11/appendix/b_traffic_light.md)).
* En lysdiod behöver ett **förkopplingsmotstånd**: `(5 V - 2 V) / 220 Ω ≈ 14 mA`. Större laster
  styrs genom en transistor och ett relä ([L11 Appendix
  A](../../L11/appendix/a_control_objects.md)).
* En knapp **studsar**; ett program som räknar tryck väntar en kort stund efter varje ändring.

### Kan du ...?
* ... räkna ut strömmen genom en lysdiod med ett givet motstånd?
* ... rita flödesplanen för ett trafikljus, och översätta den till ett program?
* ... förklara varför en knapp kan räknas flera gånger, och hur det förhindras?

---

## A.8 Tips inför provet
* **Visa hur du räknar.** Metoden ger poäng även när svaret blir fel på grund av ett slarvfel, och
  ett fel som förs vidare till nästa deluppgift kostar bara en gång.
* **Kontrollera med en sanningstabell** när du har förenklat ett uttryck. Tre variabler är åtta
  rader och tar en minut.
* **Skriv alltid ut talsystemet**: `0x2C`, `0b0010 1100` eller 44. Ett tal utan skrivsätt kan läsas
  på tre sätt.
* **Följ ett program med en tabell**: en rad per instruktion och en kolumn per register och flagga.
* **Läs frågan två gånger.** Frågar den efter ett uttryck, en sanningstabell eller ett grindnät?
  Frågar den efter `C` efter en viss instruktion, eller efter hela programmet?

---
