"""L09 figures: the flowchart symbols, and the flowcharts of the lecture's worked examples.

Every flowchart here is the plan of a program in lectures/L09/examples, drawn before the
program, which is the order the lecture asks the reader to work in.
"""

from __future__ import annotations

import flowchart
import paths
import style
from flowchart import Edge, Node

# ----------------------------------------------------------------------------------------
# A.1: the five symbols, side by side with their names.
# ----------------------------------------------------------------------------------------
_SYMBOLS = (
    Node("terminal", ["Start"], (0.0, 0.0), width=3.4),
    Node("process", ["r16 = 0"], (4.6, 0.0), width=3.4),
    Node("decision", ["r16 = 0?"], (9.6, 0.0), width=4.0, height=1.6),
    Node("io", ["PORTB = r16"], (14.8, 0.0), width=3.6),
    Node("call", ["delay"], (19.8, 0.0), width=3.4),
)
_NAMES = ("Start/stopp", "Process", "Beslut", "In/utmatning", "Subrutin")
_SYMBOL_CAPTION = (
    "En process gör något, ett beslut har två utgångar, ja och nej, och en in- eller",
    "utmatning läser eller skriver en port. Pilarna visar i vilken ordning det sker.")


def _draw_symbols(drawing, ax) -> None:
    for node, name in zip(_SYMBOLS, _NAMES):
        flowchart._node(ax, node)
        style.text(ax, name, (node.pos[0], -1.35), size=style.SMALL_SIZE,
                   color=style.ACCENT_COLOR)
    style.caption(ax, _SYMBOL_CAPTION, 9.9, -2.1)


_SYM_LEFT, _SYM_RIGHT = style.caption_bounds(_SYMBOL_CAPTION, 9.9)
SYMBOLS = style.Figure(
    _draw_symbols,
    (min(-1.9, _SYM_LEFT) - 0.45, -2.1 - style.caption_height(_SYMBOL_CAPTION) - 0.45,
     max(21.6, _SYM_RIGHT) + 0.45, 1.3))

# ----------------------------------------------------------------------------------------
# A.4: if-else, the heater of compare_branch.asm.
# ----------------------------------------------------------------------------------------
_IF_NODES = [
    Node("terminal", ["Start"], (0.0, 0.0)),
    Node("process", ["PB0 = utgång"], (0.0, -2.0)),
    Node("process", ["r16 = temperatur"], (0.0, -4.0)),
    Node("decision", ["r16 < 20?"], (0.0, -6.3)),
    Node("io", ["Värme på", "PB0 = 1"], (-3.4, -8.9), width=4.0),
    Node("io", ["Värme av", "PB0 = 0"], (3.4, -8.9), width=4.0),
    Node("terminal", ["Stopp"], (0.0, -11.5)),
]
IF_ELSE = flowchart.figure(
    _IF_NODES,
    [
        Edge(0, 1), Edge(1, 2), Edge(2, 3),
        Edge(3, 4, "left", "top", via=[(-3.4, -6.3)], label="Ja"),
        Edge(3, 5, "right", "top", via=[(3.4, -6.3)], label="Nej"),
        Edge(4, 6, "bottom", "top", via=[(-3.4, -10.4), (0.0, -10.4)]),
        Edge(5, 6, "bottom", "top", via=[(3.4, -10.4), (0.0, -10.4)]),
    ],
    caption=("Ett beslut med två grenar som möts igen: if-else. I programmet blir beslutet",
             "cpi och brlo, och grenen som inte hoppar slutar med ett rjmp förbi den andra."))

# ----------------------------------------------------------------------------------------
# B.1: the counting loop of count_loop.asm.
# ----------------------------------------------------------------------------------------
_LOOP_NODES = [
    Node("terminal", ["Start"], (0.0, 0.0)),
    Node("process", ["summa = 0", "räknare = 10"], (0.0, -2.1)),
    Node("io", ["PORTB = räknare"], (0.0, -4.3), width=4.6),
    Node("process", ["summa = summa + räknare"], (0.0, -6.2), width=5.6),
    Node("process", ["räknare = räknare - 1"], (0.0, -8.1), width=5.6),
    Node("decision", ["räknare = 0?"], (0.0, -10.4)),
    Node("terminal", ["Stopp"], (0.0, -12.8)),
]
COUNT_LOOP = flowchart.figure(
    _LOOP_NODES,
    [
        Edge(0, 1), Edge(1, 2), Edge(2, 3), Edge(3, 4), Edge(4, 5),
        Edge(5, 6, label="Ja"),
        Edge(5, 2, "right", "right", via=[(4.2, -10.4), (4.2, -4.3)], label="Nej"),
    ],
    caption=("En loop med ett bestämt antal varv. Räknaren räknas ned, och beslutet sist i",
             "loopen avgör om den ska gå ett varv till: i programmet dec och brne."))

# ----------------------------------------------------------------------------------------
# B.4: the nested delay of long_delay.asm.
# ----------------------------------------------------------------------------------------
_NEST_NODES = [
    Node("terminal", ["Fördröjning"], (0.0, 0.0)),
    Node("process", ["yttre = OUTER"], (0.0, -2.0)),
    Node("process", ["inre = INNER"], (0.0, -4.0)),
    Node("process", ["inre = inre - 1"], (0.0, -6.0)),
    Node("decision", ["inre = 0?"], (0.0, -8.2)),
    Node("process", ["yttre = yttre - 1"], (0.0, -10.4)),
    Node("decision", ["yttre = 0?"], (0.0, -12.6)),
    Node("terminal", ["Klar"], (0.0, -15.0)),
]
NESTED_DELAY = flowchart.figure(
    _NEST_NODES,
    [
        Edge(0, 1), Edge(1, 2), Edge(2, 3), Edge(3, 4),
        Edge(4, 5, label="Ja"),
        Edge(4, 3, "right", "right", via=[(3.4, -8.2), (3.4, -6.0)], label="Nej"),
        Edge(5, 6),
        Edge(6, 7, label="Ja"),
        Edge(6, 2, "left", "left", via=[(-3.6, -12.6), (-3.6, -4.0)], label="Nej"),
    ],
    caption=("Två loopar i varandra. Den inre loopen körs från början, INNER varv, för varje",
             "varv i den yttre. Tiden blir OUTER · (3 · INNER + 3) klockcykler."))

# ----------------------------------------------------------------------------------------
# B.6: several alternatives, the modes of menu.asm, with one common exit.
# ----------------------------------------------------------------------------------------
_STEP = 2.3
_MENU_NODES = [Node("terminal", ["Start"], (0.0, 2.3))]
_MENU_EDGES = [Edge(0, 1)]
_PATTERNS = ("0000 0000", "1111 1111", "0000 1111", "1111 0000")
for _k in range(4):
    _MENU_NODES.append(Node("decision", [f"läge = {_k}?"], (0.0, -_k * _STEP),
                            width=4.2, height=1.5))
for _k, _pattern in enumerate(_PATTERNS):
    _MENU_NODES.append(Node("process", [f"mönster = {_pattern}"], (6.6, -_k * _STEP), width=5.4))
_MENU_NODES.append(Node("process", ["mönster = 0101 0101", "(fel)"], (0.0, -4 * _STEP - 0.2),
                        width=5.4))
_MENU_NODES.append(Node("io", ["PORTB = mönster"], (0.0, -5 * _STEP - 0.9), width=4.8))
_MENU_NODES.append(Node("terminal", ["Stopp"], (0.0, -6 * _STEP - 1.3)))
_SHOW = 10
for _k in range(4):
    _MENU_EDGES.append(Edge(1 + _k, 5 + _k, "right", "left", label="Ja"))
    _MENU_EDGES.append(Edge(1 + _k, 2 + _k if _k < 3 else 9, "bottom", "top", label="Nej"))
    _MENU_EDGES.append(Edge(5 + _k, _SHOW, "right", "right",
                            via=[(10.2, -_k * _STEP), (10.2, -5 * _STEP - 0.9)]))
_MENU_EDGES.append(Edge(9, _SHOW))
_MENU_EDGES.append(Edge(_SHOW, 11))
MENU = flowchart.figure(
    _MENU_NODES, _MENU_EDGES,
    caption=("Ett flerval: en kedja av beslut, där varje ja-gren gör sitt och alla vägar möts",
             "i samma ruta. Programmet får en väg in och en väg ut."))

FIGURES = {
    "l09_symbols": (SYMBOLS, [paths.lecture("L09") / "flowchart_symbols.png"]),
    "l09_if_else": (IF_ELSE, [paths.lecture("L09") / "if_else.png"]),
    "l09_count_loop": (COUNT_LOOP, [paths.lecture("L09") / "count_loop.png"]),
    "l09_nested_delay": (NESTED_DELAY, [paths.lecture("L09") / "nested_delay.png"]),
    "l09_menu": (MENU, [paths.lecture("L09") / "menu.png"]),
}
