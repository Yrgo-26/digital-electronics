;********************************************************************************
; L09: A loop that runs a given number of times: the sum 1 + 2 + ... + 10.
;
; The counter counts down from 10 to 0, and the loop ends when it reaches zero. The
; current counter is shown on port B, so the laps can be followed in the I/O window.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ser r16
    out DDRB, r16                   ; Port B is output.
    clr r17                         ; r17 = the sum so far = 0
    ldi r16, 10                     ; r16 = the counter: laps left to run

loop:
    out PORTB, r16                  ; Show the counter.
    add r17, r16                    ; sum = sum + counter
    dec r16                         ; One lap fewer left. Sets Z when it reaches 0.
    brne loop                       ; Not zero yet: go round again.

end:
    rjmp end                        ; r17 = 10 + 9 + ... + 1 = 55

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect r17 = 55
; @expect r16 = 0
; @expect PORTB = 1
