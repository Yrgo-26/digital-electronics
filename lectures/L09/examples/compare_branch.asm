;********************************************************************************
; L09: If-else in assembly: a heater that switches on below 20 degrees.
;
; The temperature is a constant here. Change TEMPERATURE, rebuild, and run it again, or
; change r16 in Processor Status just before the cpi.
;********************************************************************************
.include "m328Pdef.inc"

.equ TEMPERATURE = 18               ; The measured temperature, in degrees.
.equ LIMIT = 20                     ; Below this, the heater is switched on.

.org 0x0000
    rjmp main

main:
    sbi DDRB, 0                     ; PB0 drives the heater: an output.
    ldi r16, TEMPERATURE

    cpi r16, LIMIT                  ; Compare: computes r16 - 20, keeps only the flags.
    brlo heater_on                  ; Branch if lower (C = 1): temperature < 20.
    cbi PORTB, 0                    ; Otherwise: heater off,
    rjmp done                       ; and jump past the other branch.
heater_on:
    sbi PORTB, 0                    ; Heater on.
done:
    rjmp done

; ---- Test (ci/simtest.py) ----
; @sim --until done
; @expect reached = 1
; @expect PORTB = 0b00000001
; @expect C = 1
