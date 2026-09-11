;********************************************************************************
; L08: Three additions and a subtraction, and the flags each one leaves behind.
;
; Set a breakpoint on each of the labels check1 to check4 (or step with F11) and
; read SREG in Processor Status. The expected flags are written beside each
; instruction.
;********************************************************************************
.include "m328Pdef.inc"

.org 0x0000
    rjmp main

main:
    ldi r16, 0x7F                   ; 127, the largest positive signed byte.
    ldi r17, 0x01
    add r16, r17                    ; 0x80: C=0 Z=0 N=1 V=1 S=0 H=1
check1:
    ldi r16, 0xFF                   ; 255, the largest unsigned byte.
    add r16, r17                    ; 0x00: C=1 Z=1 N=0 V=0 S=0 H=1
check2:
    ldi r16, 0x80                   ; -128 as a signed byte.
    ldi r17, 0x80
    add r16, r17                    ; 0x00: C=1 Z=1 N=0 V=1 S=1 H=0
check3:
    ldi r16, 5
    ldi r17, 7
    sub r16, r17                    ; 0xFE: C=1 Z=0 N=1 V=0 S=1 H=1
check4:
    rjmp check4

; ---- Test (ci/simtest.py) ----
; @sim --until check1
; @expect r16 = 0x80
; @expect C = 0
; @expect Z = 0
; @expect N = 1
; @expect V = 1
; @expect S = 0
; @expect H = 1
; @sim --until check2
; @expect r16 = 0x00
; @expect C = 1
; @expect Z = 1
; @expect N = 0
; @expect V = 0
; @expect S = 0
; @expect H = 1
; @sim --until check3
; @expect r16 = 0x00
; @expect C = 1
; @expect Z = 1
; @expect N = 0
; @expect V = 1
; @expect S = 1
; @expect H = 0
; @sim --until check4
; @expect r16 = 0xFE
; @expect C = 1
; @expect Z = 0
; @expect N = 1
; @expect V = 0
; @expect S = 1
; @expect H = 1
