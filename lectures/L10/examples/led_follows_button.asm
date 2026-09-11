;********************************************************************************
; L10 example: led_follows_button
;
; The LED on PB5 (Arduino pin 13) is lit while the button on PD2 (Arduino pin 2) is held
; down. One bit is tested directly with sbic, without reading the whole port.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    sbi DDRB, 5                     ; PB5 is an output.
    cbi DDRD, 2                     ; PD2 is an input (it already is after reset) ...
    sbi PORTD, 2                    ; ... with its pull-up switched on.

loop:
    sbic PIND, 2                    ; Skip the next instruction if PD2 is 0 (pressed).
    rjmp released                   ; PD2 is 1: the button is released.
pressed:
    sbi PORTB, 5                    ; Light the LED.
    rjmp loop
released:
    cbi PORTB, 5                    ; Turn the LED off.
    rjmp loop

; ---- Test (ci/simtest.py) ----
; Released: the pull-up holds PD2 high.
; @sim --cycles 200 --pin D2=1
; @expect PORTB = 0b00000000
; Pressed after 1000 cycles, released after 2000.
; @sim --cycles 1500 --pin D2=1 --event 1000:D2=0
; @expect PORTB = 0b00100000
; @sim --cycles 2500 --pin D2=1 --event 1000:D2=0 --event 2000:D2=1
; @expect PORTB = 0b00000000
