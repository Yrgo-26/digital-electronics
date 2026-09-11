"""L05 figures: troubleshooting a gate network, as a method and as a measurement plan."""

from __future__ import annotations

import flowchart as fc
import gates
import paths
import style

L05 = paths.lecture("L05")

# ----------------------------------------------------------------------------------------
# A.1: the order of work, as a flowchart.
# ----------------------------------------------------------------------------------------
_NODES = [
    fc.Node("terminal", ["Nätet ger fel utgång"], (0, 0), width=6.4),
    fc.Node("process", ["Hitta en rad i tabellen", "där utgången är fel"], (0, -2.2), width=5.0),
    fc.Node("decision", ["5 V mellan ben 14", "och ben 7 på", "varje krets?"], (0, -4.7), width=6.4,
            height=2.4),
    fc.Node("process", ["Rätta matningen"], (7.6, -4.7), width=4.0),
    fc.Node("process", ["Ställ in raden, mät", "varje grinds in- och utgångar"], (0, -7.3),
            width=6.2),
    fc.Node("decision", ["Första grinden där", "mätt och förväntat", "skiljer sig?"], (0, -9.9),
            width=7.2, height=2.6),
    fc.Node("process", ["Ingångarna fel: ledning", "eller ben före grinden"], (-7.4, -12.8),
            width=5.8),
    fc.Node("process", ["Ingångarna rätt, utgången", "fel: grinden eller kretsen"],
            (7.4, -12.8), width=5.8),
    fc.Node("terminal", ["Rätta, och testa", "om alla rader"], (0, -16.0), width=6.4),
]
_EDGES = [
    fc.Edge(0, 1), fc.Edge(1, 2),
    fc.Edge(2, 3, "right", "left", label="Nej"),
    fc.Edge(2, 4, label="Ja"),
    fc.Edge(3, 1, "top", "right", via=[(7.6, -2.2)]),
    fc.Edge(4, 5),
    fc.Edge(5, 6, "left", "top", via=[(-7.4, -9.9)], label="i ingången"),
    fc.Edge(5, 7, "right", "top", via=[(7.4, -9.9)], label="i utgången"),
    # Both branches join above the last box and enter it from the top: a terminal's rounded
    # ends sit inside its nominal width, so an arrow into its side would stop short of it.
    fc.Edge(6, 8, "bottom", "top", via=[(-7.4, -14.6), (0, -14.6)]),
    fc.Edge(7, 8, "bottom", "top", via=[(7.4, -14.6), (0, -14.6)]),
]
TROUBLESHOOTING = fc.figure(_NODES, _EDGES)

# ----------------------------------------------------------------------------------------
# A.5: halving a chain of eight inverters.
# ----------------------------------------------------------------------------------------
_PITCH = 1.8


def _draw_half_split(d, ax) -> None:
    outs = []
    for i in range(8):
        pins = gates.ansi(d, "not", ((i + 1) * _PITCH, 0.0), scale=0.9)
        outs.append(pins.out)
        if i == 0:
            gates.wire(ax, [(-0.4, 0.0), pins.inputs[0]])
        else:
            gates.wire(ax, [outs[i - 1], pins.inputs[0]])
    gates.wire(ax, [outs[-1], (outs[-1][0] + 0.6, 0.0)])
    style.text(ax, "in", (-0.6, 0.0), halign="right", size=style.SMALL_SIZE)
    style.text(ax, "ut", (outs[-1][0] + 0.9, 0.0), halign="left", size=style.SMALL_SIZE)
    # Measurement points after inverter 4, then 2 or 6, then the last one needed.
    for index, (after, label) in enumerate(((3, "1:a mätningen"), (1, "2:a om felet är före"),
                                            (5, "2:a om felet är efter"))):
        x = outs[after][0] + 0.2
        colour = style.ACCENT_COLOR if index == 0 else style.ACCENT_COLOR_2
        y = 0.9 + (0.0 if index == 0 else 0.55)
        ax.annotate("", xy=(x, 0.08), xytext=(x, y - 0.1),
                    arrowprops=dict(arrowstyle="->", color=colour, lw=style.ACCENT_WIDTH))
        style.text(ax, label, (x, y), valign="bottom", size=style.TINY_SIZE, color=colour)
    style.caption(ax, ("Mät i mitten först. Varje mätning halverar sträckan där felet kan sitta:",
                       "åtta grindar kräver högst tre mätningar, sexton högst fyra."),
                  4.5 * _PITCH, -0.9)


_CAPTION_WIDTH = style.caption_bounds(("Mät i mitten först. Varje mätning halverar sträckan där "
                                       "felet kan sitta:",), 4.5 * _PITCH)
HALF_SPLIT = style.Figure(_draw_half_split, (min(-1.4, _CAPTION_WIDTH[0] - 0.3), -2.2,
                                             max(9 * _PITCH + 1.4, _CAPTION_WIDTH[1] + 0.3), 2.3))

FIGURES = {
    "l05_troubleshooting": (TROUBLESHOOTING, [L05 / "troubleshooting.png"]),
    "l05_half_split": (HALF_SPLIT, [L05 / "half_split.png"]),
}
