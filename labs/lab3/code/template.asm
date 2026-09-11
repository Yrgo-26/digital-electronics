;********************************************************************************
; Lab 3, part N: <title>
;
; <What the program does, in one or two sentences.>
;
; Author: <your names>
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ; Write your program here.

end:
    rjmp end                        ; Stay here forever: there is nothing to return to.
