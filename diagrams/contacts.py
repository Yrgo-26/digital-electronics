"""Contact networks: push-button contacts, relay contacts, lamps and coils, IEC style.

The course draws contact networks the way a Swedish electrical schematic (strömvägsschema)
does: vertical current paths between a supply rail at the top (+24 V) and a return rail at
the bottom (0 V), with every contact drawn vertically in the path. A closed path lights the
lamp at its bottom, so "the lamp is lit" and "there is a closed path from the top rail to the
bottom rail" are the same statement, which is the whole bridge from contacts to logic.

Symbols follow IEC 60617 in the simplified form every textbook uses:

* a normally open contact (slutande, NO) is a blade tilted away from the upper terminal;
* a normally closed contact (brytande, NC) is a blade tilted onto a short stub that sticks out
  of the upper terminal;
* a push button adds a dashed mechanical link from the blade to an E-shaped actuator;
* a lamp is a circle with a cross; a relay coil is a rectangle.

Every function takes absolute canvas coordinates and returns where it ended, so a path is drawn
by chaining calls downwards. Nothing here uses schemdraw's cursor, for the reason given in the
assembly course's circuit module: relative placement is how a symbol ends up mirrored.

Ladder symbols (PLC stegdiagram) are at the bottom, for the one figure that compares the two.
"""

from __future__ import annotations

import math

from matplotlib.patches import Circle, Rectangle

import style

# ----------------------------------------------------------------------------------------
# Geometry, in canvas units.
# ----------------------------------------------------------------------------------------
CONTACT_LEN = 1.9      # Top terminal to bottom terminal of a contact.
GAP = 0.70             # Length of the contact gap in the middle of that.
BLADE_ANGLE = 28.0     # Degrees from vertical.
STUB = 0.30            # Length of an NC contact's resting stub.
LINK_LEN = 1.05        # Dashed mechanical link from blade to actuator.
LAMP_R = 0.42
LAMP_LEN = 1.9         # Space a lamp takes in a path, leads included.
COIL_W = 1.0
COIL_H = 0.62
COIL_LEN = 1.9
DOT_R = 0.085
LABEL_GAP = 0.32


def wire(ax, points, color: str | None = None, lw: float | None = None) -> None:
    """A polyline of wire through the given points."""
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color or style.LINE_COLOR, lw=lw or style.WIRE_WIDTH,
            solid_capstyle="round", solid_joinstyle="round", zorder=2)


def dot(ax, point) -> None:
    """A junction dot, where three or more wires meet."""
    ax.add_patch(Circle(point, DOT_R, color=style.LINE_COLOR, zorder=3))


def rail(ax, x0: float, x1: float, y: float, label: str) -> None:
    """A horizontal supply rail with its name to the left of it."""
    wire(ax, [(x0, y), (x1, y)], lw=style.BOX_WIDTH)
    style.text(ax, label, (x0 - 0.25, y), halign="right", size=style.SMALL_SIZE)


def contact(ax, x: float, top: float, kind: str = "no", label: str = "",
            push: bool = True, terminals: tuple[str, str] | None = None,
            highlight: bool = False) -> float:
    """A vertical contact from `top` downwards; returns the y of its bottom terminal.

    `kind` is "no" (slutande) or "nc" (brytande). `push` adds a push-button actuator on the
    left; a relay's contact has none, and is identified by its label alone. `terminals` are
    the terminal numbers printed on the right, e.g. ("13", "14") for an NO block.
    """
    ink = style.ACCENT_COLOR if highlight else style.LINE_COLOR
    bottom = top - CONTACT_LEN
    upper = top - (CONTACT_LEN - GAP) / 2          # Where the upper conductor ends.
    lower = bottom + (CONTACT_LEN - GAP) / 2       # Where the blade is hinged.
    wire(ax, [(x, top), (x, upper)], color=ink)
    wire(ax, [(x, lower), (x, bottom)], color=ink)

    length = GAP / math.cos(math.radians(BLADE_ANGLE)) * 1.08
    if kind == "no":
        # Tilted away to the left: it does not reach the upper conductor.
        tip = (x - length * math.sin(math.radians(BLADE_ANGLE)),
               lower + length * math.cos(math.radians(BLADE_ANGLE)))
    elif kind == "nc":
        # Tilted to the right, resting against a stub from the upper conductor.
        wire(ax, [(x, upper), (x + STUB, upper)], color=ink)
        tip = (x + STUB * 1.25, upper + 0.10)
    else:
        raise ValueError(f"unknown contact kind {kind!r}")
    wire(ax, [(x, lower), tip], color=ink)

    blade_mid = ((x + tip[0]) / 2, (lower + tip[1]) / 2)
    if push:
        # Dashed link from the middle of the blade to an E-shaped push actuator on the left.
        start = (blade_mid[0], blade_mid[1])
        end_x = x - LINK_LEN
        ax.plot([start[0], end_x], [start[1], start[1]], color=ink, lw=style.WIRE_WIDTH * 0.8,
                linestyle=(0, (3, 2)), zorder=2)
        spine = 0.26
        wire(ax, [(end_x + 0.18, start[1] + spine), (end_x, start[1] + spine),
                  (end_x, start[1] - spine), (end_x + 0.18, start[1] - spine)], color=ink)
    if label:
        style.text(ax, label, (x - (LINK_LEN + 0.25 if push else LABEL_GAP), blade_mid[1]),
                   halign="right", size=style.SMALL_SIZE, color=ink)
    if terminals:
        style.text(ax, terminals[0], (x + 0.18, top - 0.12), halign="left", valign="top",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
        style.text(ax, terminals[1], (x + 0.18, bottom + 0.12), halign="left",
                   valign="bottom", size=style.TINY_SIZE, color=style.MUTED_COLOR)
    return bottom


def lamp(ax, x: float, top: float, label: str = "H1", lit: bool = False) -> float:
    """A signal lamp: a circle with a cross, in a vertical path. Returns its bottom y."""
    bottom = top - LAMP_LEN
    centre = (x, (top + bottom) / 2)
    wire(ax, [(x, top), (x, centre[1] + LAMP_R)])
    wire(ax, [(x, centre[1] - LAMP_R), (x, bottom)])
    face = "#fff3b0" if lit else style.BACKGROUND
    ax.add_patch(Circle(centre, LAMP_R, facecolor=face, edgecolor=style.LINE_COLOR,
                        lw=style.WIRE_WIDTH, zorder=3))
    d = LAMP_R / math.sqrt(2)
    for sx in (-1, 1):
        ax.plot([centre[0] - d, centre[0] + d], [centre[1] - sx * d, centre[1] + sx * d],
                color=style.LINE_COLOR, lw=style.WIRE_WIDTH * 0.8, zorder=4)
    if label:
        style.text(ax, label, (x + LAMP_R + 0.25, centre[1]), halign="left",
                   size=style.SMALL_SIZE)
    return bottom


def coil(ax, x: float, top: float, label: str = "K1") -> float:
    """A relay coil: a rectangle in a vertical path. Returns its bottom y."""
    bottom = top - COIL_LEN
    mid = (top + bottom) / 2
    wire(ax, [(x, top), (x, mid + COIL_H / 2)])
    wire(ax, [(x, mid - COIL_H / 2), (x, bottom)])
    ax.add_patch(Rectangle((x - COIL_W / 2, mid - COIL_H / 2), COIL_W, COIL_H,
                           facecolor=style.BACKGROUND, edgecolor=style.LINE_COLOR,
                           lw=style.WIRE_WIDTH, zorder=3))
    if label:
        style.text(ax, label, (x + COIL_W / 2 + 0.22, mid), halign="left",
                   size=style.SMALL_SIZE)
    return bottom


def link(ax, a: tuple[float, float], b: tuple[float, float]) -> None:
    """A dashed mechanical link, e.g. between two contact blocks of the same push button."""
    ax.plot([a[0], b[0]], [a[1], b[1]], color=style.MUTED_COLOR, lw=style.WIRE_WIDTH * 0.8,
            linestyle=(0, (3, 2)), zorder=1)


# ----------------------------------------------------------------------------------------
# Ladder diagram (PLC stegdiagram) symbols: horizontal rungs between two vertical rails.
# ----------------------------------------------------------------------------------------
LD_W = 1.3      # Width of a ladder symbol.
LD_H = 0.9      # Height of a contact's two bars.


def ld_contact(ax, x: float, y: float, kind: str = "no", label: str = "") -> float:
    """`-| |-` (NO) or `-|/|-` (NC), starting at x; returns the x it ends at."""
    bar_a, bar_b = x + LD_W * 0.32, x + LD_W * 0.68
    wire(ax, [(x, y), (bar_a, y)])
    wire(ax, [(bar_b, y), (x + LD_W, y)])
    for bar in (bar_a, bar_b):
        wire(ax, [(bar, y - LD_H / 2), (bar, y + LD_H / 2)], lw=style.BOX_WIDTH)
    if kind == "nc":
        wire(ax, [(bar_a + 0.02, y - LD_H / 2 + 0.05), (bar_b - 0.02, y + LD_H / 2 - 0.05)])
    if label:
        style.text(ax, label, ((bar_a + bar_b) / 2, y + LD_H / 2 + 0.2), valign="bottom",
                   size=style.SMALL_SIZE)
    return x + LD_W


def ld_coil(ax, x: float, y: float, label: str = "") -> float:
    """`-( )-`, starting at x; returns the x it ends at."""
    from matplotlib.patches import Arc

    left, right = x + LD_W * 0.30, x + LD_W * 0.70
    wire(ax, [(x, y), (left, y)])
    wire(ax, [(right, y), (x + LD_W, y)])
    for centre, theta in ((left + 0.22, (110, 250)), (right - 0.22, (-70, 70))):
        ax.add_patch(Arc((centre, y), 0.5, LD_H, theta1=theta[0], theta2=theta[1],
                         color=style.LINE_COLOR, lw=style.BOX_WIDTH))
    if label:
        style.text(ax, label, ((left + right) / 2, y + LD_H / 2 + 0.2), valign="bottom",
                   size=style.SMALL_SIZE)
    return x + LD_W


def column(ax, x: float, top: float, bottom: float, items, spacing: float = 0.35) -> None:
    """One vertical current path from `top` to `bottom`, with its elements stacked in order.

    `items` is a sequence of tuples: ("no", label), ("nc", label), ("relay_no", label),
    ("relay_nc", label), ("lamp", label), ("coil", label), or ("gap", length) for extra wire.
    Wire is drawn between the elements and from the last one down to `bottom`, so a path can
    never be left with a gap in it, which is the mistake drawing it by hand invites.
    A contact tuple may carry a third element, a dict of keyword arguments for `contact`.
    """
    y = top
    wire(ax, [(x, y), (x, y - spacing)])
    y -= spacing
    for item in items:
        kind, label = item[0], item[1]
        extra = item[2] if len(item) > 2 else {}
        if kind in ("no", "nc"):
            y = contact(ax, x, y, kind, label, **extra)
        elif kind in ("relay_no", "relay_nc"):
            y = contact(ax, x, y, kind.split("_")[1], label, push=False, **extra)
        elif kind == "lamp":
            y = lamp(ax, x, y, label, **extra)
        elif kind == "coil":
            y = coil(ax, x, y, label)
        elif kind == "gap":
            wire(ax, [(x, y), (x, y - label)])
            y -= label
            continue
        else:
            raise ValueError(f"unknown path element {kind!r}")
        wire(ax, [(x, y), (x, y - spacing)])
        y -= spacing
    if y < bottom:
        raise ValueError(f"path at x={x} does not fit: reaches {y:.2f}, bottom is {bottom}")
    wire(ax, [(x, y), (x, bottom)])
