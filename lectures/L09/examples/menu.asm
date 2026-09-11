;********************************************************************************
; L09: Choosing between several alternatives: a light pattern selected by a mode.
;
; Mode 0 puts every LED out, 1 lights all of them, 2 the lower half and 3 the upper half.
; Any other mode is an error, shown as every other LED. Every alternative ends at the
; same place, show, so the program has one way in and one way out.
;********************************************************************************
.include "m328Pdef.inc"

.equ MODE = 2                       ; The selected mode.

.org 0x0000
    rjmp main

main:
    ser r16
    out DDRB, r16                   ; Port B is output.
    ldi r16, MODE

    cpi r16, 0
    breq mode_0
    cpi r16, 1
    breq mode_1
    cpi r16, 2
    breq mode_2
    cpi r16, 3
    breq mode_3
    ldi r17, 0b01010101             ; None of them: the error pattern.
    rjmp show
mode_0:
    ldi r17, 0b00000000
    rjmp show
mode_1:
    ldi r17, 0b11111111
    rjmp show
mode_2:
    ldi r17, 0b00001111
    rjmp show
mode_3:
    ldi r17, 0b11110000
show:
    out PORTB, r17                  ; The one place every alternative ends up.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect PORTB = 0b00001111
