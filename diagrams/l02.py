"""L02 figures: logic gates, the braking assistant, and contact networks.

Most of the contact networks in L02, L03 and Labb 1 are series-parallel networks between a +24 V
rail and a 0 V rail, so this module also holds a small layout engine for them, `path()`, which
L03 and Labb 1 import. A network is described as nested tuples and the engine works out where
every contact goes:

    ("s", [a, b, c])        a, b and c in series, top to bottom
    ("p", [a, b])           a and b in parallel, side by side
    ("no", "S1")            a push-button contact; also "nc", "relay_no", "relay_nc"
    ("lamp", "H1")          a lamp; also ("coil", "K1")

Every element knows how far it reaches to the left of its wire (the push actuator and the label)
and to the right (terminal numbers, a lamp's label), so parallel branches are spaced by what they
contain rather than by a constant that is wrong for half of them.
"""

from __future__ import annotations

import schemdraw.logic as logic

import contacts as c
import gates as g
import paths
import style


def not_gate(d, out: tuple[float, float]) -> g.Pins:
    """An ANSI NOT whose drawn output lead ends exactly at `out`.

    gates.ansi() places a NOT by its `out` anchor, but schemdraw draws the NOT's leads on to its
    `start` and `end` anchors, about 0.9 units beyond the pins it reports, so a wire joined to the
    reported pin overshoots. Placing by `end` and reporting `start`/`end` avoids that.
    """
    element = d.add(logic.Not().scale(g.ANSI_SCALE).right().anchor("end").at(out))
    return g.Pins((tuple(element.absanchors["start"]),), tuple(element.absanchors["end"]))

# ----------------------------------------------------------------------------------------
# The series-parallel layout engine.
# ----------------------------------------------------------------------------------------
STEP = 0.35         # Wire between two elements in series.
JUNCTION = 0.45     # Wire between a parallel junction and the branches.
BRANCH_GAP = 0.55   # Clear space between two parallel branches.

# How far an element reaches left and right of its own wire, in canvas units.
EXTENT = {
    "no": (2.05, 0.75),
    "nc": (2.05, 0.75),
    "relay_no": (1.05, 0.75),
    "relay_nc": (1.05, 0.75),
    "lamp": (0.55, 1.35),
    "coil": (0.65, 1.45),
}
HEIGHT = {"no": c.CONTACT_LEN, "nc": c.CONTACT_LEN, "relay_no": c.CONTACT_LEN,
          "relay_nc": c.CONTACT_LEN, "lamp": c.LAMP_LEN, "coil": c.COIL_LEN}


def size(node) -> tuple[float, float, float]:
    """(left extent, right extent, height) of a node, measured from its wire."""
    kind = node[0]
    if kind == "s":
        parts = [size(child) for child in node[1]]
        return (max(p[0] for p in parts), max(p[1] for p in parts),
                sum(p[2] for p in parts) + STEP * (len(parts) - 1))
    if kind == "p":
        parts = [size(child) for child in node[1]]
        offsets = _offsets(parts)
        return (parts[0][0], offsets[-1] + parts[-1][1],
                max(p[2] for p in parts) + 2 * JUNCTION)
    left, right = EXTENT[kind]
    return left, right, HEIGHT[kind]


def _offsets(parts) -> list[float]:
    """x of each parallel branch's wire, relative to the first branch's wire."""
    offsets = [0.0]
    for previous, current in zip(parts, parts[1:]):
        offsets.append(offsets[-1] + previous[1] + BRANCH_GAP + current[0])
    return offsets


def draw(ax, node, x: float, top: float) -> float:
    """Draw a node with its wire at `x`, starting at `top`; returns the y it ends at."""
    kind = node[0]
    if kind == "s":
        y = top
        for index, child in enumerate(node[1]):
            if index:
                c.wire(ax, [(x, y), (x, y - STEP)])
                y -= STEP
            y = draw(ax, child, x, y)
        return y
    if kind == "p":
        parts = [size(child) for child in node[1]]
        offsets = _offsets(parts)
        xs = [x + offset for offset in offsets]
        height = max(p[2] for p in parts)
        upper, lower = top - JUNCTION, top - JUNCTION - height
        c.wire(ax, [(x, top), (x, upper)])
        c.wire(ax, [(xs[0], upper), (xs[-1], upper)])
        c.wire(ax, [(xs[0], lower), (xs[-1], lower)])
        c.wire(ax, [(x, lower), (x, lower - JUNCTION)])
        for branch_x, child in zip(xs, node[1]):
            end = draw(ax, child, branch_x, upper)
            c.wire(ax, [(branch_x, end), (branch_x, lower)])
        # Every junction where three wires meet gets a dot: all of them except the far corner.
        for branch_x in xs[:-1]:
            c.dot(ax, (branch_x, upper))
            c.dot(ax, (branch_x, lower))
        return lower - JUNCTION
    if kind in ("no", "nc"):
        extra = node[2] if len(node) > 2 else {}
        return c.contact(ax, x, top, kind, node[1], **extra)
    if kind in ("relay_no", "relay_nc"):
        extra = node[2] if len(node) > 2 else {}
        return c.contact(ax, x, top, kind.split("_")[1], node[1], push=False, **extra)
    if kind == "lamp":
        return c.lamp(ax, x, top, node[1])
    if kind == "coil":
        return c.coil(ax, x, top, node[1])
    raise ValueError(f"unknown network element {kind!r}")


RAIL_TOP = 0.0
LEAD = 0.45          # Wire from a rail to the first element of a path.


def path_height(node) -> float:
    """Height from the top rail to the bottom rail for one path."""
    return size(node)[2] + 2 * LEAD


def path(ax, node, x: float, top: float, bottom: float) -> None:
    """One current path from the rail at `top` to the rail at `bottom`, wire at `x`."""
    c.wire(ax, [(x, top), (x, top - LEAD)])
    end = draw(ax, node, x, top - LEAD)
    c.wire(ax, [(x, end), (x, bottom)])


def paths_figure(networks, titles=(), caption=(), gap: float = 1.2,
                 top_label: str = "+24 V", bottom_label: str = "0 V") -> style.Figure:
    """Several current paths side by side between one pair of rails.

    `networks` is a list of nodes; `titles` optional short names drawn under each path.
    The rails are as long as the paths need, and every path joins them with a dot where the rail
    continues past it.
    """
    sizes = [size(n) for n in networks]
    xs = []
    cursor = 0.0
    for index, (left, right, _) in enumerate(sizes):
        cursor += left if index == 0 else sizes[index - 1][1] + gap + left
        xs.append(cursor)
    height = max(path_height(n) for n in networks)
    bottom = RAIL_TOP - height
    rail_left = xs[0] - sizes[0][0] - 0.3
    rail_right = xs[-1] + sizes[-1][1] + 0.3
    label_w = max(style.text_width(top_label, style.SMALL_SIZE),
                  style.text_width(bottom_label, style.SMALL_SIZE))
    title_drop = 0.55 if titles else 0.0
    low = bottom - title_drop - (style.text_height(style.SMALL_SIZE) if titles else 0.0)
    left_edge, right_edge = rail_left - 0.25 - label_w, rail_right
    for x, title in zip(xs, titles):
        half = style.text_width(title, style.SMALL_SIZE) / 2
        left_edge, right_edge = min(left_edge, x - half), max(right_edge, x + half)
    if caption:
        centre = (rail_left + rail_right) / 2
        span_left, span_right = style.caption_bounds(caption, centre)
        left_edge, right_edge = min(left_edge, span_left), max(right_edge, span_right)
        caption_top = low - (0.45 if titles else 0.7)
        low = caption_top - style.caption_height(caption)

    def draw_all(d, ax) -> None:
        c.rail(ax, rail_left, rail_right, RAIL_TOP, top_label)
        c.rail(ax, rail_left, rail_right, bottom, bottom_label)
        for x, network in zip(xs, networks):
            path(ax, network, x, RAIL_TOP, bottom)
            c.dot(ax, (x, RAIL_TOP))
            c.dot(ax, (x, bottom))
        for x, title in zip(xs, titles):
            style.text(ax, title, (x, bottom - title_drop), valign="top",
                       size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
        if caption:
            style.caption(ax, caption, (rail_left + rail_right) / 2, caption_top)

    return style.Figure(draw_all, (left_edge - 0.4, low - 0.4, right_edge + 0.4, RAIL_TOP + 0.5))


# ----------------------------------------------------------------------------------------
# A.2: the gates, in both symbol standards.
# ----------------------------------------------------------------------------------------
_GATES = [
    ("not", "NOT", "X = A'"),
    ("and", "AND", "X = AB"),
    ("or", "OR", "X = A + B"),
    ("nand", "NAND", "X = (AB)'"),
    ("nor", "NOR", "X = (A + B)'"),
    ("xor", "XOR", "X = A ⊕ B"),
    ("xnor", "XNOR", "X = (A ⊕ B)'"),
]
_ROW = 2.2
_COL_NAME, _COL_ANSI, _COL_IEC, _COL_EXPR = 0.0, 5.2, 9.6, 12.3


def _draw_gate_symbols(d, ax) -> None:
    headers = ((_COL_NAME, "Grind"), (_COL_ANSI - 1.4, "ANSI"), (_COL_IEC, "IEC"),
               (_COL_EXPR + 1.8, "Uttryck"))
    for x, text in headers:
        style.text(ax, text, (x, 1.2), weight="bold", size=style.SMALL_SIZE)
    for row, (kind, name, expression) in enumerate(_GATES):
        y = -row * _ROW
        style.text(ax, name, (_COL_NAME, y), size=style.SMALL_SIZE)
        pins = g.ansi(d, kind, (_COL_ANSI, y))
        if kind == "not":
            # A one-input gate comes without leads; give it the same short ones as the others.
            g.wire(ax, [(pins.inputs[0][0] - 0.45, y), pins.inputs[0]])
            g.wire(ax, [pins.out, (pins.out[0] + 0.3, y)])
        g.iec(ax, kind, (_COL_IEC, y))
        style.text(ax, expression, (_COL_EXPR, y), halign="left", size=style.SMALL_SIZE)
    bottom = -(len(_GATES) - 1) * _ROW - 1.2
    ax.plot([-1.3, _COL_EXPR + 4.2], [0.75, 0.75], color=style.MUTED_COLOR,
            lw=style.CELL_WIDTH)
    style.caption(ax, ("Samma sju grindar i båda symbolstandarderna. CircuitVerse och de flesta",
                       "datablad använder ANSI; svenska kopplingsscheman ofta IEC."),
                  7.4, bottom - 0.2)


GATE_SYMBOLS = style.Figure(_draw_gate_symbols, (-1.6, -16.8, 17.2, 1.9))

# ----------------------------------------------------------------------------------------
# A.8: a small network to analyse. X = AB + A'C, which turns out to be a selector.
# ----------------------------------------------------------------------------------------


def _label_input(ax, name: str, start: tuple[float, float], x0: float) -> None:
    g.wire(ax, [(x0, start[1]), start])
    style.text(ax, name, (x0 - 0.25, start[1]), halign="right")


def _draw_analysis(d, ax) -> None:
    top = g.ansi(d, "and", (6.0, 2.0))
    bottom = g.ansi(d, "and", (6.0, -0.6))
    out = g.ansi(d, "or", (10.0, 0.7))
    inv_y = bottom.inputs[0][1] + 0.55
    inv = not_gate(d, (3.3, inv_y))
    x0 = -0.8
    a_y = top.inputs[0][1]
    branch = inv.inputs[0][0]
    # A feeds the upper AND directly and, through the NOT, the lower one.
    g.wire(ax, [(x0, a_y), top.inputs[0]])
    style.text(ax, "A", (x0 - 0.25, a_y), halign="right")
    g.wire(ax, [(branch, a_y), inv.inputs[0]])
    g.dot(ax, (branch, a_y))
    g.wire(ax, [inv.out, (inv.out[0], bottom.inputs[0][1]), bottom.inputs[0]])
    _label_input(ax, "B", top.inputs[1], x0)
    _label_input(ax, "C", bottom.inputs[1], x0)
    # AND outputs into the OR.
    for pins, target in ((top, out.inputs[0]), (bottom, out.inputs[1])):
        mid = (pins.out[0] + target[0]) / 2
        g.wire(ax, [pins.out, (mid, pins.out[1]), (mid, target[1]), target])
    g.wire(ax, [out.out, (out.out[0] + 0.6, out.out[1])])
    style.text(ax, "X", (out.out[0] + 0.85, out.out[1]), halign="left")
    for label, pos in (("P", (top.out[0] + 0.15, top.out[1] + 0.3)),
                       ("Q", (bottom.out[0] + 0.15, bottom.out[1] + 0.3)),
                       ("A'", (inv.out[0] - 0.55, inv.out[1] + 0.3))):
        style.text(ax, label, pos, halign="left", size=style.SMALL_SIZE,
                   color=style.ACCENT_COLOR_2)
    style.caption(ax, ("Namnge varje mellansignal, räkna ut dem rad för rad,",
                       "och läs sedan av X."), 5.0, -2.3)


ANALYSIS_NETWORK = style.Figure(_draw_analysis, (-2.0, -3.6, 12.2, 3.2))

# ----------------------------------------------------------------------------------------
# A.10: the braking assistant, B = D + (S + R)F'.
# ----------------------------------------------------------------------------------------


def _draw_adas(d, ax) -> None:
    either = g.ansi(d, "or", (4.5, 1.1))
    notf = not_gate(d, (5.2, -1.1))
    assist = g.ansi(d, "and", (8.5, 0.0))
    brake = g.ansi(d, "or", (12.5, 1.2))
    x0 = 0.0
    _label_input(ax, "S", either.inputs[0], x0)
    _label_input(ax, "R", either.inputs[1], x0)
    _label_input(ax, "F", notf.inputs[0], x0)
    d_y = 3.0
    turn = brake.inputs[0][0] - 0.45
    g.wire(ax, [(x0, d_y), (turn, d_y), (turn, brake.inputs[0][1]), brake.inputs[0]])
    style.text(ax, "D", (x0 - 0.25, d_y), halign="right")
    for pins, target in ((either, assist.inputs[0]), (notf, assist.inputs[1])):
        mid = (pins.out[0] + target[0]) / 2
        g.wire(ax, [pins.out, (mid, pins.out[1]), (mid, target[1]), target])
    mid = (assist.out[0] + brake.inputs[1][0]) / 2
    g.wire(ax, [assist.out, (mid, assist.out[1]), (mid, brake.inputs[1][1]), brake.inputs[1]])
    g.wire(ax, [brake.out, (brake.out[0] + 0.6, brake.out[1])])
    style.text(ax, "B", (brake.out[0] + 0.85, brake.out[1]), halign="left")
    style.text(ax, "S + R", (either.out[0] + 0.1, either.out[1] + 0.32), halign="left",
               size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
    style.text(ax, "F'", (notf.out[0] + 0.1, notf.out[1] - 0.32), halign="left",
               size=style.SMALL_SIZE, color=style.ACCENT_COLOR_2)
    style.text(ax, "assistansens beslut", (assist.out[0] + 0.1, assist.out[1] - 0.5),
               halign="left", valign="top", size=style.TINY_SIZE, color=style.ACCENT_COLOR_2)
    style.caption(ax, ("B = D + (S + R)F'. Förarens broms D går förbi hela assistanslogiken",
                       "och läggs in i den sista OR-grinden."), 6.8, -2.4)


ADAS_NETWORK = style.Figure(_draw_adas, (-1.0, -3.7, 14.8, 3.6))

# ----------------------------------------------------------------------------------------
# B.1: the symbols, one of each, labelled.
# ----------------------------------------------------------------------------------------


def _draw_contact_symbols(d, ax) -> None:
    top = 0.0
    entries = [
        (1.6, lambda x: c.contact(ax, x, top, "no", "S1", terminals=("13", "14")),
         ("Tryckknapp,", "slutande (NO)")),
        (5.9, lambda x: c.contact(ax, x, top, "nc", "S1", terminals=("21", "22")),
         ("Tryckknapp,", "brytande (NC)")),
        (9.3, lambda x: c.contact(ax, x, top, "no", "K1", push=False, terminals=("13", "14")),
         ("Reläkontakt,", "slutande")),
        (12.4, lambda x: c.contact(ax, x, top, "nc", "K1", push=False, terminals=("21", "22")),
         ("Reläkontakt,", "brytande")),
        (15.2, lambda x: c.lamp(ax, x, top, "H1"), ("Signallampa",)),
        (18.6, lambda x: c.coil(ax, x, top, "K1"), ("Reläspole",)),
    ]
    for x, drawer, text in entries:
        drawer(x)
        style.caption(ax, text, x, -2.35, size=style.SMALL_SIZE)


CONTACT_SYMBOLS = style.Figure(_draw_contact_symbols, (-1.0, -3.9, 20.8, 0.6))

# ----------------------------------------------------------------------------------------
# B.2-B.5: the basic connections.
# ----------------------------------------------------------------------------------------
AND_NET = ("s", [("no", "S1"), ("no", "S2"), ("lamp", "H1")])
OR_NET = ("s", [("p", [("no", "S1"), ("no", "S2")]), ("lamp", "H1")])
NOT_NET = ("s", [("nc", "S1"), ("lamp", "H1")])
NAND_NET = ("s", [("p", [("nc", "S1"), ("nc", "S2")]), ("lamp", "H1")])
NOR_NET = ("s", [("nc", "S1"), ("nc", "S2"), ("lamp", "H1")])
XOR_NET = ("s", [("p", [("s", [("no", "S1"), ("nc", "S2")]),
                        ("s", [("nc", "S1"), ("no", "S2")])]), ("lamp", "H1")])
XNOR_NET = ("s", [("p", [("s", [("no", "S1"), ("no", "S2")]),
                         ("s", [("nc", "S1"), ("nc", "S2")])]), ("lamp", "H1")])

CONTACT_BASICS = paths_figure(
    [AND_NET, OR_NET, NOT_NET],
    titles=("AND: H1 = S1·S2", "OR: H1 = S1 + S2", "NOT: H1 = S1'"),
    caption=("Serie är AND, parallell är OR, och en brytande kontakt är NOT.",
             "Lampan lyser när det finns en sluten väg från +24 V till 0 V."))

CONTACT_NAND_NOR = paths_figure(
    [NAND_NET, NOR_NET],
    titles=("NAND: H1 = S1' + S2'", "NOR: H1 = S1'·S2'"),
    caption=("De Morgan i koppar: NAND är två brytande kontakter parallellt,",
             "NOR är två brytande kontakter i serie."))

CONTACT_XOR = paths_figure(
    [XOR_NET, XNOR_NET],
    titles=("XOR: H1 = S1·S2' + S1'·S2", "XNOR: H1 = S1·S2 + S1'·S2'"),
    gap=2.0,
    caption=("Varje knapp används med både sin slutande och sin brytande kontakt.",
             "Kontakterna med samma beteckning sitter i samma knapp och påverkas samtidigt."))

# The braking assistant as contacts: S1 = D, S2 = S, S3 = R, S4 = F (a fault opens the path).
ADAS_NET = ("s", [("p", [("no", "S1"),
                         ("s", [("p", [("no", "S2"), ("no", "S3")]), ("nc", "S4")])]),
                  ("lamp", "H1")])

CONTACT_ADAS = paths_figure(
    [ADAS_NET],
    caption=("Bromsassistenten som kontaktnät: S1 förarens pedal, S2 sensorn, S3 radarn,",
             "S4 felsignalen. H1 = S1 + (S2 + S3)·S4'."))

# ----------------------------------------------------------------------------------------
# B.7: self-holding. Stop S2 (NC) in series with start S1 (NO) paralleled by K1's own contact.
# ----------------------------------------------------------------------------------------
SELF_HOLD = ("s", [("nc", "S2"), ("p", [("no", "S1"), ("relay_no", "K1")]), ("coil", "K1")])

RELAY_SELF_HOLD = paths_figure(
    [SELF_HOLD, ("s", [("relay_no", "K1"), ("lamp", "H1")])],
    titles=("Strömväg 1", "Strömväg 2"),
    gap=1.6,
    caption=("S1 = start, S2 = stopp. När K1 har dragit håller dess egen kontakt spolen",
             "strömsatt, även efter att S1 släppts. Kretsen minns att den startades."))

# ----------------------------------------------------------------------------------------
# B.8: the same self-holding circuit as a PLC ladder diagram.
# ----------------------------------------------------------------------------------------


def _draw_ladder(d, ax) -> None:
    left, right = 0.0, 8.4
    top, bottom = 1.2, -4.6
    for x in (left, right):
        c.wire(ax, [(x, top), (x, bottom)], lw=style.BOX_WIDTH)
    y1, y2, y3 = 0.0, -1.7, -3.6
    x = c.ld_contact(ax, left + 0.4, y1, "no", "S1")
    c.wire(ax, [(left, y1), (left + 0.4, y1)])
    # K1 in parallel with S1, on a branch below it.
    c.wire(ax, [(left + 0.4 - 0.0, y1), (left + 0.4, y2)])
    c.ld_contact(ax, left + 0.4, y2, "no", "K1")
    c.wire(ax, [(x, y2), (x, y1)])
    c.dot(ax, (left + 0.4, y1))
    c.dot(ax, (x, y1))
    x = c.ld_contact(ax, x, y1, "nc", "S2")
    c.wire(ax, [(x, y1), (right - 1.7, y1)])
    x = c.ld_coil(ax, right - 1.7, y1, "K1")
    c.wire(ax, [(x, y1), (right, y1)])
    x = c.ld_contact(ax, left + 0.4, y3, "no", "K1")
    c.wire(ax, [(left, y3), (left + 0.4, y3)])
    c.wire(ax, [(x, y3), (right - 1.7, y3)])
    x = c.ld_coil(ax, right - 1.7, y3, "H1")
    c.wire(ax, [(x, y3), (right, y3)])
    style.caption(ax, ("Samma självhållning som stegdiagram i ett PLC-program: strömvägarna",
                       "ligger ned, kontakterna ritas -| |- och -|/|-, utgångarna -( )-."),
                  (left + right) / 2, bottom - 0.5)


LADDER = style.Figure(_draw_ladder, (-3.2, -6.4, 11.6, 2.1))

# ----------------------------------------------------------------------------------------
# Exercise figures.
# ----------------------------------------------------------------------------------------


def _draw_ex_network(d, ax) -> None:
    """Exercise 7 (Kontroll): X = (A + B)' + BC."""
    nor = g.ansi(d, "nor", (5.0, 1.3))
    both = g.ansi(d, "and", (5.0, -1.0))
    out = g.ansi(d, "or", (9.0, 0.15))
    x0 = 0.0
    a_y = nor.inputs[0][1]
    g.wire(ax, [(x0, a_y), nor.inputs[0]])
    style.text(ax, "A", (x0 - 0.25, a_y), halign="right")
    b_y = nor.inputs[1][1]
    g.wire(ax, [(x0, b_y), nor.inputs[1]])
    style.text(ax, "B", (x0 - 0.25, b_y), halign="right")
    g.wire(ax, [(1.4, b_y), (1.4, both.inputs[0][1]), both.inputs[0]])
    g.dot(ax, (1.4, b_y))
    _label_input(ax, "C", both.inputs[1], x0)
    for pins, target in ((nor, out.inputs[0]), (both, out.inputs[1])):
        mid = (pins.out[0] + target[0]) / 2
        g.wire(ax, [pins.out, (mid, pins.out[1]), (mid, target[1]), target])
    g.wire(ax, [out.out, (out.out[0] + 0.6, out.out[1])])
    style.text(ax, "X", (out.out[0] + 0.85, out.out[1]), halign="left")


EX_NETWORK = style.Figure(_draw_ex_network, (-1.0, -2.2, 10.9, 2.4))

EX_CONTACT = paths_figure(
    [("s", [("p", [("no", "S1"), ("nc", "S2")]), ("no", "S3"), ("lamp", "H1")]),
     ("s", [("p", [("s", [("no", "S1"), ("no", "S2")]), ("nc", "S3")]), ("lamp", "H2")])],
    titles=("a)", "b)"),
    gap=2.0)

FIGURES = {
    "l02_gate_symbols": (GATE_SYMBOLS, [paths.lecture("L02") / "gate_symbols.png"]),
    "l02_analysis_network": (ANALYSIS_NETWORK, [paths.lecture("L02") / "analysis_network.png"]),
    "l02_adas_network": (ADAS_NETWORK, [paths.lecture("L02") / "adas_network.png"]),
    "l02_contact_symbols": (CONTACT_SYMBOLS, [paths.lecture("L02") / "contact_symbols.png"]),
    "l02_contact_basics": (CONTACT_BASICS, [paths.lecture("L02") / "contact_basics.png"]),
    "l02_contact_nand_nor": (CONTACT_NAND_NOR, [paths.lecture("L02") / "contact_nand_nor.png"]),
    "l02_contact_xor": (CONTACT_XOR, [paths.lecture("L02") / "contact_xor.png"]),
    "l02_contact_adas": (CONTACT_ADAS, [paths.lecture("L02") / "contact_adas.png"]),
    "l02_relay_self_hold": (RELAY_SELF_HOLD, [paths.lecture("L02") / "relay_self_hold.png"]),
    "l02_ladder": (LADDER, [paths.lecture("L02") / "ladder.png"]),
    "l02_ex_network": (EX_NETWORK, [paths.lecture("L02") / "ex_network.png"]),
    "l02_ex_contact": (EX_CONTACT, [paths.lecture("L02") / "ex_contact.png"]),
}
