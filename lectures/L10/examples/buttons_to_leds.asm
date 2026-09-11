;********************************************************************************
; L10 example: buttons_to_leds
;
; Reads the eight pins of port D and shows them on port B: a pressed button lights the LED
; with the same bit number. The buttons connect their pin to ground and use the internal
; pull-ups, so a pressed button reads 0; com turns that into a 1 for the LED.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ldi r16, 0x00
    out DDRD, r16                   ; Port D: all eight pins are inputs.
    ldi r16, 0xFF
    out PORTD, r16                  ; ... with their pull-ups switched on.
    out DDRB, r16                   ; Port B: all eight pins are outputs.

loop:
    in r16, PIND                    ; Read the level of all eight pins at once.
    com r16                         ; Invert: a pressed button (0) becomes a lit LED (1).
    out PORTB, r16                  ; Show the result.
    rjmp loop                       ; And again, for ever.

; ---- Test (ci/simtest.py) ----
; No button pressed: every pin is held high by its pull-up, and every LED is off.
; @sim --cycles 200
; @expect PORTB = 0b00000000
; @expect DDRD = 0x00
; @expect PORTD = 0xFF
; The buttons on PD2 and PD3 pressed.
; @sim --cycles 200 --event 50:D2=0 --event 50:D3=0
; @expect PORTB = 0b00001100
