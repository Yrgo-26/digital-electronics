;********************************************************************************
; L09: A short delay: one loop of 200 laps.
;
; Every lap is dec (1 cycle) and brne (2 cycles when it branches, 1 on the last lap),
; so the whole delay, ldi included, takes 3 * 200 = 600 cycles = 37.5 us at 16 MHz.
; Measure it with breakpoints on delay_start and delay_end and the Stop Watch.
;********************************************************************************
.include "m328Pdef.inc"

.equ LAPS = 200                     ; 1-255; 0 gives 256 laps.

.org 0x0000
    rjmp main

main:
    sbi DDRB, 0                     ; PB0 is an output.
    sbi PORTB, 0                    ; A pulse starts.

delay_start:
    ldi r18, LAPS                   ; 1 cycle
delay_loop:
    dec r18                         ; 1 cycle per lap
    brne delay_loop                 ; 2 cycles per lap, 1 on the last
delay_end:
    cbi PORTB, 0                    ; The pulse ends.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --between delay_start delay_end
; @expect between = 600
; @expect PORTB = 0
