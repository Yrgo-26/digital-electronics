"""L03 figures: analysing contact networks, and finding the fault in one.

The networks are drawn with the series-parallel engine in l02.py, so a network here is written
the way its expression reads: ("p", [...]) is a sum, ("s", [...]) a product.
"""

from __future__ import annotations

import contacts as c
import paths
import style
from l02 import paths_figure

# ----------------------------------------------------------------------------------------
# A.2: a network read as an expression, and the smaller network with the same table.
# ----------------------------------------------------------------------------------------
_DISTRIBUTED = ("s", [("p", [("no", "S1"), ("no", "S2")]),
                      ("p", [("no", "S1"), ("no", "S3")]), ("lamp", "H1")])
_FACTORED = ("s", [("p", [("no", "S1"), ("s", [("no", "S2"), ("no", "S3")])]),
                   ("lamp", "H1")])

ANALYSIS_EXAMPLE = paths_figure(
    [_DISTRIBUTED, _FACTORED],
    titles=("a) (S1 + S2)·(S1 + S3)", "b) S1 + S2·S3"),
    gap=2.2,
    caption=("Två nät, samma sanningstabell. Nät b) behöver en kontakt mindre, och S1 bara",
             "en gång. Lagen bakom är A + BC = (A + B)(A + C)."))

# ----------------------------------------------------------------------------------------
# A.3: A + A'B' = A + B', as two networks.
# ----------------------------------------------------------------------------------------
_REDUNDANT = ("s", [("p", [("no", "S1"), ("s", [("nc", "S1"), ("nc", "S2")])]), ("lamp", "H1")])
_MINIMAL = ("s", [("p", [("no", "S1"), ("nc", "S2")]), ("lamp", "H1")])

EQUIVALENT = paths_figure(
    [_REDUNDANT, _MINIMAL],
    titles=("a) S1 + S1'·S2'", "b) S1 + S2'"),
    gap=2.2,
    caption=("Den brytande kontakten S1 i nät a) gör ingen nytta. När S1 är nedtryckt leder",
             "den vänstra grenen ändå, och när S1 är släppt är den sluten."))

# ----------------------------------------------------------------------------------------
# A.5: measuring along a path. +24 V, S1 (NO), S2 (NC), H1, 0 V, with measuring points.
# ----------------------------------------------------------------------------------------
_TROUBLE_CAPTION = (
    "Mät spänningen mellan varje mätpunkt och 0 V, uppifrån och ned. Så länge vägen är",
    "sluten visar mätaren 24 V; efter det element som bryter vägen visar den 0 V.")


def _draw_troubleshoot(d, ax) -> None:
    x, top, bottom = 3.0, 0.0, -9.2
    c.rail(ax, 0.0, 6.0, top, "+24 V")
    c.rail(ax, 0.0, 6.0, bottom, "0 V")
    c.dot(ax, (x, top))
    c.dot(ax, (x, bottom))
    points = []
    y = top
    c.wire(ax, [(x, y), (x, y - 0.6)])
    y -= 0.6
    points.append(y)
    y = c.contact(ax, x, y, "no", "S1")
    c.wire(ax, [(x, y), (x, y - 0.6)])
    points.append(y - 0.3)
    y -= 0.6
    y = c.contact(ax, x, y, "nc", "S2")
    c.wire(ax, [(x, y), (x, y - 0.6)])
    points.append(y - 0.3)
    y -= 0.6
    y = c.lamp(ax, x, y, "H1")
    c.wire(ax, [(x, y), (x, bottom)])
    for number, py in enumerate(points, start=1):
        ax.plot([x, x + 1.3], [py, py], color=style.ACCENT_COLOR_2, lw=style.CELL_WIDTH,
                linestyle=(0, (2, 2)))
        c.dot(ax, (x, py))
        style.text(ax, f"M{number}", (x + 1.45, py), halign="left", size=style.SMALL_SIZE,
                   color=style.ACCENT_COLOR_2)
    style.caption(ax, _TROUBLE_CAPTION, 3.0, bottom - 0.6)


_T_LEFT, _T_RIGHT = style.caption_bounds(_TROUBLE_CAPTION, 3.0)
TROUBLESHOOT = style.Figure(
    _draw_troubleshoot,
    (min(-1.4, _T_LEFT) - 0.4, -9.8 - style.caption_height(_TROUBLE_CAPTION) - 0.4,
     max(6.2, _T_RIGHT) + 0.4, 0.5))

# ----------------------------------------------------------------------------------------
# Exercise figures.
# ----------------------------------------------------------------------------------------
EX_NETWORKS = paths_figure(
    [("s", [("no", "S1"), ("p", [("no", "S2"), ("nc", "S2")]), ("lamp", "H1")]),
     ("s", [("nc", "S1"), ("p", [("no", "S1"), ("no", "S2")]), ("lamp", "H2")]),
     ("s", [("p", [("s", [("no", "S1"), ("no", "S2")]), ("s", [("no", "S1"), ("no", "S3")])]),
            ("lamp", "H3")])],
    titles=("a)", "b)", "c)"),
    gap=1.8)

EX_KONTROLL = paths_figure(
    [("s", [("p", [("no", "S1"), ("nc", "S2")]), ("p", [("nc", "S1"), ("no", "S2")]),
            ("lamp", "H1")])],
    caption=("Varje knapp används med en slutande och en brytande kontakt.",))

EX_FAULT = paths_figure(
    [("s", [("p", [("no", "S1"), ("no", "S2")]), ("nc", "S3"), ("lamp", "H1")])],
    caption=("H1 = (S1 + S2)·S3'",))

FIGURES = {
    "l03_analysis_example": (ANALYSIS_EXAMPLE, [paths.lecture("L03") / "analysis_example.png"]),
    "l03_equivalent": (EQUIVALENT, [paths.lecture("L03") / "equivalent.png"]),
    "l03_troubleshoot": (TROUBLESHOOT, [paths.lecture("L03") / "troubleshoot.png"]),
    "l03_ex_networks": (EX_NETWORKS, [paths.lecture("L03") / "ex_networks.png"]),
    "l03_ex_kontroll": (EX_KONTROLL, [paths.lecture("L03") / "ex_kontroll.png"]),
    "l03_ex_fault": (EX_FAULT, [paths.lecture("L03") / "ex_fault.png"]),
}
