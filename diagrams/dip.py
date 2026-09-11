"""DIP-14 pinout drawings of the 74HC gate circuits used in L04 and Labb 2.

A circuit is drawn the way its datasheet's logic diagram draws it: seen from above, pin 1 at the
bottom left next to the notch, pins 1-7 along the bottom edge left to right and pins 8-14 along
the top edge right to left, with the gates drawn inside the package and wired to the pins they
use. Pin numbers and pin names sit outside the package, so nothing inside competes with the wires.

Two pin patterns cover every circuit here:

* 74HC00, 74HC08, 74HC32, 74HC86: inputs A and B on the two left pins of each group of three,
  output Y on the right one (1A=1, 1B=2, 1Y=3, ... 3Y=8, 3A=9, 3B=10, 4Y=11, 4A=12, 4B=13).
* 74HC02: the output comes *first* in each group (1Y=1, 1A=2, 1B=3, ... 3A=8, 3B=9, 3Y=10,
  4A=11, 4B=12, 4Y=13), so its gates face the other way. This is the pinout that catches people
  who wire a 7402 from memory of a 7400.

The 74HC04 has six inverters, input then output (1A=1, 1Y=2, ... 6A=13, 6Y=12).
Every circuit has GND on pin 7 and VCC on pin 14.
"""

from __future__ import annotations

import schemdraw.logic as logic
from matplotlib.patches import Arc, Rectangle

import style

PITCH = 2.2            # Distance between two neighbouring pins.
BODY_H = 5.4           # Height of the package, between the two rows of pins.
END = 0.8 * PITCH      # Package overhang beyond the outermost pins.
PIN_W = 0.55
PIN_H = 0.45
GATE_SCALE = 0.85      # schemdraw gate size inside the package.
GATE_Y = 1.55          # Gate centre line, measured in from the pin row it is wired to.
OUT_GAP = 0.38         # Between a gate's output end and the pin column its output drops to.
MARGIN = 0.5

GATE_KIND = {"00": "nand", "02": "nor", "04": "not", "08": "and", "32": "or", "86": "xor"}
FUNCTION = {"00": "4 x NAND", "02": "4 x NOR", "04": "6 x inverterare", "08": "4 x AND",
            "32": "4 x OR", "86": "4 x XOR"}


def pin_x(pin: int) -> float:
    """x of one pin: 1-7 left to right along the bottom, 14-8 left to right along the top."""
    return (pin - 1) * PITCH if pin <= 7 else (14 - pin) * PITCH


def pin_names(number: str) -> dict[int, str]:
    """The datasheet's name for every pin of one circuit."""
    names = {7: "GND", 14: "VCC"}
    if number == "04":
        names.update({1: "1A", 2: "1Y", 3: "2A", 4: "2Y", 5: "3A", 6: "3Y",
                      8: "4Y", 9: "4A", 10: "5Y", 11: "5A", 12: "6Y", 13: "6A"})
    elif number == "02":
        names.update({1: "1Y", 2: "1A", 3: "1B", 4: "2Y", 5: "2A", 6: "2B",
                      8: "3A", 9: "3B", 10: "3Y", 11: "4A", 12: "4B", 13: "4Y"})
    else:
        names.update({1: "1A", 2: "1B", 3: "1Y", 4: "2A", 5: "2B", 6: "2Y",
                      8: "3Y", 9: "3A", 10: "3B", 11: "4Y", 12: "4A", 13: "4B"})
    return names


def _wire(ax, points) -> None:
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=style.LINE_COLOR, lw=style.WIRE_WIDTH * 0.8,
            solid_joinstyle="miter", zorder=2)


def _gate(drawing, kind: str, out: tuple[float, float], facing: str):
    """Place one gate by its output pin; returns (input anchors sorted top to bottom, out)."""
    make = {"nand": lambda: logic.Nand(inputs=2), "nor": lambda: logic.Nor(inputs=2),
            "and": lambda: logic.And(inputs=2), "or": lambda: logic.Or(inputs=2),
            "xor": lambda: logic.Xor(inputs=2), "not": lambda: logic.Not()}[kind]
    element = make().scale(GATE_SCALE)
    element = getattr(element, facing)()
    element = drawing.add(element.anchor("out").at(out))
    names = ["in1"] if kind == "not" else ["in1", "in2"]
    inputs = sorted((tuple(element.absanchors[n]) for n in names), key=lambda p: -p[1])
    return inputs, tuple(element.absanchors["out"])


def _two_input(drawing, ax, kind: str, pins: tuple[int, int, int], top: bool,
               output_first: bool) -> None:
    """One two-input gate wired to three neighbouring pins (a, b, y) of one row."""
    a, b, y = pins
    row_y = BODY_H if top else 0.0
    centre = BODY_H - GATE_Y if top else GATE_Y
    xs = {p: pin_x(p) for p in pins}
    if not output_first:
        # Inputs on the two left pins, output on the right: the gate faces right.
        out_x = max(xs.values()) - OUT_GAP
        inputs, out = _gate(drawing, kind, (out_x, centre), "right")
        far, near = sorted((a, b), key=lambda p: xs[p])      # far = further from the gate
        out_pin = y
    else:
        # Output on the left pin, inputs on the two right pins: the gate faces left.
        out_x = min(xs.values()) + OUT_GAP
        inputs, out = _gate(drawing, kind, (out_x, centre), "left")
        near, far = sorted((a, b), key=lambda p: xs[p])
        out_pin = y
    upper, lower = inputs
    # The pin further from the gate takes the input furthest from its own row, so its wire runs
    # past the nearer pin's wire instead of crossing it.
    far_input, near_input = (lower, upper) if top else (upper, lower)
    for pin, target in ((far, far_input), (near, near_input)):
        _wire(ax, [(xs[pin], row_y), (xs[pin], target[1]), target])
    _wire(ax, [out, (xs[out_pin], out[1]), (xs[out_pin], row_y)])


def _inverter(drawing, ax, pins: tuple[int, int], top: bool) -> None:
    """One inverter from input pin a to the output pin y to its right, in one row.

    Drawn by hand rather than with schemdraw's Not, whose leads stretch it to a fixed length
    that is longer than the distance between two pins.
    """
    from matplotlib.patches import Circle, Polygon

    a, y = pins
    row_y = BODY_H if top else 0.0
    centre = BODY_H - GATE_Y if top else GATE_Y
    width, height, bubble = 0.75, 0.62, 0.09
    out_x = pin_x(y) - OUT_GAP
    tip = out_x - 2 * bubble
    left = tip - width
    ax.add_patch(Polygon([(left, centre + height / 2), (tip, centre),
                          (left, centre - height / 2)], closed=True,
                         facecolor=style.BACKGROUND, edgecolor=style.LINE_COLOR,
                         lw=style.WIRE_WIDTH, zorder=3))
    ax.add_patch(Circle((tip + bubble, centre), bubble, facecolor=style.BACKGROUND,
                        edgecolor=style.LINE_COLOR, lw=style.WIRE_WIDTH * 0.8, zorder=3))
    _wire(ax, [(pin_x(a), row_y), (pin_x(a), centre), (left, centre)])
    _wire(ax, [(out_x, centre), (pin_x(y), centre), (pin_x(y), row_y)])


def _draw(number: str, drawing, ax) -> None:
    left, right = -END, 6 * PITCH + END
    ax.add_patch(Rectangle((left, 0), right - left, BODY_H, facecolor="#f4f4f4",
                           edgecolor=style.LINE_COLOR, lw=style.BOX_WIDTH, zorder=1))
    # The notch that marks the pin 1 end.
    ax.add_patch(Arc((left, BODY_H / 2), 1.0, 1.0, theta1=-90, theta2=90,
                     color=style.LINE_COLOR, lw=style.BOX_WIDTH, zorder=3))
    style.text(ax, f"74HC{number}", (3 * PITCH, BODY_H / 2 + 0.22), size=style.SMALL_SIZE,
               weight="bold")
    style.text(ax, FUNCTION[number], (3 * PITCH, BODY_H / 2 - 0.25), size=style.TINY_SIZE,
               color=style.MUTED_COLOR)

    names = pin_names(number)
    for pin in range(1, 15):
        x = pin_x(pin)
        top = pin >= 8
        y0 = BODY_H if top else -PIN_H
        ax.add_patch(Rectangle((x - PIN_W / 2, y0), PIN_W, PIN_H, facecolor="#c8c8c8",
                               edgecolor=style.LINE_COLOR, lw=style.CELL_WIDTH, zorder=1))
        sign = 1 if top else -1
        edge = BODY_H + PIN_H if top else -PIN_H
        style.text(ax, str(pin), (x, edge + sign * 0.12),
                   valign="bottom" if top else "top", size=style.SMALL_SIZE, weight="bold")
        colour = style.ACCENT_COLOR if names[pin] in ("VCC", "GND") else style.ACCENT_COLOR_2
        style.text(ax, names[pin], (x, edge + sign * 0.62),
                   valign="bottom" if top else "top", size=style.TINY_SIZE, color=colour)

    kind = GATE_KIND[number]
    if number == "04":
        for pins, top in (((1, 2), False), ((3, 4), False), ((5, 6), False),
                          ((13, 12), True), ((11, 10), True), ((9, 8), True)):
            _inverter(drawing, ax, pins, top)
    elif number == "02":
        for pins, top in (((2, 3, 1), False), ((5, 6, 4), False),
                          ((11, 12, 13), True), ((8, 9, 10), True)):
            _two_input(drawing, ax, kind, pins, top, output_first=True)
    else:
        for pins, top in (((1, 2, 3), False), ((4, 5, 6), False),
                          ((12, 13, 11), True), ((9, 10, 8), True)):
            _two_input(drawing, ax, kind, pins, top, output_first=False)


def figure(number: str) -> style.Figure:
    """The pinout of 74HC<number>, e.g. figure("00")."""
    text = style.text_height(style.SMALL_SIZE) + style.text_height(style.TINY_SIZE) + 0.8
    return style.Figure(lambda d, ax: _draw(number, d, ax),
                        (-END - 0.9 - MARGIN, -PIN_H - text - MARGIN,
                         6 * PITCH + END + MARGIN, BODY_H + PIN_H + text + MARGIN))
