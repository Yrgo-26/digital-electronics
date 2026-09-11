"""L01 figures: what a bit is worth, how four bits become one hex digit, and a 7-segment display.

All three are drawn as cells, because a binary number on paper is a row of positions, and the
point of every one of these figures is what a position is worth.
"""

from __future__ import annotations

from matplotlib.patches import Polygon

import paths
import shapes
import style

CELL_W = 1.45
CELL_H = 1.1
MARGIN = 0.45

# ----------------------------------------------------------------------------------------
# A.3: the weights of an 8-bit number, with 1010 1110 = 174 filled in.
# ----------------------------------------------------------------------------------------
_BITS = "10101110"
_WEIGHT_CAPTION = ("1010 1110 = 128 + 32 + 8 + 4 + 2 = 174",
                   "Varje position är värd dubbelt så mycket som positionen till höger om den.")


def _draw_weights(d, ax) -> None:
    for index, bit in enumerate(_BITS):
        position = 7 - index
        left = index * CELL_W
        fill = "accent" if bit == "1" else "plain"
        shapes.cell(ax, left, 0.0, CELL_W, CELL_H, fill)
        style.text(ax, bit, (left + CELL_W / 2, CELL_H / 2))
        style.text(ax, f"bit {position}", (left + CELL_W / 2, CELL_H + 0.2), valign="bottom",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
        style.text(ax, f"2^{position}", (left + CELL_W / 2, -0.25), valign="top",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
        colour = style.ACCENT_COLOR if bit == "1" else style.MUTED_COLOR
        style.text(ax, str(2 ** position), (left + CELL_W / 2, -0.75), valign="top",
                   size=style.SMALL_SIZE, color=colour)
    style.text(ax, "MSB", (CELL_W / 2, CELL_H + 0.75), valign="bottom", size=style.TINY_SIZE)
    style.text(ax, "LSB", (7.5 * CELL_W, CELL_H + 0.75), valign="bottom", size=style.TINY_SIZE)
    style.text(ax, "vikt:", (-0.3, -1.0), halign="right", size=style.SMALL_SIZE,
               color=style.MUTED_COLOR)
    style.caption(ax, _WEIGHT_CAPTION, 4 * CELL_W, -1.85)


_W_LEFT, _W_RIGHT = style.caption_bounds(_WEIGHT_CAPTION, 4 * CELL_W)
BIT_WEIGHTS = style.Figure(
    _draw_weights,
    (min(-1.5, _W_LEFT) - MARGIN, -1.85 - style.caption_height(_WEIGHT_CAPTION) - MARGIN,
     max(8 * CELL_W, _W_RIGHT) + MARGIN, CELL_H + 1.2 + MARGIN))

# ----------------------------------------------------------------------------------------
# A.5: 1011 0110 grouped into nibbles, B and 6.
# ----------------------------------------------------------------------------------------
_HEX_BITS = "10110110"
_HEX_CAPTION = ("Fyra bitar är exakt en hexadecimal siffra.",
                "Därför är 1011 0110 (binärt) = B6 (hexadecimalt) = 182 (decimalt).")


def _draw_hex(d, ax) -> None:
    gap = 0.5
    for index, bit in enumerate(_HEX_BITS):
        left = index * CELL_W + (gap if index >= 4 else 0.0)
        fill = "accent2" if index < 4 else "accent"
        shapes.cell(ax, left, 0.0, CELL_W, CELL_H, fill)
        style.text(ax, bit, (left + CELL_W / 2, CELL_H / 2))
        style.text(ax, str(2 ** (3 - index % 4)), (left + CELL_W / 2, CELL_H + 0.2),
                   valign="bottom", size=style.TINY_SIZE, color=style.MUTED_COLOR)
    shapes.brace(ax, 0.0, 4 * CELL_W, -0.3, "8 + 2 + 1 = 11 = B", below=True,
                 color=style.ACCENT_COLOR_2)
    shapes.brace(ax, 4 * CELL_W + gap, 8 * CELL_W + gap, -0.3, "4 + 2 = 6", below=True)
    style.caption(ax, _HEX_CAPTION, (8 * CELL_W + gap) / 2, -1.45)


_H_CENTRE = (8 * CELL_W + 0.5) / 2
_H_LEFT, _H_RIGHT = style.caption_bounds(_HEX_CAPTION, _H_CENTRE)
HEX_GROUPING = style.Figure(
    _draw_hex,
    (min(0.0, _H_LEFT) - MARGIN, -1.45 - style.caption_height(_HEX_CAPTION) - MARGIN,
     max(8 * CELL_W + 0.5, _H_RIGHT) + MARGIN, CELL_H + 0.7 + MARGIN))

# ----------------------------------------------------------------------------------------
# B.5: a 7-segment display, labelled, beside the digit 5 lit.
# ----------------------------------------------------------------------------------------
_SEG_L = 2.2    # Segment length.
_SEG_T = 0.42   # Segment thickness.


def _segment(ax, centre, horizontal: bool, lit: bool) -> None:
    x, y = centre
    half, t = _SEG_L / 2, _SEG_T / 2
    if horizontal:
        points = [(x - half, y), (x - half + t, y + t), (x + half - t, y + t), (x + half, y),
                  (x + half - t, y - t), (x - half + t, y - t)]
    else:
        points = [(x, y - half), (x + t, y - half + t), (x + t, y + half - t), (x, y + half),
                  (x - t, y + half - t), (x - t, y - half + t)]
    ax.add_patch(Polygon(points, closed=True,
                         facecolor=style.ACCENT_COLOR if lit else style.FILLS["muted"],
                         edgecolor=style.LINE_COLOR, lw=style.CELL_WIDTH, zorder=2))


def _segments(origin):
    """Centre and orientation of segments a to g, for a display whose middle is `origin`."""
    x, y = origin
    h = _SEG_L / 2 + 0.08
    return {
        "a": ((x, y + 2 * h), True), "b": ((x + h, y + h), False),
        "c": ((x + h, y - h), False), "d": ((x, y - 2 * h), True),
        "e": ((x - h, y - h), False), "f": ((x - h, y + h), False),
        "g": ((x, y), True),
    }


def _draw_display(ax, origin, lit: str, labels: bool) -> None:
    for name, (centre, horizontal) in _segments(origin).items():
        _segment(ax, centre, horizontal, name in lit)
        if labels:
            offset = (0.0, 0.55) if horizontal else (0.55 if centre[0] > origin[0] else -0.55,
                                                       0.0)
            if name == "g":
                offset = (0.0, 0.55)
            if name == "d":
                offset = (0.0, -0.55)
            style.text(ax, name, (centre[0] + offset[0], centre[1] + offset[1]),
                       size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2, weight="bold")


_SEG_CAPTION = ("Sju segment, a till g, som tänds var för sig. Till höger siffran 5:",
                "segmenten a, c, d, f och g tända, alltså koden gfedcba = 1101101.")


def _draw_seven_segment(d, ax) -> None:
    _draw_display(ax, (0.0, 0.0), "", labels=True)
    _draw_display(ax, (5.0, 0.0), "acdfg", labels=False)
    style.caption(ax, _SEG_CAPTION, 2.5, -3.6)


_S_LEFT, _S_RIGHT = style.caption_bounds(_SEG_CAPTION, 2.5)
SEVEN_SEGMENT = style.Figure(
    _draw_seven_segment,
    (min(-2.2, _S_LEFT) - MARGIN, -3.6 - style.caption_height(_SEG_CAPTION) - MARGIN,
     max(7.2, _S_RIGHT) + MARGIN, 3.0 + MARGIN))

FIGURES = {
    "l01_bit_weights": (BIT_WEIGHTS, [paths.lecture("L01") / "bit_weights.png"]),
    "l01_hex_grouping": (HEX_GROUPING, [paths.lecture("L01") / "hex_grouping.png"]),
    "l01_seven_segment": (SEVEN_SEGMENT, [paths.lecture("L01") / "seven_segment.png"]),
}
