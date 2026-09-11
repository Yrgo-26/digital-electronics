;********************************************************************************
; L07: The first program.
;
; Loads two numbers, copies one of them, and counts up and down. Nothing happens outside
; the processor: step through it in the simulator and watch r16-r20 change.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P.

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump to main.

main:
    ldi r16, 5                      ; r16 = 5
    ldi r17, 3                      ; r17 = 3
    mov r18, r16                    ; r18 = r16, so r18 = 5 (r16 is unchanged)
    inc r18                         ; r18 = r18 + 1 = 6
    dec r17                         ; r17 = r17 - 1 = 2
    clr r19                         ; r19 = 0
    ser r20                         ; r20 = 0xFF (all ones)

end:
    rjmp end                        ; Stay here forever.

; ---- Test (ci/simtest.py) ----
; @sim --until end
; @expect reached = 1
; @expect r16 = 5
; @expect r17 = 2
; @expect r18 = 6
; @expect r19 = 0
; @expect r20 = 0xFF
; @expect cycles = 9
