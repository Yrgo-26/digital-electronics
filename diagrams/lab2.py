"""Labb 2 figures: a gate network drawn as it is wired, with circuit names and pin numbers.

The lecture figures show networks as logic. On the breadboard every gate is a particular gate in a
particular circuit, and every wire runs between two pin numbers. This figure is the bridge: the same
network as L04's X = AB + C, annotated the way the wiring list in L04 Appendix B.7 reads it.
"""

from __future__ import annotations

import gates
import paths
import shapes
import style

LAB2 = paths.lab("lab2")


def _pin(ax, point, number: str, above: bool = True, left: bool = False) -> None:
    """A pin number just beside a gate pin."""
    x, y = point
    style.text(ax, number, (x + (-0.12 if left else 0.12), y + (0.12 if above else -0.12)),
               halign="right" if left else "left", valign="bottom" if above else "top",
               size=style.TINY_SIZE, color=style.ACCENT_COLOR)


def _draw_wiring(d, ax) -> None:
    u1 = gates.ansi(d, "and", (4.2, 1.0))
    u2 = gates.ansi(d, "or", (8.6, 0.45))
    # Inputs from the station's switches.
    for (x, y), name in zip(u1.inputs, ("A", "B")):
        gates.wire(ax, [(0.6, y), (x, y)])
        style.text(ax, name, (0.4, y), halign="right")
    gates.wire(ax, [(0.6, u2.inputs[1][1]), u2.inputs[1]])
    style.text(ax, "C", (0.4, u2.inputs[1][1]), halign="right")
    # U1 output to U2 input 1.
    gates.wire(ax, [u1.out, (5.4, u1.out[1]), (5.4, u2.inputs[0][1]), u2.inputs[0]])
    # U2 output to the LED.
    gates.wire(ax, [u2.out, (9.6, u2.out[1])])
    style.text(ax, "X, till lysdiod", (9.8, u2.out[1]), halign="left", size=style.SMALL_SIZE)

    _pin(ax, u1.inputs[0], "1", left=True)
    _pin(ax, u1.inputs[1], "2", above=False, left=True)
    _pin(ax, u1.out, "3")
    _pin(ax, u2.inputs[0], "1", left=True)
    _pin(ax, u2.inputs[1], "2", above=False, left=True)
    _pin(ax, u2.out, "3")

    shapes.dashed_box(ax, 1.7, 0.24, 4.7, 2.75, "U1: 74HC08")
    shapes.dashed_box(ax, 6.0, -0.75, 9.1, 2.2, "U2: 74HC32")
    style.caption(ax, _CAPTION, 6.0, -1.3)


_CAPTION = ("Röda siffror är bennummer. Båda kretsarna har dessutom VCC på ben 14",
            "och GND på ben 7, och ingångarna på de oanvända grindarna kopplade till GND.")
_LEFT, _RIGHT = style.caption_bounds(_CAPTION, 6.0)
WIRING = style.Figure(_draw_wiring, (min(-0.7, _LEFT - 0.4), -2.6, max(13.2, _RIGHT + 0.4), 3.4))

FIGURES = {
    "lab2_wiring_and_or": (WIRING, [LAB2 / "wiring_and_or.png"]),
}
