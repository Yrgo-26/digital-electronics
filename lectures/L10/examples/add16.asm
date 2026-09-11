;********************************************************************************
; L10 example: add16
;
; 16-bit arithmetic with register pairs: 1000 + 2000 = 3000 with add and adc, a copy of
; the pair with movw, and adiw and sbiw on the result.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ldi r24, low(1000)              ; r25:r24 = 1000 = 0x03E8.
    ldi r25, high(1000)
    ldi r22, low(2000)              ; r23:r22 = 2000 = 0x07D0.
    ldi r23, high(2000)

    add r24, r22                    ; Low bytes: 0xE8 + 0xD0 = 0x1B8. r24 = 0xB8, C = 1.
    adc r25, r23                    ; High bytes and the carry: 0x03 + 0x07 + 1 = 0x0B.
                                    ; r25:r24 = 0x0BB8 = 3000.

    movw r18, r24                   ; Copy the pair: r19:r18 = 3000.
    adiw r24, 1                     ; r25:r24 = 3001.
    sbiw r24, 2                     ; r25:r24 = 2999 = 0x0BB7.

end:
    rjmp end                        ; Stay here forever: there is nothing to return to.

; ---- Test (ci/simtest.py) ----
; @sim --cycles 100
; @expect r18 = 0xB8
; @expect r19 = 0x0B
; @expect r24 = 0xB7
; @expect r25 = 0x0B
