"""L08 figures: a byte as a circle, the five shifts and rotations, and three masks.

The AVR figures L08 also embeds (SREG, the port states, the Arduino pin map, the LED) are drawn
by avr.py and shared with other lectures.
"""

from __future__ import annotations

import math

from matplotlib.patches import Circle, FancyArrowPatch

import bitfield
import paths
import shapes
import style
from bitfield import Bit, Register

# ----------------------------------------------------------------------------------------
# A.3 and A.5: the 256 values of a byte as a circle, read unsigned outside and signed inside.
# ----------------------------------------------------------------------------------------
_R = 3.6            # Radius of the circle.
_OUTER = 4.35       # Radius of the unsigned labels.
_INNER = 2.75       # Radius of the signed labels.
_TICKS = range(0, 256, 32)


def _angle(value: int) -> float:
    """Clockwise from the top, the way a dial is read."""
    return math.radians(90.0 - value / 256.0 * 360.0)


def _point(value: float, radius: float) -> tuple[float, float]:
    a = _angle(value)
    return radius * math.cos(a), radius * math.sin(a)


_CIRCLE_CAPTION = (
    "Ytterst: byten läst utan tecken, 0 till 255. Innerst: samma byte läst med tecken,",
    "-128 till 127. Ett steg medurs är inc, ett steg moturs är dec.")


def _draw_circle(drawing, ax) -> None:
    ax.add_patch(Circle((0, 0), _R, facecolor="none", edgecolor=style.LINE_COLOR,
                        lw=style.BOX_WIDTH))
    for value in _TICKS:
        x0, y0 = _point(value, _R - 0.18)
        x1, y1 = _point(value, _R + 0.18)
        ax.plot([x0, x1], [y0, y1], color=style.LINE_COLOR, lw=style.WIRE_WIDTH)
        signed = value - 256 if value >= 128 else value
        style.text(ax, str(value), _point(value, _OUTER), size=style.SMALL_SIZE)
        style.text(ax, str(signed), _point(value, _INNER), size=style.SMALL_SIZE,
                   color=style.ACCENT_COLOR_2 if value >= 128 else style.MUTED_COLOR)
    # The two places where something happens: an arc across each, clockwise like inc.
    ax.add_patch(FancyArrowPatch(_point(248, _R + 1.25), _point(8, _R + 1.25),
                                 connectionstyle="arc3,rad=-0.2", arrowstyle="-|>",
                                 mutation_scale=14, color=style.ACCENT_COLOR,
                                 lw=style.ACCENT_WIDTH))
    style.text(ax, "255 + 1 = 0  (C = 1 med add)", (0, _R + 1.95), size=style.SMALL_SIZE,
               color=style.ACCENT_COLOR)
    ax.add_patch(FancyArrowPatch(_point(120, _R + 1.25), _point(136, _R + 1.25),
                                 connectionstyle="arc3,rad=-0.2", arrowstyle="-|>",
                                 mutation_scale=14, color=style.ACCENT_COLOR_2,
                                 lw=style.ACCENT_WIDTH))
    style.text(ax, "127 + 1 = 128, men med tecken +127 + 1 = -128  (V = 1)",
               (0, -_R - 1.95), size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
    style.caption(ax, _CIRCLE_CAPTION, 0.0, -_R - 2.6)


_CIRCLE_LEFT, _CIRCLE_RIGHT = style.caption_bounds(_CIRCLE_CAPTION, 0.0)
NUMBER_CIRCLE = style.Figure(
    _draw_circle,
    (min(-_OUTER - 1.0, _CIRCLE_LEFT) - 0.45,
     -_R - 2.6 - style.caption_height(_CIRCLE_CAPTION) - 0.45,
     max(_OUTER + 1.0, _CIRCLE_RIGHT) + 0.45, _R + 2.5))

# ----------------------------------------------------------------------------------------
# B.3 and B.4: lsl, lsr, asr, rol and ror, one row each.
#
# The carry flag sits on the side the bit falls out of. Arrows show the two ends, which is
# where the five instructions differ; in the middle, every bit moves one place, in all five.
# ----------------------------------------------------------------------------------------
_CELL = 0.95
_ROW = 2.35
_C_GAP = 0.9
_BITS = [str(b) for b in range(7, -1, -1)]
_SHIFTS = (
    # (name, direction, what enters, description)
    ("lsl", "left", "0", "skifta vänster: x 2"),
    ("rol", "left", "C", "rotera vänster genom C"),
    ("lsr", "right", "0", "skifta höger: / 2 utan tecken"),
    ("asr", "right", "bit7", "skifta höger: / 2 med tecken"),
    ("ror", "right", "C", "rotera höger genom C"),
)
_REG_W = 8 * _CELL


def _arrow(ax, start, end, colour=style.ACCENT_COLOR, rad=0.0) -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                                 connectionstyle=f"arc3,rad={rad}", color=colour,
                                 lw=style.ACCENT_WIDTH, shrinkA=0, shrinkB=0, zorder=4))


def _draw_shifts(drawing, ax) -> None:
    for row, (name, direction, enters, text) in enumerate(_SHIFTS):
        y = -row * _ROW
        style.text(ax, name, (-_C_GAP - _CELL - 0.9, y + _CELL / 2), halign="right",
                   weight="bold")
        style.text(ax, text, (_REG_W / 2, y + _CELL + 0.45), size=style.TINY_SIZE,
                   color=style.MUTED_COLOR)
        for index, label in enumerate(_BITS):
            shapes.cell(ax, index * _CELL, y, _CELL, _CELL, "plain", lw=style.CELL_WIDTH)
            style.text(ax, label, ((index + 0.5) * _CELL, y + _CELL / 2),
                       size=style.TINY_SIZE, color=style.MUTED_COLOR)
        mid = y + _CELL / 2
        if direction == "left":
            cx = -_C_GAP - _CELL
            shapes.cell(ax, cx, y, _CELL, _CELL, "accent2")
            style.text(ax, "C", (cx + _CELL / 2, mid), size=style.SMALL_SIZE)
            _arrow(ax, (0.0, mid), (cx + _CELL, mid))
            if enters == "0":
                style.text(ax, "0", (_REG_W + 0.95, mid), size=style.SMALL_SIZE,
                           color=style.ACCENT_COLOR)
                _arrow(ax, (_REG_W + 0.7, mid), (_REG_W, mid))
            else:
                # C back round underneath into bit 0.
                low = y - 0.35
                ax.plot([cx + _CELL / 2, cx + _CELL / 2, _REG_W + 0.5, _REG_W + 0.5],
                        [y, low, low, mid], color=style.ACCENT_COLOR_2, lw=style.ACCENT_WIDTH)
                _arrow(ax, (_REG_W + 0.5, mid), (_REG_W, mid), style.ACCENT_COLOR_2)
        else:
            cx = _REG_W + _C_GAP
            shapes.cell(ax, cx, y, _CELL, _CELL, "accent2")
            style.text(ax, "C", (cx + _CELL / 2, mid), size=style.SMALL_SIZE)
            _arrow(ax, (_REG_W, mid), (cx, mid))
            if enters == "0":
                style.text(ax, "0", (-0.95, mid), size=style.SMALL_SIZE,
                           color=style.ACCENT_COLOR)
                _arrow(ax, (-0.7, mid), (0.0, mid))
            elif enters == "bit7":
                # Bit 7 is copied back into itself: the sign stays.
                ax.plot([_CELL * 0.5, _CELL * 0.5], [y, y - 0.35], color=style.ACCENT_COLOR,
                        lw=style.ACCENT_WIDTH)
                ax.plot([_CELL * 0.5, -0.5, -0.5], [y - 0.35, y - 0.35, mid],
                        color=style.ACCENT_COLOR, lw=style.ACCENT_WIDTH)
                _arrow(ax, (-0.5, mid), (0.0, mid))
            else:
                low = y - 0.35
                ax.plot([cx + _CELL / 2, cx + _CELL / 2, -0.5, -0.5], [y, low, low, mid],
                        color=style.ACCENT_COLOR_2, lw=style.ACCENT_WIDTH)
                _arrow(ax, (-0.5, mid), (0.0, mid), style.ACCENT_COLOR_2)
    bottom = -(len(_SHIFTS) - 1) * _ROW - 0.35
    style.caption(ax, _SHIFT_CAPTION, _REG_W / 2, bottom - 0.6)


_SHIFT_CAPTION = (
    "I alla fem flyttas varje bit ett steg. Det som skiljer är ändarna: vad som skiftas in,",
    "och att biten som skiftas ut alltid hamnar i carryflaggan C.")
_SHIFT_LEFT, _SHIFT_RIGHT = style.caption_bounds(_SHIFT_CAPTION, _REG_W / 2)
_SHIFT_BOTTOM = -(len(_SHIFTS) - 1) * _ROW - 0.35 - 0.6 - style.caption_height(_SHIFT_CAPTION)

SHIFTS = style.Figure(
    _draw_shifts,
    (min(-_C_GAP - _CELL - 0.9 - style.text_width("lsl"), _SHIFT_LEFT) - 0.45,
     _SHIFT_BOTTOM - 0.45, max(_REG_W + _C_GAP + _CELL, _SHIFT_RIGHT) + 0.45,
     _CELL + 0.45 + style.text_height(style.TINY_SIZE) + 0.45))

# ----------------------------------------------------------------------------------------
# B.2: three masks on the same byte. The bits the mask acts on are tinted, in the mask and in
# the result, so the reader sees which bits changed and which were left alone.
# ----------------------------------------------------------------------------------------
_VALUE = "10110110"


def _row(name: str, bits: str, active: set[int], fill: str) -> Register:
    """One row of cells. `active` holds bit numbers (7 is the leftmost cell)."""
    return Register(name, [Bit(b, fill if (7 - i) in active else "plain")
                           for i, b in enumerate(bits)])


def _mask_figure(operation: str, mask: str, active: set[int], result: str,
                 caption: tuple[str, ...]) -> style.Figure:
    return bitfield.figure(
        [_row("r16", _VALUE, set(), "plain"),
         _row(operation, mask, active, "accent2"),
         _row("resultat", result, active, "accent")],
        caption=caption)


MASK_AND = _mask_figure(
    "mask", "00001111", {4, 5, 6, 7}, "00000110",
    ("AND med en nolla i masken nollställer biten; en etta låter den vara.",
     "andi r16, 0b00001111 nollställer de fyra övre bitarna."))

MASK_OR = _mask_figure(
    "mask", "10000001", {0, 7}, "10110111",
    ("OR med en etta i masken ettställer biten; en nolla låter den vara.",
     "ori r16, 0b10000001 ettställer bit 7 och bit 0."))

MASK_EOR = _mask_figure(
    "mask", "11000000", {6, 7}, "01110110",
    ("XOR med en etta i masken inverterar biten; en nolla låter den vara.",
     "eor med 0b11000000 inverterar bit 7 och bit 6."))

FIGURES = {
    "l08_number_circle": (NUMBER_CIRCLE, [paths.lecture("L08") / "number_circle.png"]),
    "l08_shifts": (SHIFTS, [paths.lecture("L08") / "shifts.png"]),
    "l08_mask_and": (MASK_AND, [paths.lecture("L08") / "mask_and.png"]),
    "l08_mask_or": (MASK_OR, [paths.lecture("L08") / "mask_or.png"]),
    "l08_mask_eor": (MASK_EOR, [paths.lecture("L08") / "mask_eor.png"]),
}
