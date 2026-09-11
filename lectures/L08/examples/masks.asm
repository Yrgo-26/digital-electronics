;********************************************************************************
; L08: Setting, clearing, toggling and testing bits with masks.
;
; Every result goes to its own register, so they can all be read at the end.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ldi r16, 0b10110110             ; The starting pattern, used by every example.

    mov r17, r16
    andi r17, 0b00001111            ; Clear the upper four bits: 0b00000110
    mov r18, r16
    ori r18, 0b00000001             ; Set bit 0: 0b10110111
    mov r19, r16
    ldi r24, 0b11000000             ; No eori, so the mask goes in a register.
    eor r19, r24                    ; Toggle bits 7 and 6: 0b01110110
    mov r20, r16
    com r20                         ; Invert every bit: 0b01001001
    mov r21, r16
    andi r21, 0b00000100            ; Test bit 2: the result is not zero, so Z = 0.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect r17 = 0b00000110
; @expect r18 = 0b10110111
; @expect r19 = 0b01110110
; @expect r20 = 0b01001001
; @expect r21 = 0b00000100
; @expect Z = 0
