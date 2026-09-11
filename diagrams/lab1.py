"""Labb 1 figures: the station's parts, the continuity test, and the network in task 8."""

from __future__ import annotations

from matplotlib.patches import Circle

import contacts as c
import paths
import shapes
import style
from l02 import paths_figure

# ----------------------------------------------------------------------------------------
# The station: two push buttons, each with a normally open and a normally closed block that
# are pressed together, a lamp and the supply.
# ----------------------------------------------------------------------------------------
_STATION_CAPTION = (
    "Exempel på märkning. Slutsiffrorna 3-4 betyder slutande (NO), 1-2 brytande (NC).",
    "Kontrollera märkningen på just din station, och rita av den i uppgift 1.")


def _draw_station(d, ax) -> None:
    top = 0.0
    for x0, name in ((1.6, "S1"), (9.0, "S2")):
        c.contact(ax, x0, top, "no", name, terminals=("13", "14"))
        c.contact(ax, x0 + 3.2, top, "nc", "", push=False, terminals=("21", "22"))
        # The NC block is in the same button: one dashed link joins both blades.
        c.link(ax, (x0 - 0.15, -0.95), (x0 + 3.2 + 0.3, -0.95))
        shapes.dashed_box(ax, x0 - 2.3, -2.5, x0 + 4.1, 0.9, "")
        style.text(ax, f"Tryckknapp {name}", (x0 + 1.2, -2.95), valign="top",
                   size=style.SMALL_SIZE)
    c.lamp(ax, 15.9, top, "H1")
    style.text(ax, "X1", (16.1, -0.1), halign="left", valign="top", size=style.TINY_SIZE,
               color=style.MUTED_COLOR)
    style.text(ax, "X2", (16.1, -1.8), halign="left", valign="bottom", size=style.TINY_SIZE,
               color=style.MUTED_COLOR)
    style.text(ax, "Lampa 24 V", (15.9, -2.95), valign="top", size=style.SMALL_SIZE)
    for y, text in ((0.2, "+24 V"), (-1.7, "0 V")):
        ax.add_patch(Circle(
            (19.5, y), 0.22, facecolor=style.BACKGROUND, edgecolor=style.LINE_COLOR,
            lw=style.WIRE_WIDTH))
        style.text(ax, text, (19.95, y), halign="left", size=style.SMALL_SIZE)
    style.text(ax, "Aggregat", (20.2, -2.95), valign="top", size=style.SMALL_SIZE)
    style.caption(ax, _STATION_CAPTION, 10.8, -3.9)


_S_LEFT, _S_RIGHT = style.caption_bounds(_STATION_CAPTION, 10.8)
STATION = style.Figure(
    _draw_station,
    (min(-1.2, _S_LEFT) - 0.4, -3.9 - style.caption_height(_STATION_CAPTION) - 0.4,
     max(21.9, _S_RIGHT) + 0.4, 1.4))

# ----------------------------------------------------------------------------------------
# Task 1: the lamp as a continuity tester. Whatever sits between a and b closes the path.
# ----------------------------------------------------------------------------------------
_TEST_CAPTION = ("Lampan lyser om det som sitter mellan a och b leder.",
                 "Koppla ett kontaktelement i taget mellan a och b, och tryck på knappen.")


def _draw_continuity(d, ax) -> None:
    x, top, bottom = 2.5, 0.0, -6.4
    c.rail(ax, 0.8, 4.4, top, "+24 V")
    c.rail(ax, 0.8, 4.4, bottom, "0 V")
    c.wire(ax, [(x, top), (x, -1.0)])
    ax.add_patch(Circle(
        (x, -1.0), 0.13, facecolor=style.BACKGROUND, edgecolor=style.LINE_COLOR,
        lw=style.WIRE_WIDTH, zorder=4))
    ax.add_patch(Circle(
        (x, -3.0), 0.13, facecolor=style.BACKGROUND, edgecolor=style.LINE_COLOR,
        lw=style.WIRE_WIDTH, zorder=4))
    shapes.dashed_box(ax, x - 1.1, -2.9, x + 1.1, -1.1, "")
    style.text(ax, "?", (x, -2.0), size=style.TITLE_SIZE, color=style.ACCENT_COLOR)
    style.text(ax, "a", (x + 0.3, -0.8), halign="left", size=style.SMALL_SIZE)
    style.text(ax, "b", (x + 0.3, -3.2), halign="left", size=style.SMALL_SIZE)
    c.wire(ax, [(x, -3.0), (x, -3.5)])
    y = c.lamp(ax, x, -3.5, "H1")
    c.wire(ax, [(x, y), (x, bottom)])
    c.dot(ax, (x, top))
    c.dot(ax, (x, bottom))
    style.caption(ax, _TEST_CAPTION, x, bottom - 0.6)


_C_LEFT, _C_RIGHT = style.caption_bounds(_TEST_CAPTION, 2.5)
CONTINUITY = style.Figure(
    _draw_continuity,
    (min(-0.7, _C_LEFT) - 0.4, -7.0 - style.caption_height(_TEST_CAPTION) - 0.4,
     max(4.8, _C_RIGHT) + 0.4, 0.5))

# ----------------------------------------------------------------------------------------
# Task 8: the network to analyse, S1 + S1'·S2, before it is simplified.
# ----------------------------------------------------------------------------------------
TASK8 = paths_figure(
    [("s", [("p", [("no", "S1"), ("s", [("nc", "S1"), ("no", "S2")])]), ("lamp", "H1")])],
    caption=("Nätet i uppgift 8. Kontakterna med samma beteckning",
             "sitter i samma knapp."))

FIGURES = {
    "lab1_station": (STATION, [paths.lab("lab1") / "station.png"]),
    "lab1_continuity": (CONTINUITY, [paths.lab("lab1") / "continuity.png"]),
    "lab1_task8": (TASK8, [paths.lab("lab1") / "task8.png"]),
}
