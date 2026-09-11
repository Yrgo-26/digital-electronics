;********************************************************************************
; L09: A longer delay: a loop inside a loop.
;
; The inner loop, its ldi included, takes 3 * INNER cycles, as in short_delay.asm.
; Around it, every outer lap adds dec (1) and brne (2, or 1 on the last lap), and
; ldi r19 adds back the one cycle the last lap saves, so the whole delay takes
; OUTER * (3 * INNER + 3) cycles. With 208 and 255: 208 * 768 = 159 744 cycles,
; which is 9.984 ms at 16 MHz.
;********************************************************************************
.include "m328Pdef.inc"

.equ OUTER = 208                    ; Outer laps, 1-255.
.equ INNER = 255                    ; Inner laps per outer lap, 1-255.

.org 0x0000
    rjmp main

main:
    sbi DDRB, 0
    sbi PORTB, 0                    ; A pulse starts.

delay_start:
    ldi r19, OUTER                  ; 1 cycle
delay_outer:
    ldi r18, INNER                  ; 1 cycle per outer lap
delay_inner:
    dec r18                         ; 1 cycle per inner lap
    brne delay_inner                ; 2 per inner lap, 1 on the last
    dec r19                         ; 1 cycle per outer lap
    brne delay_outer                ; 2 per outer lap, 1 on the last
delay_end:
    cbi PORTB, 0                    ; The pulse ends, about 10 ms later.

end:
    rjmp end

; ---- Test (ci/simtest.py) ----
; @sim --cycles 200000 --between delay_start delay_end
; @expect between = 159744
; @expect PORTB = 0
