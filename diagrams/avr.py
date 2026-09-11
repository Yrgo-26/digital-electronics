"""The ATmega328P figures, shared by the microcomputer lectures L07 to L11.

Ported from the QAcademy assembly course with Swedish text, and simplified where that course
aimed at readers who already write C. Every figure is written to each lecture that embeds it,
so the copies stay identical:

* L07: the register file, SREG, the three memory spaces, an `ldi` encoded, the toolchain.
* L08: SREG again, the four states of a pin, the Arduino pin map, the LED circuit.
* L10: the button circuit, and the stack across an `rcall` and a `ret`.
* L11: the pin map, the LED circuit and the button circuit again, for wiring the real board.

`stack_figure` is public, for any later figure that needs to show the stack changing.
"""

from __future__ import annotations

from typing import Sequence

import schemdraw.elements as elm

import bitfield
import flow
import memory
import paths
import regfile
import shapes
import style
from bitfield import Bit, Register

# ----------------------------------------------------------------------------------------
# The register file.
# ----------------------------------------------------------------------------------------
_POINTERS = {26: "XL", 27: "XH", 28: "YL", 29: "YH", 30: "ZL", 31: "ZH"}


def _annotate_regfile(ax, layout) -> None:
    left, right = layout.column_x(1)
    _, _, _, high = layout.cell(16)
    shapes.brace(ax, left, right, high + 0.30, "ldi når bara dessa",
                 size=style.TINY_SIZE)
    for name, (low_reg, high_reg) in (("X", (26, 27)), ("Y", (28, 29)), ("Z", (30, 31))):
        _, low, edge, _ = layout.cell(high_reg)
        _, _, _, top = layout.cell(low_reg)
        shapes.vbrace(ax, low, top, edge + 0.30, name, color=style.ACCENT_COLOR_2,
                      size=style.FONT_SIZE)


REGISTER_FILE = regfile.figure(
    fills={number: "accent" for number in range(16, 32)}
    | {number: "accent2" for number in _POINTERS},
    labels=dict(_POINTERS),
    caption=("Alla 32 fungerar med mov, add, sub, inc och dec.",
             "Bara r16-r31 kan laddas med en konstant (ldi, andi, ori, subi, cpi)."),
    annotate=_annotate_regfile,
    pad=(0.0, 0.0, 1.6, 1.15))

# ----------------------------------------------------------------------------------------
# SREG.
# ----------------------------------------------------------------------------------------
_SREG = Register(
    "SREG",
    [Bit("I", "muted"), Bit("T", "muted"), Bit("H"), Bit("S"), Bit("V"), Bit("N"),
     Bit("Z", "accent2"), Bit("C", "accent2")],
    address="0x5F")


def _annotate_sreg(ax, layout) -> None:
    left, _ = layout.cell_x(layout.bit_index(0, "H"))
    _, right = layout.cell_x(layout.bit_index(0, "C"))
    _, high = layout.row_y(0)
    shapes.brace(ax, left, right, high + bitfield.BRACE_LIFT,
                 "flaggor som aritmetik och logik skriver", size=style.TINY_SIZE)
    left, _ = layout.cell_x(layout.bit_index(0, "Z"))
    _, right = layout.cell_x(layout.bit_index(0, "C"))
    low, _ = layout.row_y(0)
    shapes.brace(ax, left, right, low - 0.30, "breq/brne, brlo/brsh",
                 below=True, color=style.ACCENT_COLOR_2, size=style.TINY_SIZE)


SREG = bitfield.figure(
    [_SREG],
    caption=("C = carry (minnessiffra)   Z = zero (noll)   N = negative (negativ)",
             "V = overflow (tvåkomplementsspill)   S = sign (N xor V)   H = half carry"),
    annotate=_annotate_sreg,
    caption_drop=1.32,
    pad=(0.0, 0.30, 0.0, 1.05))

# ----------------------------------------------------------------------------------------
# The three memory spaces.
# ----------------------------------------------------------------------------------------
_FLASH = memory.Column(
    "Programminne (flash)",
    [
        memory.Region("Avbrottsvektorer", "0x0000", "0x0033", "här startar programmet",
                      "accent", height=1.30),
        memory.Region("Ditt program", "0x0034", "0x3EFF", "instruktioner och konstanter",
                      height=1.55),
        memory.Region("Bootloader", "0x3F00", "0x3FFF", "Arduinos, 512 byte", "muted",
                      height=1.30),
    ],
    width=5.8,
    note=("32 kB, adresseras i ord", "(16 bitar per adress)."))

_DATA = memory.Column(
    "Dataminne",
    [
        memory.Region("Registren r0-r31", "0x0000", "0x001F", "32 byte", "accent2",
                      height=1.30),
        memory.Region("I/O-register", "0x0020", "0x005F", "PORTB, DDRB, PIND, SREG ...",
                      "accent", height=1.30),
        memory.Region("Utökade I/O-register", "0x0060", "0x00FF", "timrar m.m.",
                      height=1.30),
        memory.Region("SRAM", "0x0100", "0x08FF", "2048 byte; stacken i toppen",
                      height=1.55),
    ],
    width=5.8,
    note=("Här ligger variabler och stacken.", "RAMEND = 0x08FF."))

_EEPROM = memory.Column(
    "EEPROM",
    [
        memory.Region("EEPROM", "0x0000", "0x03FF", "1024 byte, tål strömavbrott",
                      height=2.20),
    ],
    width=5.8,
    note=("Används inte i kursen.",))

MEMORY_SPACES = memory.figure(
    [_FLASH, _DATA, _EEPROM],
    caption=("Tre separata minnen, inte tre delar av ett. Programmet ligger i flash,",
             "variablerna och stacken i SRAM."))

# ----------------------------------------------------------------------------------------
# One instruction, encoded.
# ----------------------------------------------------------------------------------------
_ENCODING_CELL_W = 1.02

_PATTERN = Register(
    "mönster",
    [Bit(c, fill) for c, fill in
     [("1", "muted"), ("1", "muted"), ("1", "muted"), ("0", "muted"),
      ("K", "accent"), ("K", "accent"), ("K", "accent"), ("K", "accent"),
      ("d", "accent2"), ("d", "accent2"), ("d", "accent2"), ("d", "accent2"),
      ("K", "accent"), ("K", "accent"), ("K", "accent"), ("K", "accent")]])

_ASSEMBLED = Register(
    "0xE20A",
    [Bit(c, fill) for c, fill in
     [("1", "muted"), ("1", "muted"), ("1", "muted"), ("0", "muted"),
      ("0", "accent"), ("0", "accent"), ("1", "accent"), ("0", "accent"),
      ("0", "accent2"), ("0", "accent2"), ("0", "accent2"), ("0", "accent2"),
      ("1", "accent"), ("0", "accent"), ("1", "accent"), ("0", "accent")]])


def _annotate_encoding(ax, layout) -> None:
    _, high = layout.row_y(0)
    low, _ = layout.row_y(1)
    lift = high + bitfield.BRACE_LIFT

    def cells(first: int, last: int) -> tuple[float, float]:
        return layout.cell_x(first)[0], layout.cell_x(last)[1]

    opcode_left, opcode_right = cells(0, 3)
    shapes.brace(ax, opcode_left, opcode_right, lift, "ldi", color=style.MUTED_COLOR,
                 size=style.TINY_SIZE)
    dest_left, dest_right = cells(8, 11)
    shapes.brace(ax, dest_left, dest_right, lift, "d = Rd - 16", color=style.ACCENT_COLOR_2,
                 size=style.TINY_SIZE)
    high_left, high_right = cells(4, 7)
    low_left, low_right = cells(12, 15)
    shapes.brace(ax, high_left, high_right, lift, "K[7:4]", size=style.TINY_SIZE)
    shapes.brace(ax, low_left, low_right, lift, "K[3:0]", size=style.TINY_SIZE)
    shapes.brace(ax, dest_left, dest_right, low - 0.30, "r16", below=True,
                 color=style.ACCENT_COLOR_2, size=style.TINY_SIZE)
    shapes.brace(ax, high_left, high_right, low - 0.30, "0x2", below=True,
                 size=style.TINY_SIZE)
    shapes.brace(ax, low_left, low_right, low - 0.30, "0xA", below=True,
                 size=style.TINY_SIZE)


LDI_ENCODING = bitfield.figure(
    [_PATTERN, _ASSEMBLED],
    caption=("ldi r16, 0x2A blir maskinkoden 0xE20A. Konstanten delas i två halvor, och",
             "registerfältet har bara fyra bitar, därför når ldi bara r16-r31."),
    annotate=_annotate_encoding,
    caption_drop=1.30,
    cell_w=_ENCODING_CELL_W,
    pad=(0.0, 0.30, 0.0, 1.15))

# ----------------------------------------------------------------------------------------
# The toolchain, as Microchip Studio runs it.
# ----------------------------------------------------------------------------------------
TOOLCHAIN = flow.figure(
    [
        flow.Node("main.asm", (0.0, 0.0), "programmet du skriver", "accent2"),
        flow.Node("Assembler", (6.6, 0.0), "Build (F7) i Studio", width=5.0),
        flow.Node("projekt.hex", (13.2, 1.3), "maskinkoden", "accent", width=5.0),
        flow.Node("projekt.lss", (13.2, -1.3), "listfil: kod + adresser", width=5.0),
        flow.Node("Simulatorn", (20.0, 1.3), "stega, se register", width=5.4),
        flow.Node("Arduino Uno", (20.0, -1.3), "via avrdude (L11)", "muted", width=5.4),
    ],
    [flow.Edge(0, 1), flow.Edge(1, 2), flow.Edge(1, 3), flow.Edge(2, 4),
     flow.Edge(2, 5, dashed=True)],
    caption=("Assemblern översätter varje rad till en eller två 16-bitars instruktioner.",
             "Hexfilen är det som körs, i simulatorn eller på ett riktigt kort."))

# ----------------------------------------------------------------------------------------
# The four states of a pin.
# ----------------------------------------------------------------------------------------
_STATE_W = 6.4
_STATE_H = 2.0
_STATE_GAP = 0.30
_HEADER_GAP = 0.45
_ROW_LABEL_GAP = 0.45

_STATES = {
    (0, 0): ("Ingång, flytande", "läser brus om inget är anslutet", "plain"),
    (1, 0): ("Ingång med pull-up", "läser 1 tills något drar ner den", "accent2"),
    (0, 1): ("Utgång, låg", "stiftet hålls på 0 V", "accent"),
    (1, 1): ("Utgång, hög", "stiftet hålls på 5 V", "accent"),
}

_STATE_CAPTION = (
    "PINx är det tredje registret och ingår inte i rutnätet: läs PINx för att se stiftets",
    "verkliga nivå. DDRx avgör riktningen, PORTx nivån eller pull-upen.")


def _state_bounds(column: int, row: int) -> tuple[float, float]:
    return (column * (_STATE_W + _STATE_GAP), -(row + 1) * _STATE_H - row * _STATE_GAP)


def _draw_port_states(drawing, ax) -> None:
    for (column, row), (heading, detail, fill) in _STATES.items():
        left, low = _state_bounds(column, row)
        shapes.cell(ax, left, low, _STATE_W, _STATE_H, fill)
        middle = left + _STATE_W / 2
        style.text(ax, heading, (middle, low + _STATE_H / 2 + 0.22), valign="bottom",
                   size=style.SMALL_SIZE)
        style.text(ax, detail, (middle, low + _STATE_H / 2 - 0.22), valign="top",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
    for column, text in ((0, "PORTx = 0"), (1, "PORTx = 1")):
        left, _ = _state_bounds(column, 0)
        style.text(ax, text, (left + _STATE_W / 2, _HEADER_GAP), valign="bottom")
    for row, (text, detail) in ((0, ("DDRx = 0", "ingång")), (1, ("DDRx = 1", "utgång"))):
        _, low = _state_bounds(0, row)
        style.text(ax, text, (-_ROW_LABEL_GAP, low + _STATE_H / 2 + 0.22), halign="right",
                   valign="bottom")
        style.text(ax, detail, (-_ROW_LABEL_GAP, low + _STATE_H / 2 - 0.22), halign="right",
                   valign="top", size=style.TINY_SIZE, color=style.MUTED_COLOR)
    _, bottom = _state_bounds(0, 1)
    style.caption(ax, _STATE_CAPTION, _STATE_RIGHT / 2, bottom - 0.55)


_STATE_RIGHT = _STATE_W * 2 + _STATE_GAP
_STATE_TEXT_LEFT, _STATE_TEXT_RIGHT = style.caption_bounds(_STATE_CAPTION, _STATE_RIGHT / 2)
_STATE_LEFT = min(-_ROW_LABEL_GAP - style.text_width("DDRx = 0"), _STATE_TEXT_LEFT)
_STATE_BOTTOM = _state_bounds(0, 1)[1] - 0.55 - style.caption_height(_STATE_CAPTION)

PORT_STATES = style.Figure(
    _draw_port_states,
    (_STATE_LEFT - 0.45, _STATE_BOTTOM - 0.45,
     max(_STATE_RIGHT, _STATE_TEXT_RIGHT) + 0.45,
     _HEADER_GAP + style.text_height() + 0.45))

# ----------------------------------------------------------------------------------------
# Arduino pin numbers against port bits.
# ----------------------------------------------------------------------------------------
_PIN_W = 1.62
_PIN_H = 1.25
_PIN_COUNT = 14
_PORTD_PINS = 8

_PIN_CAPTION = (
    "Siffrorna på kortet är Arduinos numrering; processorn känner bara till portar och bitar.",
    "Stift 13, med den inbyggda lysdioden, är bit 5 i port B (PB5).")


def _draw_arduino_pins(drawing, ax) -> None:
    for pin in range(_PIN_COUNT):
        left = pin * _PIN_W
        port = "D" if pin < _PORTD_PINS else "B"
        bit = pin if pin < _PORTD_PINS else pin - _PORTD_PINS
        fill = "accent2" if port == "D" else "accent"
        if pin in (0, 1):
            fill = "muted"
        shapes.cell(ax, left, 0.0, _PIN_W, _PIN_H, fill)
        style.text(ax, str(pin), (left + _PIN_W / 2, _PIN_H + 0.16), valign="bottom",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
        style.text(ax, f"P{port}{bit}", (left + _PIN_W / 2, _PIN_H / 2), size=style.SMALL_SIZE)
    shapes.brace(ax, 0.0, 2 * _PIN_W, -0.30, "USB-serie", below=True,
                 color=style.MUTED_COLOR, size=style.TINY_SIZE)
    shapes.brace(ax, 2 * _PIN_W, _PORTD_PINS * _PIN_W, -0.30, "port D, bit 2-7", below=True,
                 color=style.ACCENT_COLOR_2)
    shapes.brace(ax, _PORTD_PINS * _PIN_W, _PIN_COUNT * _PIN_W, -0.30, "port B, bit 0-5",
                 below=True)
    style.caption(ax, _PIN_CAPTION, _PIN_RIGHT / 2, -1.30)


_PIN_RIGHT = _PIN_COUNT * _PIN_W
_PIN_TEXT_LEFT, _PIN_TEXT_RIGHT = style.caption_bounds(_PIN_CAPTION, _PIN_RIGHT / 2)

ARDUINO_PINS = style.Figure(
    _draw_arduino_pins,
    (min(0.0, _PIN_TEXT_LEFT) - 0.45,
     -1.30 - style.caption_height(_PIN_CAPTION) - 0.45,
     max(_PIN_RIGHT, _PIN_TEXT_RIGHT) + 0.45,
     _PIN_H + 0.16 + style.text_height(style.TINY_SIZE) + 0.45))

# ----------------------------------------------------------------------------------------
# The two circuits: an LED on an output, and a button against the internal pull-up.
# ----------------------------------------------------------------------------------------
DEVICE = 3.0
PIN_X = 0.0
LEAD = 1.2
CIRCUIT_MARGIN = 0.55


def _canvas(caption, centre, left, right, top, bottom):
    text_left, text_right = style.caption_bounds(caption, centre)
    return (min(left, text_left) - CIRCUIT_MARGIN,
            bottom - 1.5 - style.caption_height(caption) - CIRCUIT_MARGIN,
            max(right, text_right) + CIRCUIT_MARGIN, top + CIRCUIT_MARGIN)


_LED_CHIP_W = 3.6
_LED_R_X = PIN_X + LEAD
_LED_D_X = _LED_R_X + DEVICE
_LED_G_X = _LED_D_X + DEVICE + LEAD
_LED_TOP = 1.7
_LED_BOTTOM = -0.9
_LED_CAPTION = (
    "En etta i PORTB bit 5 tänder lysdioden, en nolla släcker den. Motståndet begränsar",
    "strömmen; utan det kan både lysdioden och stiftet förstöras.")


def _draw_led(drawing, ax) -> None:
    drawing.add(elm.Resistor().at((_LED_R_X, 0)).right().label("220 Ω", loc="top"))
    drawing.add(elm.LED().at((_LED_D_X, 0)).right().label("lysdiod", loc="top"))
    drawing.add(elm.Line().at((PIN_X, 0)).to((_LED_R_X, 0)))
    drawing.add(elm.Line().at((_LED_D_X + DEVICE, 0)).to((_LED_G_X, 0)))
    drawing.add(elm.Ground().at((_LED_G_X, 0)))
    shapes.dashed_box(ax, PIN_X - _LED_CHIP_W, _LED_BOTTOM, PIN_X, _LED_TOP, "ATmega328P")
    style.text(ax, "PB5", (PIN_X - 0.25, 0.28), halign="right", valign="bottom",
               size=style.SMALL_SIZE)
    style.caption(ax, _LED_CAPTION, (PIN_X - _LED_CHIP_W + _LED_G_X) / 2, _LED_BOTTOM - 1.5)


LED_CIRCUIT = style.Figure(
    _draw_led,
    _canvas(_LED_CAPTION, (PIN_X - _LED_CHIP_W + _LED_G_X) / 2, PIN_X - _LED_CHIP_W,
            _LED_G_X + 0.8, _LED_TOP, _LED_BOTTOM))

_BUTTON_CHIP_W = 5.6
_PULLUP_X = PIN_X - _BUTTON_CHIP_W + 1.7
_PULLUP_TOP = 3.2
_PULLUP_BOTTOM = _PULLUP_TOP - DEVICE
_BUTTON_X = PIN_X + LEAD
_BUTTON_G_X = _BUTTON_X + DEVICE + LEAD
_CHIP_TOP = _PULLUP_TOP + 1.7
_CHIP_BOTTOM = -2.1
_CALLOUT_X = PIN_X - _BUTTON_CHIP_W - 2.3
_BUTTON_CAPTION = (
    "Släppt knapp: pull-upen håller stiftet på 5 V och PIND bit 2 läses som 1.",
    "Nedtryckt knapp: stiftet kortsluts till jord och läses som 0.",
    "En nedtryckt knapp läses alltså som noll (aktivt låg).")


def _draw_button(drawing, ax) -> None:
    drawing.add(elm.Resistor().at((_PULLUP_X, _PULLUP_TOP)).down().color(style.ACCENT_COLOR_2))
    drawing.add(elm.Button().at((_BUTTON_X, 0)).right().label("knapp", loc="top"))
    style.text(ax, "20-50 kΩ", (_PULLUP_X + 0.45, (_PULLUP_TOP + _PULLUP_BOTTOM) / 2),
               halign="left", size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
    drawing.add(elm.Line().at((_PULLUP_X, _PULLUP_BOTTOM)).to((_PULLUP_X, 0))
                .color(style.ACCENT_COLOR_2))
    drawing.add(elm.Line().at((_PULLUP_X, 0)).to((_BUTTON_X, 0)))
    drawing.add(elm.Line().at((_BUTTON_X + DEVICE, 0)).to((_BUTTON_G_X, 0)))
    drawing.add(elm.Ground().at((_BUTTON_G_X, 0)))
    drawing.add(elm.Vdd().at((_PULLUP_X, _PULLUP_TOP)).label("5 V"))
    shapes.dashed_box(ax, PIN_X - _BUTTON_CHIP_W, _CHIP_BOTTOM, PIN_X, _CHIP_TOP, "")
    style.text(ax, "ATmega328P", (PIN_X - _BUTTON_CHIP_W / 2, _CHIP_BOTTOM + 0.42),
               valign="bottom", size=style.SMALL_SIZE, color=style.MUTED_COLOR)
    style.text(ax, "PD2", (PIN_X - 0.25, 0.28), halign="right", valign="bottom",
               size=style.SMALL_SIZE)
    shapes.callout(ax, (_CALLOUT_X, 1.35), (_PULLUP_X - 0.35, 1.8))
    for index, line in enumerate(("slås på med", "PORTD bit 2 = 1", "när DDRD bit 2 = 0")):
        style.text(ax, line, (_CALLOUT_X, 1.15 - index * 0.42), valign="top",
                   size=style.TINY_SIZE, color=style.ACCENT_COLOR)
    style.caption(ax, _BUTTON_CAPTION, (PIN_X - _BUTTON_CHIP_W + _BUTTON_G_X) / 2,
                  _CHIP_BOTTOM - 1.5)


BUTTON_CIRCUIT = style.Figure(
    _draw_button,
    _canvas(_BUTTON_CAPTION, (PIN_X - _BUTTON_CHIP_W + _BUTTON_G_X) / 2, _CALLOUT_X - 2.0,
            _BUTTON_G_X + 0.8, _CHIP_TOP + 0.9, _CHIP_BOTTOM))

# ----------------------------------------------------------------------------------------
# The stack, as snapshots of the bytes at the top of SRAM.
# ----------------------------------------------------------------------------------------
STACK_CELL_W = 3.6
STACK_CELL_H = 0.95
STACK_PANEL_GAP = 3.4
STACK_TOP = 0x08FF


def stack_figure(panels: Sequence[tuple[str, dict[int, tuple[str, str]], int]], rows: int,
                 caption: Sequence[str]) -> style.Figure:
    """Snapshots of the top `rows` bytes of SRAM, side by side, with SP drawn into each.

    Each panel is (title, {address: (text, fill)}, stack pointer address). High addresses are
    at the top, so "the stack grows downwards" is a downward movement on the page too.
    """

    def panel_left(index: int) -> float:
        return index * (STACK_CELL_W + STACK_PANEL_GAP)

    def row_y(address: int) -> tuple[float, float]:
        high = -(STACK_TOP - address) * STACK_CELL_H
        return high - STACK_CELL_H, high

    left_edge = -0.32 - style.text_width("0x08FF", style.TINY_SIZE)
    right_edge = (panel_left(len(panels) - 1) + STACK_CELL_W + 0.35 + 1.15 + 0.25
                  + style.text_width("SP", style.SMALL_SIZE))
    centre = (left_edge + right_edge) / 2
    bottom = row_y(STACK_TOP - rows + 1)[0]

    def draw(drawing, ax) -> None:
        for index, (title, contents, pointer) in enumerate(panels):
            left = panel_left(index)
            style.text(ax, title, (left + STACK_CELL_W / 2, 0.55), valign="bottom",
                       size=style.SMALL_SIZE)
            for row in range(rows):
                address = STACK_TOP - row
                low, high = row_y(address)
                text, fill = contents.get(address, ("", "plain"))
                shapes.cell(ax, left, low, STACK_CELL_W, STACK_CELL_H, fill)
                if text:
                    colour = style.MUTED_COLOR if fill == "muted" else style.LINE_COLOR
                    style.text(ax, text, (left + STACK_CELL_W / 2, (low + high) / 2),
                               size=style.SMALL_SIZE, color=colour)
                if index == 0:
                    style.text(ax, f"0x{address:04X}", (left - 0.32, (low + high) / 2),
                               halign="right", size=style.TINY_SIZE, color=style.MUTED_COLOR)
            low, high = row_y(pointer)
            middle = (low + high) / 2
            shapes.arrow(ax, (left + STACK_CELL_W + 0.35 + 1.15, middle),
                         (left + STACK_CELL_W + 0.35, middle), color=style.ACCENT_COLOR_2)
            style.text(ax, "SP", (left + STACK_CELL_W + 0.35 + 1.15 + 0.25, middle),
                       halign="left", size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
        style.caption(ax, caption, centre, bottom - 0.75)

    text_left, text_right = style.caption_bounds(caption, centre)
    return style.Figure(draw, (min(left_edge, text_left) - 0.5,
                               bottom - 0.75 - style.caption_height(caption) - 0.5,
                               max(right_edge, text_right) + 0.5,
                               0.55 + style.text_height(style.SMALL_SIZE) + 0.5))


CALL_STACK = stack_figure(
    [
        ("Före rcall", {}, 0x08FF),
        ("I subrutinen", {0x08FF: ("returadr. låg", "accent"),
                          0x08FE: ("returadr. hög", "accent")}, 0x08FD),
        ("Efter ret", {0x08FF: ("returadr. låg", "muted"),
                       0x08FE: ("returadr. hög", "muted")}, 0x08FF),
    ],
    rows=4,
    caption=("rcall lägger returadressen på stacken och SP flyttas två steg nedåt.",
             "ret hämtar tillbaka adressen och flyttar SP uppåt igen. Bytena raderas inte,",
             "de är bara inte längre någons: nästa rcall eller push skriver över dem."))

FIGURES = {
    "avr_register_file": (REGISTER_FILE, [paths.lecture("L07") / "register_file.png"]),
    "avr_sreg": (SREG, [paths.lecture("L07") / "sreg.png", paths.lecture("L08") / "sreg.png"]),
    "avr_memory_spaces": (MEMORY_SPACES, [paths.lecture("L07") / "memory_spaces.png"]),
    "avr_ldi_encoding": (LDI_ENCODING, [paths.lecture("L07") / "ldi_encoding.png"]),
    "avr_toolchain": (TOOLCHAIN, [paths.lecture("L07") / "toolchain.png"]),
    "avr_port_states": (PORT_STATES, [paths.lecture("L08") / "port_states.png"]),
    "avr_arduino_pins": (ARDUINO_PINS, [paths.lecture("L08") / "arduino_pins.png",
                                    paths.lecture("L11") / "arduino_pins.png"]),
    "avr_led_circuit": (LED_CIRCUIT, [paths.lecture("L08") / "led_circuit.png",
                                  paths.lecture("L11") / "led_circuit.png"]),
    "avr_button_circuit": (BUTTON_CIRCUIT, [paths.lecture("L10") / "button_circuit.png",
                                        paths.lecture("L11") / "button_circuit.png"]),
    "avr_call_stack": (CALL_STACK, [paths.lecture("L10") / "call_stack.png"]),
}
