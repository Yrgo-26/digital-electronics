;********************************************************************************
; L07: One number, four ways of writing it.
;
; r16, r17, r18 and r19 all end up holding 200, written in decimal, binary and two
; hexadecimal notations. r20 holds the ASCII code of the character 'A'.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ldi r16, 200                    ; Decimal.
    ldi r17, 0b11001000             ; Binary: 128 + 64 + 8 = 200.
    ldi r18, 0xC8                   ; Hexadecimal: 12 * 16 + 8 = 200.
    ldi r19, $C8                    ; Hexadecimal again, in the older $ notation.
    ldi r20, 'A'                    ; A character: its ASCII code, 65 = 0x41.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect r16 = 200
; @expect r17 = 200
; @expect r18 = 200
; @expect r19 = 200
; @expect r20 = 0x41
