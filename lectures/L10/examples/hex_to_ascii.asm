;********************************************************************************
; L10 example: hex_to_ascii
;
; Converts the byte in r16 into two ASCII characters, the way it would be written in
; hexadecimal: 0x3C becomes '3' in r20 and 'C' in r21. The same five lines convert each
; nibble; L10 Appendix C turns them into a subroutine.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ldi r16, 0x3C                   ; The byte to convert.

    ; The high nibble: 0x3C -> 0x03 -> '3'.
    mov r24, r16                    ; Work on a copy, so r16 keeps its value.
    swap r24                        ; Swap the two nibbles: 0x3C -> 0xC3.
    andi r24, 0x0F                  ; Keep only the low nibble: 0xC3 -> 0x03.
    cpi r24, 10                     ; A digit 0-9, or a letter A-F?
    brlo high_digit                 ; 0-9: skip the extra step.
    subi r24, -7                    ; A-F: add 7 more, so that 10 lands on 'A'.
high_digit:
    subi r24, -0x30                 ; Add 0x30, the ASCII code for '0'.
    mov r20, r24                    ; r20 = '3' = 0x33.

    ; The low nibble: 0x3C -> 0x0C -> 'C'.
    mov r24, r16
    andi r24, 0x0F                  ; Keep only the low nibble: 0x3C -> 0x0C.
    cpi r24, 10
    brlo low_digit
    subi r24, -7
low_digit:
    subi r24, -0x30
    mov r21, r24                    ; r21 = 'C' = 0x43.

end:
    rjmp end                        ; Stay here forever: there is nothing to return to.

; ---- Test (ci/simtest.py) ----
; @sim --cycles 100
; @expect r20 = 0x33
; @expect r21 = 0x43
; @expect r16 = 0x3C
