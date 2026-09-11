;********************************************************************************
; L10 example: blink_subroutine
;
; Blinks the LED on PB5 (Arduino pin 13) twice a second, using a delay subroutine that
; takes the number of milliseconds to wait in r24. The subroutine saves every register it
; changes, so the caller's registers are the same after the call as before it.
;********************************************************************************
.include "m328Pdef.inc"             ; Register names for the ATmega328P: PORTB, DDRB ...

.org 0x0000                         ; The processor starts here after reset.
    rjmp main                       ; Jump over everything else, to main.

;--------------------------------------------------------------------------------
; main: The program starts here.
;--------------------------------------------------------------------------------
main:
    ldi r16, high(RAMEND)           ; Point the stack pointer at the top of SRAM,
    out SPH, r16                    ; high byte first ...
    ldi r16, low(RAMEND)
    out SPL, r16                    ; ... then the low byte. SP = 0x08FF.

    sbi DDRB, 5                     ; PB5 is an output.
    ldi r17, 0b00100000             ; The mask that selects bit 5.

loop:
    in r16, PORTB                   ; Toggle PB5.
    eor r16, r17
    out PORTB, r16
    ldi r24, 250                    ; Wait 250 ms.
call_site:
    rcall delay_ms
after_call:
    rjmp loop

;--------------------------------------------------------------------------------
; delay_ms: Waits r24 milliseconds (1-255) at 16 MHz.
;
; Each turn of the outer loop takes exactly 16 000 cycles, 1 ms. With the rcall, the
; pushes, the pops and the ret, a call takes 16 000 x r24 + 18 cycles.
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
    ret                             ; Back to the instruction after the rcall.

; ---- Test (ci/simtest.py) ----
; @sim --cycles 5000000 --between call_site after_call
; @expect between = 4000018
; @sim --cycles 5000000 --until after_call
; @expect r24 = 250
; @expect SP = 0x08FF
; Inside delay_ms: two bytes of return address and three saved registers on the stack.
; @sim --cycles 2000000
; @expect PORTB = 0b00100000
; @expect SP = 0x08FA
; @sim --cycles 6000000
; @expect PORTB = 0b00000000
