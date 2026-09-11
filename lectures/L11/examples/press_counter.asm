;********************************************************************************
; L11 example: press_counter
;
; Counts presses of the button on PD2 (Arduino pin 2) and shows the count in binary on
; PB0-PB3 (Arduino pins 8-11), 0 to 15 and round again. A mechanical button bounces for a
; few milliseconds when it closes and when it opens, so after every change the program
; waits 20 ms before it looks at the button again. Without the waits, one press could be
; counted several times.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.equ BUTTON = 2                     ; PD2, Arduino pin 2.
.equ SETTLE_MS = 20                 ; Longer than the button bounces, shorter than a press.

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

    ldi r16, 0b00001111
    out DDRB, r16                   ; PB0-PB3 are outputs.
    cbi DDRD, BUTTON                ; The button pin is an input ...
    sbi PORTD, BUTTON               ; ... with its pull-up switched on.
    clr r17                         ; r17 counts the presses.

loop:
wait_press:
    sbic PIND, BUTTON               ; Skip the jump when the button is pressed (0).
    rjmp wait_press
    inc r17                         ; One more press.
    andi r17, 0x0F                  ; Four LEDs: count 0-15 and round again.
    out PORTB, r17
    ldi r24, SETTLE_MS              ; Let the contact settle.
    rcall delay_ms

wait_release:
    sbis PIND, BUTTON               ; Skip the jump when the button is released (1).
    rjmp wait_release
    ldi r24, SETTLE_MS              ; Let the contact settle again.
    rcall delay_ms
    rjmp loop

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
; Two presses, each bouncing once when it closes and once when it opens (1 ms apart):
; press at 100 000 cycles, release at 2 000 000, press at 4 000 000, release at 6 000 000.
; @sim --cycles 8000000 --pin D2=1 --event 100000:D2=0 --event 116000:D2=1 --event 132000:D2=0 --event 2000000:D2=1 --event 2016000:D2=0 --event 2032000:D2=1 --event 4000000:D2=0 --event 4016000:D2=1 --event 4032000:D2=0 --event 6000000:D2=1 --event 6016000:D2=0 --event 6032000:D2=1
; @expect r17 = 2
; @expect PORTB = 0b00000010
; No press at all.
; @sim --cycles 2000000 --pin D2=1
; @expect PORTB = 0b00000000
