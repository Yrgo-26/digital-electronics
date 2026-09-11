"""L12 figures: the gate network the review exercises ask you to analyse."""

from __future__ import annotations

import gates
import paths
import style

_CAPTION = ("Analysera nätet: skriv uttrycket för X, gör sanningstabellen och",
            "säg vilken enda grind som gör samma sak.")


def _draw_review(drawing, ax) -> None:
    nor = gates.ansi(drawing, "nor", (4.0, 1.6))
    both = gates.ansi(drawing, "and", (4.0, -0.6))
    out = gates.ansi(drawing, "or", (8.0, 0.5))
    a_y, b_y = nor.inputs[0][1], nor.inputs[1][1]
    # A and B each feed both gates: a vertical wire per input, with a dot where it branches.
    xa, xb = 0.6, 1.3
    for x, y_top, y_bottom, name in ((xa, a_y, both.inputs[0][1], "A"),
                                     (xb, b_y, both.inputs[1][1], "B")):
        gates.wire(ax, [(-0.4, y_top), (nor.inputs[0][0], y_top)])
        gates.wire(ax, [(x, y_top), (x, y_bottom), (both.inputs[0][0], y_bottom)])
        gates.dot(ax, (x, y_top))
        style.text(ax, name, (-0.6, y_top), halign="right")
    gates.wire(ax, [nor.out, (5.2, nor.out[1]), (5.2, out.inputs[0][1]), out.inputs[0]])
    gates.wire(ax, [both.out, (5.2, both.out[1]), (5.2, out.inputs[1][1]), out.inputs[1]])
    gates.wire(ax, [out.out, (out.out[0] + 0.5, out.out[1])])
    style.text(ax, "X", (out.out[0] + 0.7, out.out[1]), halign="left")
    style.caption(ax, _CAPTION, 4.0, -1.9)


_LEFT, _RIGHT = style.caption_bounds(_CAPTION, 4.0)
REVIEW_NETWORK = style.Figure(
    _draw_review, (min(-1.2, _LEFT) - 0.4, -1.9 - style.caption_height(_CAPTION) - 0.5,
                   max(9.2, _RIGHT) + 0.4, 2.6))

FIGURES = {
    "l12_review_network": (REVIEW_NETWORK, [paths.lecture("L12") / "review_network.png"]),
}
