"""L10 figures: a 16-bit register pair, a nibble becoming a character, and the stack at work.

The stack snapshots use `avr.stack_figure`, and every value in them was read out of the
simulator running the L10 examples: blink_subroutine.asm for the call into delay_ms, and
push_pop.asm for the swap.
"""

from __future__ import annotations

import avr
import flow
import paths
import shapes
import style

# ----------------------------------------------------------------------------------------
# A.2: two registers read as one 16-bit number.
# ----------------------------------------------------------------------------------------
_PAIR_W = 3.6
_PAIR_H = 1.2
_PAIR_CAPTION = ("Registerparet r25:r24 är ett 16-bitars tal. r25 är den höga byten och r24",
                 "den låga: 0x03 x 256 + 0xE8 = 768 + 232 = 1000.")


def _draw_pair(drawing, ax) -> None:
    for index, (name, value, role) in enumerate((("r25", "0x03", "hög byte"),
                                                 ("r24", "0xE8", "låg byte"))):
        left = index * _PAIR_W
        shapes.cell(ax, left, 0.0, _PAIR_W, _PAIR_H, "accent" if index else "accent2")
        style.text(ax, value, (left + _PAIR_W / 2, _PAIR_H / 2))
        style.text(ax, name, (left + _PAIR_W / 2, _PAIR_H + 0.25), valign="bottom",
                   size=style.SMALL_SIZE)
        style.text(ax, role, (left + _PAIR_W / 2, -0.25), valign="top",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
        style.text(ax, "bit 15-8" if index == 0 else "bit 7-0",
                   (left + _PAIR_W / 2, _PAIR_H + 0.85), valign="bottom",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
    shapes.brace(ax, 0.0, 2 * _PAIR_W, -0.95, "r25:r24 = 0x03E8 = 1000", below=True,
                 size=style.SMALL_SIZE)
    style.caption(ax, _PAIR_CAPTION, _PAIR_W, -2.25)


_PAIR_LEFT, _PAIR_RIGHT = style.caption_bounds(_PAIR_CAPTION, _PAIR_W)
REGISTER_PAIR = style.Figure(
    _draw_pair,
    (min(0.0, _PAIR_LEFT) - 0.5, -2.25 - style.caption_height(_PAIR_CAPTION) - 0.5,
     max(2 * _PAIR_W, _PAIR_RIGHT) + 0.5, _PAIR_H + 1.55))

# ----------------------------------------------------------------------------------------
# A.1: one byte, two nibbles, two characters.
# ----------------------------------------------------------------------------------------
NIBBLES = flow.figure(
    [
        flow.Node("r16 = 0x3C", (0.0, 0.0), "byten som ska skrivas", "accent2", width=4.4),
        flow.Node("0x03", (6.2, 1.5), "swap, andi 0x0F", width=4.4),
        flow.Node("0x0C", (6.2, -1.5), "andi 0x0F", width=4.4),
        flow.Node("0x33 = '3'", (12.8, 1.5), "0-9: + 0x30", "accent", width=4.6),
        flow.Node("0x43 = 'C'", (12.8, -1.5), "A-F: + 7 + 0x30", "accent", width=4.6),
    ],
    [flow.Edge(0, 1, "hög halva", label_offset=(-0.2, 0.3)),
     flow.Edge(0, 2, "låg halva", label_offset=(-0.2, -0.3)),
     flow.Edge(1, 3), flow.Edge(2, 4)],
    caption=("Varje hexadecimal siffra är fyra bitar. En byte blir två tecken: först delas",
             "den i två halvor, sedan blir varje halva sitt ASCII-tecken."))

# ----------------------------------------------------------------------------------------
# C.4: the stack during a call of delay_ms, from blink_subroutine.asm.
# ----------------------------------------------------------------------------------------
STACK_IN_DELAY = avr.stack_figure(
    [
        ("Före rcall", {}, 0x08FF),
        ("Efter rcall", {0x08FF: ("0x0C  ret. låg", "accent"),
                         0x08FE: ("0x00  ret. hög", "accent")}, 0x08FD),
        ("Efter tre push", {0x08FF: ("0x0C  ret. låg", "accent"),
                            0x08FE: ("0x00  ret. hög", "accent"),
                            0x08FD: ("0xFA  r24", "accent2"),
                            0x08FC: ("0x00  r26", "accent2"),
                            0x08FB: ("0x00  r27", "accent2")}, 0x08FA),
        ("Efter pop och ret", {0x08FF: ("0x0C  ret. låg", "muted"),
                               0x08FE: ("0x00  ret. hög", "muted"),
                               0x08FD: ("0xFA  r24", "muted"),
                               0x08FC: ("0x00  r26", "muted"),
                               0x08FB: ("0x00  r27", "muted")}, 0x08FF),
    ],
    rows=6,
    caption=("rcall lägger returadressen 0x000C på stacken, och delay_ms sparar sedan tre",
             "register ovanpå den. Tre pop och en ret tar bort dem i omvänd ordning, och SP",
             "står där den stod före anropet. Bytena ligger kvar, men är inte längre någons."))

# ----------------------------------------------------------------------------------------
# C.5: last in, first out, from push_pop.asm.
# ----------------------------------------------------------------------------------------
PUSH_POP = avr.stack_figure(
    [
        ("Före", {}, 0x08FF),
        ("push r16, push r17", {0x08FF: ("0x11  (r16)", "accent"),
                                0x08FE: ("0x22  (r17)", "accent")}, 0x08FD),
        ("pop r16", {0x08FF: ("0x11", "accent"), 0x08FE: ("0x22", "muted")}, 0x08FE),
        ("pop r17", {0x08FF: ("0x11", "muted"), 0x08FE: ("0x22", "muted")}, 0x08FF),
    ],
    rows=4,
    caption=("Det som lades på stacken sist tas av först. pop r16 får alltså 0x22, som kom",
             "från r17, och pop r17 får 0x11: de två registren har bytt värden."))

FIGURES = {
    "l10_register_pair": (REGISTER_PAIR, [paths.lecture("L10") / "register_pair.png"]),
    "l10_nibbles": (NIBBLES, [paths.lecture("L10") / "nibbles.png"]),
    "l10_stack_in_delay": (STACK_IN_DELAY, [paths.lecture("L10") / "stack_in_delay.png"]),
    "l10_push_pop": (PUSH_POP, [paths.lecture("L10") / "push_pop.png"]),
}
