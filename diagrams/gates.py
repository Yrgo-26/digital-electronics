"""Logic gates, in both symbol standards the course shows.

* **ANSI/IEEE** (the distinctive shapes: the D-shaped AND, the curved OR) are what CircuitVerse,
  most datasheets and most of the internet draw. They come from `schemdraw.logic`.
* **IEC 60617** (rectangles with `&`, `≥1`, `1` or `=1` inside, and a small circle for an
  inverted output) are what Swedish textbooks and electrical schematics tend to draw. schemdraw
  has none, so they are drawn here.

Both helpers place a gate at an absolute point and hand back its pin coordinates, so a network
is drawn by placing gates and then joining pins with `wire`. Nothing depends on a drawing
cursor.
"""

from __future__ import annotations

from dataclasses import dataclass

import schemdraw.logic as logic
from matplotlib.patches import Circle, Rectangle

import style

# ----------------------------------------------------------------------------------------
# IEC rectangles, in canvas units.
# ----------------------------------------------------------------------------------------
IEC_W = 1.3
IEC_PITCH = 0.7        # Vertical distance between two input pins.
IEC_LEAD = 0.55        # Length of the input and output leads outside the box.
BUBBLE_R = 0.12

IEC_SYMBOLS = {
    "and": "&", "nand": "&", "or": "≥1", "nor": "≥1", "not": "1", "buf": "1",
    "xor": "=1", "xnor": "=1",
}
INVERTED = {"nand", "nor", "not", "xnor"}


@dataclass(frozen=True)
class Pins:
    """Where a placed gate's pins ended up: `inputs` top to bottom, and `out`."""

    inputs: tuple[tuple[float, float], ...]
    out: tuple[float, float]


def wire(ax, points, color: str | None = None) -> None:
    """A polyline of wire through the given points."""
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color or style.LINE_COLOR, lw=style.WIRE_WIDTH,
            solid_capstyle="round", solid_joinstyle="round", zorder=2)


def dot(ax, point) -> None:
    """A junction dot where a signal branches."""
    ax.add_patch(Circle(point, 0.08, color=style.LINE_COLOR, zorder=4))


def iec(ax, kind: str, centre: tuple[float, float], inputs: int = 2,
        label: str | None = None) -> Pins:
    """An IEC gate centred at `centre`. `kind` is and/or/not/nand/nor/xor/xnor/buf."""
    n = 1 if kind in ("not", "buf") else inputs
    height = max(1.2, (n - 1) * IEC_PITCH + 0.9)
    x, y = centre
    left, right = x - IEC_W / 2, x + IEC_W / 2
    ax.add_patch(Rectangle((left, y - height / 2), IEC_W, height, facecolor=style.BACKGROUND,
                           edgecolor=style.LINE_COLOR, lw=style.BOX_WIDTH, zorder=3))
    style.text(ax, label or IEC_SYMBOLS[kind], (x, y + height / 2 - 0.3),
               size=style.SMALL_SIZE, valign="top")

    pins = []
    first = y + (n - 1) * IEC_PITCH / 2
    for i in range(n):
        pin_y = first - i * IEC_PITCH
        wire(ax, [(left - IEC_LEAD, pin_y), (left, pin_y)])
        pins.append((left - IEC_LEAD, pin_y))

    out_start = right
    if kind in INVERTED:
        ax.add_patch(Circle((right + BUBBLE_R, y), BUBBLE_R, facecolor=style.BACKGROUND,
                            edgecolor=style.LINE_COLOR, lw=style.WIRE_WIDTH, zorder=4))
        out_start = right + 2 * BUBBLE_R
    wire(ax, [(out_start, y), (right + IEC_LEAD, y)])
    return Pins(tuple(pins), (right + IEC_LEAD, y))


# ----------------------------------------------------------------------------------------
# ANSI shapes, from schemdraw.
# ----------------------------------------------------------------------------------------
ANSI_CLASSES = {
    "and": logic.And, "nand": logic.Nand, "or": logic.Or, "nor": logic.Nor,
    "xor": logic.Xor, "xnor": logic.Xnor, "not": logic.Not, "buf": logic.Buf,
}


# schemdraw's gates are drawn for its own default text size; ours is larger, so they are scaled
# up to match. Every anchor scales with the element, so pin positions stay exact.
ANSI_SCALE = 1.35


def ansi(drawing, kind: str, out: tuple[float, float], inputs: int = 2,
         inputnots: tuple[int, ...] | None = None, scale: float = ANSI_SCALE) -> Pins:
    """An ANSI gate whose output pin sits exactly at `out`, facing right.

    Placed by its output rather than its centre, because a network is usually drawn from the
    output backwards: the output position is what the next gate needs.
    """
    cls = ANSI_CLASSES[kind]
    if kind in ("not", "buf"):
        # schemdraw pads a one-input gate with leads out to its default element length, so the
        # drawn wire runs well past the `in1` and `out` anchors it reports, and a wire joined to
        # those anchors overshoots its corner. Setting the length to the body itself removes the
        # leads, and leaves both anchors exactly where they were.
        body = cls().anchors["out"][0] - cls().anchors["in1"][0]
        element = cls().scale(scale).length(body * scale)
    else:
        element = cls(inputs=inputs, inputnots=inputnots).scale(scale)
    element = drawing.add(element.right().anchor("out").at(out))
    names = ["in1"] if kind in ("not", "buf") else [f"in{i + 1}" for i in range(inputs)]
    inputs_xy = tuple(tuple(element.absanchors[name]) for name in names)
    return Pins(inputs_xy, tuple(element.absanchors["out"]))
