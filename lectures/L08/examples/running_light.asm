;********************************************************************************
; L08: A running light on port B, made with rol and the carry flag.
;
; rol moves bit 7 into C and C into bit 0, so the single one travels through nine
; places: bits 0 to 7, and then the carry flag, when every LED is dark for one step.
; Step it with F11 and watch PORTB in the I/O window.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ser r16
    out DDRB, r16                   ; All of port B is output.
    clc                             ; C = 0, so no stray one is rotated in.
    ldi r16, 0b00000001             ; Start with one LED lit.

loop:
    out PORTB, r16                  ; Show the pattern.
    rol r16                         ; Move it one place to the left, through C.
    rjmp loop

; ---- Test (ci/simtest.py) ----
; Six cycles reach loop, and every pass takes four (out 1, rol 1, rjmp 2), so pass k has
; written its pattern after 7 + 4k cycles.
; @sim --cycles 8
; @expect PORTB = 0b00000001
; @sim --cycles 36
; @expect PORTB = 0b10000000
; @sim --cycles 39
; @expect PORTB = 0b00000000
; @expect C = 1
; @sim --cycles 44
; @expect PORTB = 0b00000001
