"""L04 figures: Karnaugh maps, the networks they lead to, and the 74HC circuits on a breadboard.

Every map below was checked against its truth table by enumerating all rows before it was drawn,
and every network against its expression: a grouping that looks right and covers the wrong cell
renders without complaint, so the check is the only thing that catches it.
"""

from __future__ import annotations

import schemdraw.elements as elm
from matplotlib.patches import Circle, Rectangle

import dip
import gates
import kmap
import paths
import shapes
import style
from kmap import Group, Kmap, from_ones

L04 = paths.lecture("L04")
LAB2 = paths.lab("lab2")


def legend_map(km: Kmap) -> style.Figure:
    """A map whose group terms are listed one per line to the right, in the group's colour.

    kmap.figure writes each term beside the first row of its group, so two groups starting on
    the same row write their terms on top of each other. A list never collides.
    """
    from dataclasses import replace

    base = kmap.figure(replace(km, terms=False))
    if not km.groups:
        return base
    cols = len(km.col_codes)
    x = cols * kmap.CELL_W + kmap.TERM_GAP
    width = max(style.text_width(g.term) for g in km.groups)

    def draw(d, ax) -> None:
        base.draw(d, ax)
        for index, group in enumerate(km.groups):
            colour, _ = kmap.GROUP_STYLES[index % len(kmap.GROUP_STYLES)]
            style.text(ax, group.term, (x, -0.5 * kmap.CELL_H - index * 0.62), halign="left",
                       color=colour)

    left, bottom, right, top = base.canvas
    return style.Figure(draw, (left, bottom, max(right, x + width + kmap.MARGIN), top))


# ----------------------------------------------------------------------------------------
# A.2: the three map shapes, with each cell's minterm number.
# ----------------------------------------------------------------------------------------
LAYOUT2 = kmap.figure(Kmap("AB", {}, minterms=True,
                           caption=("Två variabler: A nedåt, B åt sidan.",)))
LAYOUT3 = kmap.figure(Kmap("ABC", {}, minterms=True,
                           caption=("Tre variabler: AB nedåt i Graykod, C åt sidan.",)))
LAYOUT4 = kmap.figure(Kmap("ABCD", {}, minterms=True,
                           caption=("Fyra variabler: AB nedåt, CD åt sidan,",
                                    "båda i Graykod.")))

# ----------------------------------------------------------------------------------------
# A.3-A.4: the worked example, X = AB + C, as three frames of one map.
# ----------------------------------------------------------------------------------------
_EX_ONES = [1, 3, 5, 6, 7]
EX_FILLED = legend_map(from_ones("ABC", _EX_ONES, show_zeros=True,
                                  caption=("Sanningstabellen inlagd: en etta per rad där X = 1.",)))
EX_GROUP_C = legend_map(from_ones("ABC", _EX_ONES, groups=[Group([0, 1, 2, 3], [1], "C")],
                                   caption=("Första gruppen: hela kolumnen C = 1.",)))
EX_GROUPS = legend_map(from_ones("ABC", _EX_ONES,
                                  groups=[Group([0, 1, 2, 3], [1], "C"), Group([2], [0, 1], "AB")],
                                  caption=("Alla ettor täckta: X = AB + C.",)))

# ----------------------------------------------------------------------------------------
# A.5: groups across the edges and in the corners.
# ----------------------------------------------------------------------------------------
WRAP3 = legend_map(from_ones("ABC", [0, 1, 4, 5, 7],
                              groups=[Group([0, 3], [0, 1], "B'"), Group([2, 3], [1], "AC")],
                              caption=("Översta och nedersta raden är grannar:",
                                       "X = B' + AC.")))
CORNERS = legend_map(from_ones("ABCD", [0, 2, 5, 7, 8, 10, 13, 15],
                                groups=[Group([0, 3], [0, 3], "B'D'"),
                                        Group([1, 2], [1, 2], "BD")],
                                caption=("De fyra hörnen är en grupp om fyra: X = B'D' + BD.",)))

# ----------------------------------------------------------------------------------------
# A.6: don't care. A BCD digit 0-9 on ABCD; X = 1 when the digit is at least 5.
# ----------------------------------------------------------------------------------------
DONT_CARE = legend_map(from_ones("ABCD", [5, 6, 7, 8, 9], dont_care=range(10, 16),
                                  groups=[Group([2, 3], [0, 1, 2, 3], "A"),
                                          Group([1, 2], [1, 2], "BD"),
                                          Group([1, 2], [2, 3], "BC")],
                                  caption=("X = siffran är minst 5. Kombinationerna 10-15 finns",
                                           "aldrig i BCD och får räknas som ettor: X = A + BD + BC.")))

# ----------------------------------------------------------------------------------------
# A.7: the worked synthesis example, three tank sensors voting (majority), and its network.
# A.8 reuses the same map as the full adder's carry.
# ----------------------------------------------------------------------------------------
MAJORITY = legend_map(from_ones("ABC", [3, 5, 6, 7],
                                 groups=[Group([1, 2], [1], "BC"), Group([2], [0, 1], "AB"),
                                         Group([2, 3], [1], "AC")],
                                 caption=("Tre grupper om två som överlappar i ABC = 111:",
                                          "X = AB + AC + BC.")))
CHECKERBOARD = legend_map(from_ones("ABC", [1, 2, 4, 7],
                                     caption=("Summan S i en heladderare: inga två ettor är",
                                              "grannar, så varje grupp blir en enda ruta.")))


def _labels(ax, points, names, dx=-0.25) -> None:
    for (x, y), name in zip(points, names):
        style.text(ax, name, (x + dx, y), halign="right")


def _draw_majority_net(d, ax) -> None:
    ab = gates.ansi(d, "and", (4.0, 3.0))
    ac = gates.ansi(d, "and", (4.0, 1.2))
    bc = gates.ansi(d, "and", (4.0, -0.6))
    x = gates.ansi(d, "or", (8.2, 1.2), inputs=3)
    rail = {"A": 0.0, "B": 0.6, "C": 1.2}
    top, bottom = 3.9, -1.2
    for name, rx in rail.items():
        gates.wire(ax, [(rx, top), (rx, bottom)])
        style.text(ax, name, (rx, top + 0.3), valign="bottom")
    for gate, (first, second) in ((ab, "AB"), (ac, "AC"), (bc, "BC")):
        for pin, name in zip(gate.inputs, (first, second)):
            gates.wire(ax, [(rail[name], pin[1]), pin])
            gates.dot(ax, (rail[name], pin[1]))
    for gate, pin in zip((ab, ac, bc), x.inputs):
        gates.wire(ax, [gate.out, (5.2, gate.out[1]), (5.2, pin[1]), pin])
    gates.wire(ax, [x.out, (x.out[0] + 0.5, x.out[1])])
    style.text(ax, "X", (x.out[0] + 0.7, x.out[1]), halign="left")


MAJORITY_NET = style.Figure(_draw_majority_net, (-0.8, -1.8, 9.8, 4.6))


def _draw_and_or(d, ax) -> None:
    a = gates.ansi(d, "and", (3.0, 1.0))
    o = gates.ansi(d, "or", (6.0, 0.45))
    gates.wire(ax, [a.out, (a.out[0] + 0.3, a.out[1]), (a.out[0] + 0.3, o.inputs[0][1]),
                    o.inputs[0]])
    gates.wire(ax, [(0, o.inputs[1][1]), o.inputs[1]])
    for (x, y) in a.inputs:
        gates.wire(ax, [(0, y), (x, y)])
    _labels(ax, [(0, a.inputs[0][1]), (0, a.inputs[1][1]), (0, o.inputs[1][1])], "ABC")
    gates.wire(ax, [o.out, (o.out[0] + 0.4, o.out[1])])
    style.text(ax, "X", (o.out[0] + 0.6, o.out[1]), halign="left")
    style.text(ax, "AND + OR: 2 grindar, 2 kretsar", (3.2, -1.1), size=style.SMALL_SIZE,
               color=style.MUTED_COLOR)


AND_OR = style.Figure(_draw_and_or, (-1.0, -1.7, 7.6, 2.0))


def _draw_nand_nand(d, ax) -> None:
    n1 = gates.ansi(d, "nand", (3.2, 1.2))
    n2 = gates.ansi(d, "nand", (3.2, -0.4))
    n3 = gates.ansi(d, "nand", (6.6, 0.4))
    for (x, y) in n1.inputs:
        gates.wire(ax, [(0, y), (x, y)])
    cy = (n2.inputs[0][1] + n2.inputs[1][1]) / 2
    gates.wire(ax, [(0, cy), (n2.inputs[0][0] - 0.35, cy)])
    gates.wire(ax, [(n2.inputs[0][0] - 0.35, n2.inputs[0][1]),
                    (n2.inputs[0][0] - 0.35, n2.inputs[1][1])])
    for pin in n2.inputs:
        gates.wire(ax, [(pin[0] - 0.35, pin[1]), pin])
    gates.dot(ax, (n2.inputs[0][0] - 0.35, cy))
    for src, pin in ((n1, n3.inputs[0]), (n2, n3.inputs[1])):
        gates.wire(ax, [src.out, (4.0, src.out[1]), (4.0, pin[1]), pin])
    _labels(ax, [(0, n1.inputs[0][1]), (0, n1.inputs[1][1]), (0, cy)], "ABC")
    style.text(ax, "(AB)'", (3.6, n1.out[1] + 0.3), size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    style.text(ax, "C'", (3.6, n2.out[1] - 0.3), size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    gates.wire(ax, [n3.out, (n3.out[0] + 0.4, n3.out[1])])
    style.text(ax, "X", (n3.out[0] + 0.6, n3.out[1]), halign="left")
    style.text(ax, "enbart NAND: 3 grindar, 1 krets", (3.6, -1.5), size=style.SMALL_SIZE,
               color=style.MUTED_COLOR)


NAND_NAND = style.Figure(_draw_nand_nand, (-1.0, -2.1, 8.2, 2.0))


def _draw_nor_nor(d, ax) -> None:
    n1 = gates.ansi(d, "nor", (3.2, 1.2))
    n2 = gates.ansi(d, "nor", (3.2, -0.4))
    n3 = gates.ansi(d, "nor", (6.6, 0.4))
    a_pin, c1_pin = n1.inputs
    c2_pin, b_pin = n2.inputs
    gates.wire(ax, [(0, a_pin[1]), a_pin])
    gates.wire(ax, [(0, b_pin[1]), b_pin])
    # C sits between the gates and feeds both: one rail, two taps, no crossings.
    c_y = (c1_pin[1] + c2_pin[1]) / 2
    c_x = 0.6
    gates.wire(ax, [(0, c_y), (c_x, c_y)])
    gates.wire(ax, [c1_pin, (c_x, c1_pin[1]), (c_x, c2_pin[1]), c2_pin])
    gates.dot(ax, (c_x, c_y))
    for src, pin in ((n1, n3.inputs[0]), (n2, n3.inputs[1])):
        gates.wire(ax, [src.out, (4.0, src.out[1]), (4.0, pin[1]), pin])
    _labels(ax, [(0, a_pin[1]), (0, b_pin[1]), (0, c_y)], "ABC")
    style.text(ax, "(A+C)'", (3.6, n1.out[1] + 0.3), size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    style.text(ax, "(B+C)'", (3.6, n2.out[1] - 0.3), size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    gates.wire(ax, [n3.out, (n3.out[0] + 0.4, n3.out[1])])
    style.text(ax, "X", (n3.out[0] + 0.6, n3.out[1]), halign="left")
    style.text(ax, "enbart NOR: 3 grindar, 1 krets", (3.6, -1.5), size=style.SMALL_SIZE,
               color=style.MUTED_COLOR)


NOR_NOR = style.Figure(_draw_nor_nor, (-1.0, -2.1, 8.2, 2.0))


def _draw_xor_nand(d, ax) -> None:
    n1 = gates.ansi(d, "nand", (3.8, 0.2))
    n2 = gates.ansi(d, "nand", (7.4, 1.3))
    n3 = gates.ansi(d, "nand", (7.4, -0.9))
    n4 = gates.ansi(d, "nand", (10.8, 0.2))
    a_y, b_y = n2.inputs[0][1], n3.inputs[1][1]
    a_x, b_x = 0.5, 0.9
    gates.wire(ax, [(0, a_y), n2.inputs[0]])
    gates.wire(ax, [(0, b_y), n3.inputs[1]])
    gates.wire(ax, [(a_x, a_y), (a_x, n1.inputs[0][1]), n1.inputs[0]])
    gates.wire(ax, [(b_x, b_y), (b_x, n1.inputs[1][1]), n1.inputs[1]])
    gates.dot(ax, (a_x, a_y))
    gates.dot(ax, (b_x, b_y))
    mid = 4.4
    gates.wire(ax, [n1.out, (mid, n1.out[1])])
    gates.wire(ax, [n2.inputs[1], (mid, n2.inputs[1][1]), (mid, n3.inputs[0][1]), n3.inputs[0]])
    gates.dot(ax, (mid, n1.out[1]))
    for src, pin in ((n2, n4.inputs[0]), (n3, n4.inputs[1])):
        gates.wire(ax, [src.out, (8.0, src.out[1]), (8.0, pin[1]), pin])
    _labels(ax, [(0, a_y), (0, b_y)], "AB")
    style.text(ax, "(AB)'", (mid + 0.1, n1.out[1] + 0.3), halign="left", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    gates.wire(ax, [n4.out, (n4.out[0] + 0.4, n4.out[1])])
    style.text(ax, "X = A xor B", (n4.out[0] + 0.6, n4.out[1]), halign="left")


XOR_NAND = style.Figure(_draw_xor_nand, (-1.0, -1.9, 14.6, 2.4))

# ----------------------------------------------------------------------------------------
# A.10: product of sums, by grouping the zeros of the worked example.
# ----------------------------------------------------------------------------------------
ZEROS = legend_map(Kmap("ABC", {0: "0", 2: "0", 4: "0", 1: "1", 3: "1", 5: "1", 6: "1",
                                 7: "1"}, show_zeros=True,
                         groups=[Group([0, 1], [0], "(A + C)"), Group([0, 3], [0], "(B + C)")],
                         caption=("Grupperna ringar in nollor. Varje grupp ger en OR-term:",
                                  "X = (A + C)(B + C), samma funktion som AB + C.")))

# ----------------------------------------------------------------------------------------
# B.4-B.5: a switch into a gate input, and an LED on a gate output.
# ----------------------------------------------------------------------------------------


def _draw_io(d, ax) -> None:
    # Input side: 5 V -> switch -> node -> gate input; node -> 10 kOhm -> GND.
    node = (3.2, 0.0)
    d.add(elm.Switch().at((0.0, 3.4)).down().label("S1", loc="bottom", ofst=0.2))
    d.add(elm.Vdd().at((0.0, 3.4)).label("5 V"))
    gates.wire(ax, [(0.0, 0.4), (0.0, 0.0), node])
    d.add(elm.Resistor().at((1.6, 0.0)).down().label("10 kΩ", loc="bottom"))
    d.add(elm.Ground().at((1.6, -3.0)))
    gates.dot(ax, (1.6, 0.0))
    g = gates.ansi(d, "and", (7.0, 0.0))
    gates.wire(ax, [node, (g.inputs[0][0] - 0.4, 0.0), (g.inputs[0][0] - 0.4, g.inputs[0][1]),
                    g.inputs[0]])
    gates.wire(ax, [(g.inputs[1][0] - 1.0, g.inputs[1][1]), g.inputs[1]])
    style.text(ax, "B", (g.inputs[1][0] - 1.15, g.inputs[1][1]), halign="right",
               size=style.SMALL_SIZE)
    style.text(ax, "A", (node[0] + 0.1, 0.25), halign="left", valign="bottom",
               size=style.SMALL_SIZE)
    # Output side: gate -> 330 Ohm -> LED -> GND.
    d.add(elm.Resistor().at((7.5, 0.0)).right().label("330 Ω", loc="top"))
    gates.wire(ax, [g.out, (7.5, 0.0)])
    d.add(elm.LED().at((10.5, 0.0)).right().label("lysdiod", loc="top"))
    gates.wire(ax, [(13.5, 0.0), (14.2, 0.0)])
    d.add(elm.Ground().at((14.2, 0.0)))
    style.text(ax, "Y", (7.35, 0.25), halign="left", valign="bottom", size=style.SMALL_SIZE)
    shapes.dashed_box(ax, 3.9, -1.3, 7.15, 1.6, "74HC08")
    style.caption(ax, ("Släppt S1: motståndet drar A till 0 V (logisk 0). Tryckt S1: A = 5 V (1).",
                       "Ingång B kopplas likadant, med en egen knapp och ett eget motstånd.",
                       "Motståndet på utgången begränsar strömmen genom lysdioden."),
                  7.0, -3.9)


IO_CIRCUIT = style.Figure(_draw_io, (-2.2, -5.6, 15.6, 4.8))

# ----------------------------------------------------------------------------------------
# B.6: the breadboard, schematically.
# ----------------------------------------------------------------------------------------


def _draw_breadboard(d, ax) -> None:
    cols = 24
    pitch = 0.6
    hole = 0.22
    rows_top = "jihgf"
    rows_bottom = "edcba"
    width = (cols + 1) * pitch
    # The board starts well left of the first column, so the row letters and rail signs sit on
    # the board instead of on its border.
    ax.add_patch(Rectangle((-1.1, -5.6), width + 1.3, 11.0, facecolor="#f7f3ea",
                           edgecolor=style.LINE_COLOR, lw=style.BOX_WIDTH))

    def holes(y, highlight=()):
        for c in range(cols):
            x = c * pitch
            fill = "#f4d7d7" if c in highlight else "white"
            ax.add_patch(Rectangle((x - hole / 2, y - hole / 2), hole, hole, facecolor=fill,
                                   edgecolor=style.MUTED_COLOR, lw=0.8))

    # Power rails, top and bottom: two rows each, connected along the whole length. The + rail
    # of each pair is the one nearest the terminal strips, so no supply wire crosses a rail.
    for y, colour, sign, line in ((4.1, style.ACCENT_COLOR, "+", 3.8),
                                  (4.7, style.ACCENT_COLOR_2, "-", 5.0),
                                  (-4.1, style.ACCENT_COLOR_2, "-", -3.8),
                                  (-4.7, style.ACCENT_COLOR, "+", -5.0)):
        holes(y)
        ax.plot([-0.3, (cols - 1) * pitch + 0.3], [line, line], color=colour, lw=1.5)
        style.text(ax, sign, (-0.45, y), halign="right", size=style.SMALL_SIZE, color=colour)
    # Terminal strips: five holes per column on each side of the centre gap.
    for i, r in enumerate(rows_top):
        holes(2.9 - i * pitch)
        style.text(ax, r, (-0.45, 2.9 - i * pitch), halign="right", size=style.TINY_SIZE,
                   color=style.MUTED_COLOR)
    for i, r in enumerate(rows_bottom):
        holes(-0.5 - i * pitch)
        style.text(ax, r, (-0.45, -0.5 - i * pitch), halign="right", size=style.TINY_SIZE,
                   color=style.MUTED_COLOR)
    for c in range(0, cols, 5):
        style.text(ax, str(c + 1), (c * pitch, 3.35), size=style.TINY_SIZE,
                   color=style.MUTED_COLOR)
    # One connected column, outlined, and named in the empty centre gap above it.
    c = 2
    ax.add_patch(Rectangle((c * pitch - 0.2, -0.5 - 4 * pitch - 0.2), 0.4, 4 * pitch + 0.4,
                           fill=False, edgecolor=style.ACCENT_COLOR, lw=2.0, zorder=5))
    style.text(ax, "kolumn 3, a-e: fem förbundna hål", (c * pitch - 0.25, 0.0),
               halign="left", size=style.TINY_SIZE, color=style.ACCENT_COLOR)
    # An IC straddling the gap, pins 1-7 in row e, pins 14-8 in row f.
    first = 12
    ax.add_patch(Rectangle((first * pitch - 0.3, -0.7), 6 * pitch + 0.6, 1.4,
                           facecolor="#303030", edgecolor=style.LINE_COLOR, zorder=4))
    ax.add_patch(Circle((first * pitch - 0.1, 0.0), 0.12, color="white", zorder=5))
    # Drawn with ax.text directly, above the package, which style.text would draw beneath.
    for label, x, y, colour in (("74HC08", first + 3, 0.0, "white"),
                                ("1", first, -0.42, "#ffb0b0"), ("14", first, 0.42, "#ffb0b0"),
                                ("7", first + 6, -0.42, "#ffb0b0"),
                                ("8", first + 6, 0.42, "#ffb0b0")):
        ax.text(x * pitch + (0.15 if label in ("1", "14") else 0.0), y, label,
                fontsize=style.TINY_SIZE, family=style.FONT, color=colour, ha="center",
                va="center", zorder=7)
    # Supply wires: pin 14 to +, pin 7 to -.
    ax.plot([first * pitch, first * pitch], [2.9, 4.1], color=style.ACCENT_COLOR, lw=3, zorder=6)
    ax.plot([(first + 6) * pitch, (first + 6) * pitch], [-0.5 - 4 * pitch, -4.1],
            color=style.ACCENT_COLOR_2, lw=3, zorder=6)
    style.caption(ax, ("Matningsskenorna går längs hela kanten; hålen i mitten är förbundna fem och",
                       "fem i kolumner. Kretsen sitter över mittspåret, så att varje ben får en egen",
                       "kolumn. Ben 14 går till +5 V och ben 7 till jord."),
                  width / 2 - 0.5, -6.0)


BREADBOARD = style.Figure(_draw_breadboard, (-2.0, -7.9, 15.8, 5.9))

# ----------------------------------------------------------------------------------------
# Exercise solutions.
# ----------------------------------------------------------------------------------------
SOL_2VAR = legend_map(from_ones("AB", [1, 3], groups=[Group([0, 1], [1], "B")],
                                 caption=("X = B",)))
SOL_3VAR_B = legend_map(from_ones("ABC", [0, 1, 4, 5], groups=[Group([0, 3], [0, 1], "B'")],
                                   caption=("X = B'",)))
SOL_3VAR_XNOR = legend_map(from_ones("ABC", [0, 2, 5, 7],
                                      groups=[Group([0, 1], [0], "A'C'"), Group([2, 3], [1], "AC")],
                                      caption=("X = A'C' + AC",)))
SOL_X = legend_map(from_ones("ABCD", [4, 5, 6, 7, 8, 9, 10, 11],
                              groups=[Group([1], [0, 1, 2, 3], "A'B"),
                                      Group([3], [0, 1, 2, 3], "AB'")],
                              caption=("X = A'B + AB'",)))
SOL_Y = legend_map(from_ones("ABCD", [0, 3, 4, 7, 8, 11, 12, 15],
                              groups=[Group([0, 1, 2, 3], [0], "C'D'"),
                                      Group([0, 1, 2, 3], [2], "CD")],
                              caption=("Y = C'D' + CD",)))
SOL_CORNERS = legend_map(from_ones("ABCD", [0, 2, 8, 10, 15],
                                    groups=[Group([0, 3], [0, 3], "B'D'"),
                                            Group([2], [2], "ABCD")],
                                    caption=("X = B'D' + ABCD",)))
SOL_SEGMENT_E = legend_map(from_ones("ABCD", [0, 2, 6, 8], dont_care=range(10, 16),
                                      groups=[Group([0, 3], [0, 3], "B'D'"),
                                              Group([0, 1, 2, 3], [3], "CD'")],
                                      caption=("e = B'D' + CD'",)))
SOL_FAN = legend_map(Kmap("TWCB", {m: "1" for m in (2, 6, 8, 10, 14)},
                           groups=[Group([0, 1, 2, 3], [3], "CB'"), Group([3], [0, 3], "TW'B'")],
                           caption=("F = TW'B' + CB'",)))
SOL_MUX = legend_map(Kmap("SAB", {m: "1" for m in (1, 3, 6, 7)},
                           groups=[Group([0, 1], [1], "S'B"), Group([2], [0, 1], "SA")],
                           caption=("X = S'B + SA",)))

SOL_CHECK = legend_map(from_ones("ABCD", [1, 3, 5, 7, 9, 11],
                                groups=[Group([0, 1], [1, 2], "A'D"),
                                        Group([0, 3], [1, 2], "B'D")],
                                caption=("X = A'D + B'D = D(A' + B')",)))

FIGURES = {
    "l04_kmap_layout2": (LAYOUT2, [L04 / "kmap_layout2.png"]),
    "l04_kmap_layout3": (LAYOUT3, [L04 / "kmap_layout3.png"]),
    "l04_kmap_layout4": (LAYOUT4, [L04 / "kmap_layout4.png"]),
    "l04_kmap_example_filled": (EX_FILLED, [L04 / "kmap_example_filled.png"]),
    "l04_kmap_example_group_c": (EX_GROUP_C, [L04 / "kmap_example_group_c.png"]),
    "l04_kmap_example_groups": (EX_GROUPS, [L04 / "kmap_example_groups.png"]),
    "l04_kmap_wrap3": (WRAP3, [L04 / "kmap_wrap3.png"]),
    "l04_kmap_corners": (CORNERS, [L04 / "kmap_corners.png"]),
    "l04_kmap_dont_care": (DONT_CARE, [L04 / "kmap_dont_care.png"]),
    "l04_kmap_majority": (MAJORITY, [L04 / "kmap_majority.png"]),
    "l04_kmap_checkerboard": (CHECKERBOARD, [L04 / "kmap_checkerboard.png"]),
    "l04_kmap_zeros": (ZEROS, [L04 / "kmap_zeros.png"]),
    "l04_net_majority": (MAJORITY_NET, [L04 / "net_majority.png"]),
    "l04_net_and_or": (AND_OR, [L04 / "net_and_or.png"]),
    "l04_net_nand_nand": (NAND_NAND, [L04 / "net_nand_nand.png"]),
    "l04_net_nor_nor": (NOR_NOR, [L04 / "net_nor_nor.png"]),
    "l04_net_xor_nand": (XOR_NAND, [L04 / "net_xor_nand.png", LAB2 / "net_xor_nand.png"]),
    "l04_io_circuit": (IO_CIRCUIT, [L04 / "io_circuit.png", LAB2 / "io_circuit.png"]),
    "l04_breadboard": (BREADBOARD, [L04 / "breadboard.png", LAB2 / "breadboard.png"]),
    "l04_sol_2var": (SOL_2VAR, [L04 / "sol_2var.png"]),
    "l04_sol_3var_b": (SOL_3VAR_B, [L04 / "sol_3var_b.png"]),
    "l04_sol_3var_xnor": (SOL_3VAR_XNOR, [L04 / "sol_3var_xnor.png"]),
    "l04_sol_x": (SOL_X, [L04 / "sol_x.png"]),
    "l04_sol_y": (SOL_Y, [L04 / "sol_y.png"]),
    "l04_sol_corners": (SOL_CORNERS, [L04 / "sol_corners.png"]),
    "l04_sol_segment_e": (SOL_SEGMENT_E, [L04 / "sol_segment_e.png"]),
    "l04_sol_fan": (SOL_FAN, [L04 / "sol_fan.png"]),
    "l04_sol_mux": (SOL_MUX, [L04 / "sol_mux.png"]),
    "l04_sol_check": (SOL_CHECK, [L04 / "sol_check.png"]),
}

# The pinouts are embedded by both L04 and the Labb 2 guide; the XOR circuit only by L04.
for _number in ("00", "02", "04", "08", "32", "86"):
    _targets = [L04 / f"dip_74hc{_number}.png"]
    if _number != "86":
        _targets.append(LAB2 / f"dip_74hc{_number}.png")
    FIGURES[f"l04_dip_74hc{_number}"] = (dip.figure(_number), _targets)
