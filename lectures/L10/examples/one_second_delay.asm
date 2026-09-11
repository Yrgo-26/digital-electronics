;********************************************************************************
; L10 example: one_second_delay
;
; Blinks the LED on PB5 (Arduino pin 13): one second on, one second off. The delay is two
; nested loops, an 8-bit outer loop around a 16-bit inner loop, and takes exactly
; 16 000 000 clock cycles, one second at 16 MHz.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.equ OUTER_TURNS = 80               ; Outer loop: 80 turns.
.equ INNER_TURNS = 49999            ; Inner loop: 49 999 turns of 4 cycles each.

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    sbi DDRB, 5                     ; PB5 is an output.
    ldi r17, 0b00100000             ; The mask that selects bit 5.

loop:
    in r16, PORTB                   ; Toggle PB5: read the port,
    eor r16, r17                    ; flip bit 5,
    out PORTB, r16                  ; and write it back.

delay_begin:
    ldi r20, OUTER_TURNS            ; 1 cycle.
outer:
    ldi r24, low(INNER_TURNS)       ; 1 cycle.
    ldi r25, high(INNER_TURNS)      ; 1 cycle.
inner:
    sbiw r24, 1                     ; 2 cycles: r25:r24 = r25:r24 - 1.
    brne inner                      ; 2 cycles while r25:r24 is not 0, 1 the last time.
    dec r20                         ; 1 cycle.
    brne outer                      ; 2 cycles while r20 is not 0, 1 the last time.
delay_end:
    rjmp loop                       ; 2 cycles. Toggle again.

; ---- Test (ci/simtest.py) ----
; @sim --cycles 20000000 --between delay_begin delay_end
; @expect between = 16000000
; @sim --cycles 8000000
; @expect PORTB = 0b00100000
; @sim --cycles 24000000
; @expect PORTB = 0b00000000
