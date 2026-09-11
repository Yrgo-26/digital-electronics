"""L07 figures: what one line of assembly consists of, and the loop you work in.

The AVR figures L07 also embeds (the register file, SREG, the memories, an encoded `ldi`, the
toolchain) are drawn by avr.py and shared with later lectures.
"""

from __future__ import annotations

import flow
import paths
import shapes
import style

# ----------------------------------------------------------------------------------------
# B.2: one line of assembly, taken apart.
#
# The line is set in the monospace font the whole figure uses, so a column of characters is a
# fixed width and each part can be braced by counting characters rather than by guessing.
# ----------------------------------------------------------------------------------------
_LINE = "loop:   inc r16          ; count up"
_PARTS = (
    # (first character, last character, label, colour, level): level 1 hangs lower, so the two
    # neighbouring labels "instruktion" and "operand" never share a baseline.
    (0, 4, "etikett", style.ACCENT_COLOR_2, 0),
    (8, 10, "instruktion", style.ACCENT_COLOR, 0),
    (12, 14, "operand", style.ACCENT_COLOR_2, 1),
    (25, 34, "kommentar", style.MUTED_COLOR, 0),
)
_SIZE = 20
_CHAR = style.text_width("x", _SIZE)
_LINE_CAPTION = (
    "Etiketten namnger adressen, instruktionen säger vad processorn ska göra, operanden",
    "säger med vad, och kommentaren är till för människor: assemblern hoppar över den.")


def _draw_line(drawing, ax) -> None:
    width = len(_LINE) * _CHAR
    shapes.cell(ax, -0.3, -0.55, width + 0.6, 1.1, "plain", lw=style.CELL_WIDTH)
    style.text(ax, _LINE, (0.0, 0.0), halign="left", size=_SIZE)
    for first, last, label, colour, level in _PARTS:
        shapes.brace(ax, first * _CHAR, (last + 1) * _CHAR, -0.85 - 0.85 * level, label,
                     below=True, color=colour, size=style.SMALL_SIZE)
    style.caption(ax, _LINE_CAPTION, width / 2, -2.75)


_LINE_WIDTH = len(_LINE) * _CHAR
_LINE_LEFT, _LINE_RIGHT = style.caption_bounds(_LINE_CAPTION, _LINE_WIDTH / 2)

LINE_ANATOMY = style.Figure(
    _draw_line,
    (min(-0.3, _LINE_LEFT) - 0.45, -2.75 - style.caption_height(_LINE_CAPTION) - 0.45,
     max(_LINE_WIDTH + 0.3, _LINE_RIGHT) + 0.45, 0.55 + 0.45))

# ----------------------------------------------------------------------------------------
# C.1: the loop you work in, from writing a line to checking what it did.
# ----------------------------------------------------------------------------------------
WORKFLOW = flow.figure(
    [
        flow.Node("Skriv", (0.0, 0.0), "ändra main.asm", "accent2", width=4.4),
        flow.Node("Bygg (F7)", (6.4, 0.0), "assemblera", width=4.4),
        flow.Node("Förutsäg", (12.8, 0.0), "skriv ned vad du väntar dig", width=5.4),
        flow.Node("Stega (F11)", (12.8, -3.4), "en instruktion i taget", width=5.4),
        flow.Node("Jämför", (0.0, -3.4), "register, flaggor, portar", "accent", width=5.0),
        flow.Node("Error List", (6.4, 3.2), "rätta första felet", "muted", width=4.4),
    ],
    [
        flow.Edge(0, 1),
        flow.Edge(1, 2, label="0 fel", label_offset=(0.0, 0.24)),
        flow.Edge(1, 5, label="fel", dashed=True, label_offset=(0.45, -0.2)),
        flow.Edge(5, 0, dashed=True),
        flow.Edge(2, 3),
        flow.Edge(3, 4),
        flow.Edge(4, 0, label="stämmer inte", dashed=True, label_offset=(1.25, -0.2)),
    ],
    caption=("Förutsäg före varje steg. En skillnad mellan det du väntade dig och det",
             "simulatorn visar är inget misslyckande: den visar var felet sitter."))

FIGURES = {
    "l07_line_anatomy": (LINE_ANATOMY, [paths.lecture("L07") / "line_anatomy.png"]),
    "l07_workflow": (WORKFLOW, [paths.lecture("L07") / "workflow.png"]),
}
