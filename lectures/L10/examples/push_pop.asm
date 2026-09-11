;********************************************************************************
; L10 example: push_pop
;
; The stack is last in, first out: two values pushed in one order and popped in the same
; order come back swapped.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ldi r16, high(RAMEND)           ; SP = RAMEND = 0x08FF.
    out SPH, r16
    ldi r16, low(RAMEND)
    out SPL, r16

    ldi r16, 0x11
    ldi r17, 0x22
    push r16                        ; 0x08FF = 0x11, SP = 0x08FE.
    push r17                        ; 0x08FE = 0x22, SP = 0x08FD.
    pop r16                         ; r16 = 0x22 (the last one pushed), SP = 0x08FE.
    pop r17                         ; r17 = 0x11, SP = 0x08FF.

end:
    rjmp end                        ; Stay here forever: there is nothing to return to.

; ---- Test (ci/simtest.py) ----
; @sim --cycles 100
; @expect r16 = 0x22
; @expect r17 = 0x11
; @expect SP = 0x08FF
; @expect [0x08FF] = 0x11
; @expect [0x08FE] = 0x22
