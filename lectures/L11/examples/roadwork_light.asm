;********************************************************************************
; L11 example: roadwork_light
;
; A road-work light: one lane, two lights, red 4 s and green 4 s, for ever. Red is PB0
; (Arduino pin 8) and green PB2 (pin 10). The worked example in L11 Appendix B.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.equ RED = 0                        ; PB0, Arduino pin 8.
.equ GREEN = 2                      ; PB2, Arduino pin 10.

.equ QUARTER_MS = 250               ; 250 ms. Set it to 1 to run about 250 times
                                    ; faster in the simulator; set it back before
                                    ; flashing.

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

    ldi r16, (1 << RED) | (1 << GREEN)
    out DDRB, r16                   ; The two lights are outputs.

loop:
    ldi r16, (1 << RED)             ; Red, 4 s.
    out PORTB, r16
    ldi r24, 4
    rcall delay_s

    ldi r16, (1 << GREEN)           ; Green, 4 s.
    out PORTB, r16
    ldi r24, 4
    rcall delay_s

    rjmp loop                       ; And round again.

;--------------------------------------------------------------------------------
; delay_s: Waits r24 seconds (1-63), as 4 x r24 calls of delay_ms with 250 ms each.
; A call takes 16 000 084 x r24 + 18 cycles: about 5 microseconds too long per second.
;--------------------------------------------------------------------------------
delay_s:
    push r24                        ; Save the registers this subroutine changes.
    push r25
    mov r25, r24
    lsl r25                         ; r25 = 2 x r24 ...
    lsl r25                         ; ... = 4 x r24: the number of quarter seconds.
    ldi r24, QUARTER_MS             ; A quarter of a second is 250 ms.
delay_s_loop:
    rcall delay_ms
    dec r25
    brne delay_s_loop
    pop r25                         ; Restore them, in the opposite order.
    pop r24
    ret

;--------------------------------------------------------------------------------
; delay_ms: Waits r24 milliseconds (1-255) at 16 MHz.
; A call takes 16 000 x r24 + 18 cycles, the rcall and the ret included.
;--------------------------------------------------------------------------------
delay_ms:
    push r24                        ; Save the registers this subroutine changes.
    push r26
    push r27
delay_ms_outer:
    ldi r26, low(3999)              ; X = r27:r26 = 3999.
    ldi r27, high(3999)
delay_ms_inner:
    sbiw r26, 1                     ; 4 cycles per turn, 3 the last time.
    brne delay_ms_inner
    dec r24                         ; One more millisecond done.
    brne delay_ms_outer
    pop r27                         ; Restore them, in the opposite order.
    pop r26
    pop r24
    ret

; ---- Test (ci/simtest.py) ----
; One full cycle is 8 s = 128 000 000 cycles.
; @sim --cycles 32000000
; @expect PORTB = 0b00000001
; @sim --cycles 96000000
; @expect PORTB = 0b00000100
; @sim --cycles 160000000
; @expect PORTB = 0b00000001
