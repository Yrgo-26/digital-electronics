;********************************************************************************
; L08: Lighting LEDs on port B, a whole byte at a time and one bit at a time.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ser r16                         ; r16 = 0xFF
    out DDRB, r16                   ; Every pin of port B is an output.

    ldi r16, 0b00100001             ; LEDs on PB5 and PB0.
    out PORTB, r16                  ; Write all eight bits at once.

    sbi PORTB, 3                    ; Also light PB3, leaving the others as they were.
    cbi PORTB, 0                    ; Put out PB0, leaving the others as they were.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect DDRB = 0xFF
; @expect PORTB = 0b00101000
