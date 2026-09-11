"""L06 figures: from a latch to a microcomputer.

Two halves. The first draws memory: the relay self-hold circuit from L02 next to the SR latch it
is the same thing as, the D latch, the D flip-flop's timing, and the register, shift register and
counter built from flip-flops. The second draws the machine: the adder the ALU is made of, the
microcomputer's block diagram, the instruction cycle, and the ATmega328P used from L07 on.

Every timing diagram is computed rather than drawn by hand: the latch and flip-flop outputs are
derived from the clock and D by the same rules the appendix states, so the picture cannot
disagree with the text.
"""

from __future__ import annotations

from matplotlib.patches import Polygon, Rectangle

import contacts
import flow
import gates
import paths
import shapes
import style
import waveform as wf

L06 = paths.lecture("L06")

# ----------------------------------------------------------------------------------------
# A.2: the relay self-hold circuit, again: memory built from contacts.
# ----------------------------------------------------------------------------------------


def _draw_self_hold(d, ax) -> None:
    top, bottom = 0.0, -8.4
    contacts.rail(ax, 0.8, 10.4, top, "+24 V")
    contacts.rail(ax, 0.8, 10.4, bottom, "0 V")
    # Path 1: stop (NC), then start (NO) in parallel with K1's own contact, then the coil.
    x, xk = 3.0, 5.8
    contacts.wire(ax, [(x, top), (x, -0.3)])
    y = contacts.contact(ax, x, -0.3, "nc", "S2 stopp", terminals=("11", "12"))
    contacts.wire(ax, [(x, y), (x, y - 0.4)])
    split = y - 0.4
    contacts.wire(ax, [(x, split), (xk, split)])
    contacts.dot(ax, (x, split))
    ya = contacts.contact(ax, x, split, "no", "S1 start", terminals=("13", "14"))
    yb = contacts.contact(ax, xk, split, "no", "K1", push=False)
    join = ya - 0.4
    contacts.wire(ax, [(x, ya), (x, join)])
    contacts.wire(ax, [(xk, yb), (xk, join), (x, join)])
    contacts.dot(ax, (x, join))
    y = contacts.coil(ax, x, join - 0.2, "K1")
    contacts.wire(ax, [(x, join), (x, join - 0.2)])
    contacts.wire(ax, [(x, y), (x, bottom)])
    contacts.dot(ax, (x, top))
    contacts.dot(ax, (x, bottom))
    # Path 2: K1's second contact lights the lamp.
    x2 = 8.6
    contacts.column(ax, x2, top, bottom, [("relay_no", "K1"), ("gap", 1.0), ("lamp", "H1")])
    contacts.dot(ax, (x2, top))
    contacts.dot(ax, (x2, bottom))
    style.caption(ax, _SH_CAPTION, 5.6, bottom - 0.7)


_SH_CAPTION = ("S1 drar K1, och K1:s egen kontakt håller sedan K1 dragen när S1 släpps.",
               "Först S2 bryter. Kretsen minns att S1 har tryckts: det är ett SR-lås.")
_SH_LEFT, _SH_RIGHT = style.caption_bounds(_SH_CAPTION, 5.6)
SELF_HOLD = style.Figure(_draw_self_hold, (min(-1.8, _SH_LEFT - 0.4), -10.6,
                                           max(11.6, _SH_RIGHT + 0.4), 0.8))

# ----------------------------------------------------------------------------------------
# A.3-A.4: the SR latch from two NOR gates, and the D latch built on it.
# ----------------------------------------------------------------------------------------


def _sr_core(d, ax, left_r, left_s):
    """Two cross-coupled NOR gates. Returns their pins; the caller wires R and S."""
    n1 = gates.ansi(d, "nor", (6.0, 1.6))
    n2 = gates.ansi(d, "nor", (6.0, -1.6))
    q, qn = n1.out, n2.out
    # Q feeds back to the lower gate's upper input, Q' to the upper gate's lower input.
    gates.wire(ax, [q, (8.2, q[1])])
    gates.wire(ax, [qn, (8.2, qn[1])])
    gates.wire(ax, [(6.6, q[1]), (6.6, 0.4), (3.2, 0.4), (3.2, n2.inputs[0][1]), n2.inputs[0]])
    gates.wire(ax, [(7.0, qn[1]), (7.0, -0.4), (2.8, -0.4), (2.8, n1.inputs[1][1]),
                    n1.inputs[1]])
    gates.dot(ax, (6.6, q[1]))
    gates.dot(ax, (7.0, qn[1]))
    style.text(ax, "Q", (8.4, q[1]), halign="left")
    style.text(ax, "Q'", (8.4, qn[1]), halign="left")
    return n1, n2


def _draw_sr(d, ax) -> None:
    n1, n2 = _sr_core(d, ax, 0, 0)
    gates.wire(ax, [(0.6, n1.inputs[0][1]), n1.inputs[0]])
    gates.wire(ax, [(0.6, n2.inputs[1][1]), n2.inputs[1]])
    style.text(ax, "R", (0.4, n1.inputs[0][1]), halign="right")
    style.text(ax, "S", (0.4, n2.inputs[1][1]), halign="right")
    style.text(ax, "R = reset (nollställ)   S = set (ettställ)", (4.4, -3.2),
               size=style.SMALL_SIZE, color=style.MUTED_COLOR)


SR_LATCH = style.Figure(_draw_sr, (-0.6, -3.8, 9.4, 2.8))


def _draw_d_latch(d, ax) -> None:
    n1, n2 = _sr_core(d, ax, 0, 0)
    # R = D'·en into the upper NOR, S = D·en into the lower one.
    a1 = gates.ansi(d, "and", (1.8, n1.inputs[0][1] + 0.34))
    a2 = gates.ansi(d, "and", (1.8, n2.inputs[1][1] - 0.34))
    gates.wire(ax, [a1.out, (2.2, a1.out[1]), (2.2, n1.inputs[0][1]), n1.inputs[0]])
    gates.wire(ax, [a2.out, (2.2, a2.out[1]), (2.2, n2.inputs[1][1]), n2.inputs[1]])
    style.text(ax, "R", (2.35, n1.inputs[0][1] + 0.18), halign="left", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    style.text(ax, "S", (2.35, n2.inputs[1][1] - 0.18), halign="left", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    inv = gates.ansi(d, "not", (a1.inputs[0][0] - 0.2, a1.inputs[0][1]), scale=0.9)
    d_x, en_x = -3.6, -2.9
    gates.wire(ax, [(-4.4, -0.0), (d_x, 0.0)])
    gates.wire(ax, [(d_x, 0.0), (d_x, inv.inputs[0][1]), inv.inputs[0]])
    gates.wire(ax, [inv.out, a1.inputs[0]])
    gates.wire(ax, [(d_x, 0.0), (d_x, a2.inputs[0][1]), a2.inputs[0]])
    gates.dot(ax, (d_x, 0.0))
    gates.wire(ax, [(-4.4, -0.9), (en_x, -0.9)])
    gates.wire(ax, [(en_x, a1.inputs[1][1]), (en_x, a2.inputs[1][1])])
    gates.wire(ax, [(en_x, a1.inputs[1][1]), a1.inputs[1]])
    gates.wire(ax, [(en_x, a2.inputs[1][1]), a2.inputs[1]])
    gates.dot(ax, (en_x, -0.9))
    style.text(ax, "D", (-4.6, 0.0), halign="right")
    style.text(ax, "en", (-4.6, -0.9), halign="right")


D_LATCH = style.Figure(_draw_d_latch, (-5.6, -3.3, 9.4, 3.4))

# ----------------------------------------------------------------------------------------
# A.5: a latch against a flip-flop, both driven by the same clock and D.
# ----------------------------------------------------------------------------------------
_CLK_START, _CLK_PERIOD, _CLK_COUNT, _END = 1.0, 2.0, 5, 11.0
_CLK = wf.clock(_CLK_START, _CLK_PERIOD, _CLK_COUNT, begin=0.0, end=_END)
_D = [(0.0, 0), (1.5, 1), (2.4, 0), (3.6, 1), (5.5, 0), (8.5, 1), (_END, 1)]


def _level(points, t: float) -> int:
    """The level a stepped signal holds at time t (the value set by the last point at or
    before t)."""
    value = points[0][1]
    for x, level in points:
        if x <= t:
            value = level
    return value


def _latch(clock, data) -> list[tuple[float, int]]:
    """Q of a D latch: follows D while the clock is high, holds while it is low."""
    events = sorted({x for x, _ in clock} | {x for x, _ in data})
    out, q = [(0.0, 0)], 0
    for t in events:
        if _level(clock, t) == 1:
            new = _level(data, t)
            if new != q:
                q = new
                out.append((t, q))
    out.append((_END, q))
    return out


def _flip_flop(clock, data) -> list[tuple[float, int]]:
    """Q of a rising-edge D flip-flop: takes D at each rising edge and holds it otherwise."""
    out, q = [(0.0, 0)], 0
    for (x0, l0), (x1, l1) in zip(clock, clock[1:]):
        if l0 == 0 and l1 == 1:
            new = _level(data, x1)
            if new != q:
                q = new
                out.append((x1, q))
    out.append((_END, q))
    return out


_RISES = [_CLK_START + i * _CLK_PERIOD for i in range(_CLK_COUNT)]
LATCH_VS_FLIPFLOP = wf.figure(wf.Timing(
    [wf.Signal("klocka", _CLK), wf.Signal("D", _D), wf.Signal("Q, lås", _latch(_CLK, _D)),
     wf.Signal("Q, vippa", _flip_flop(_CLK, _D))],
    marks=_RISES,
    shades=[(2, r, r + _CLK_PERIOD / 2) for r in _RISES],
    notes=[(3, 6.0, "vippan ändras bara vid stigande flank")],
    caption=("Låset är genomsläppligt medan klockan är hög (skuggat) och följer D.",
             "Vippan läser D bara i ögonblicket klockan går från 0 till 1."),
    width=_END))

# A glitch between two edges: the flip-flop never sees it.
_D2 = [(0.0, 0), (1.6, 1), (4.3, 0), (4.7, 1), (7.4, 0), (_END, 0)]
DFF_TIMING = wf.figure(wf.Timing(
    [wf.Signal("klocka", _CLK), wf.Signal("D", _D2), wf.Signal("Q", _flip_flop(_CLK, _D2))],
    marks=_RISES,
    shades=[(1, 4.3, 4.7)],
    notes=[(1, 4.5, "kort dipp mellan två flanker")],
    caption=("D dippar och återhämtar sig mellan två stigande flanker. Q rör sig inte,",
             "eftersom ingen flank inträffade medan D var låg."),
    width=_END))

# ----------------------------------------------------------------------------------------
# A.5-A.8: flip-flop boxes, a register, a shift register, a counter.
# ----------------------------------------------------------------------------------------
FF_W, FF_H = 1.6, 1.8


def _ff(ax, x: float, y: float, label: str = "") -> dict[str, tuple[float, float]]:
    """A D flip-flop box with its lower-left corner at (x, y); returns its pin positions."""
    shapes.cell(ax, x, y, FF_W, FF_H, "plain", lw=style.BOX_WIDTH)
    d_pin = (x, y + FF_H * 0.72)
    q_pin = (x + FF_W, y + FF_H * 0.72)
    clk_pin = (x, y + FF_H * 0.25)
    style.text(ax, "D", (x + 0.2, d_pin[1]), halign="left", size=style.SMALL_SIZE)
    style.text(ax, "Q", (x + FF_W - 0.2, q_pin[1]), halign="right", size=style.SMALL_SIZE)
    ax.add_patch(Polygon([(x, clk_pin[1] + 0.2), (x + 0.3, clk_pin[1]), (x, clk_pin[1] - 0.2)],
                         closed=True, fill=False, edgecolor=style.LINE_COLOR,
                         lw=style.WIRE_WIDTH, zorder=3))
    if label:
        style.text(ax, label, (x + FF_W / 2, y + FF_H + 0.25), valign="bottom",
                   size=style.TINY_SIZE, color=style.MUTED_COLOR)
    return {"d": d_pin, "q": q_pin, "clk": clk_pin}


def _draw_register(d, ax) -> None:
    bus_x = 0.8
    pins = []
    for i, bit in enumerate((3, 2, 1, 0)):
        y = -i * 2.4
        p = _ff(ax, 2.0, y)
        pins.append(p)
        gates.wire(ax, [(-0.4, p["d"][1]), p["d"]])
        style.text(ax, f"D{bit}", (-0.6, p["d"][1]), halign="right", size=style.SMALL_SIZE)
        gates.wire(ax, [p["q"], (4.8, p["q"][1])])
        style.text(ax, f"Q{bit}", (5.0, p["q"][1]), halign="left", size=style.SMALL_SIZE)
        gates.wire(ax, [(bus_x, p["clk"][1]), p["clk"]])
        gates.dot(ax, (bus_x, p["clk"][1]))
    low = pins[-1]["clk"][1]
    gates.wire(ax, [(bus_x, pins[0]["clk"][1]), (bus_x, low - 0.9), (-0.4, low - 0.9)])
    style.text(ax, "klocka", (-0.6, low - 0.9), halign="right", size=style.SMALL_SIZE)
    style.caption(ax, _REG_CAPTION, 2.6, low - 1.6)


_REG_CAPTION = ("Fyra D-vippor med gemensam klocka: ett 4-bitars register.",
                "Vid varje stigande flank kopieras D3-D0 till Q3-Q0.")
_REG_LEFT, _REG_RIGHT = style.caption_bounds(_REG_CAPTION, 2.6)
REGISTER = style.Figure(_draw_register, (min(-2.8, _REG_LEFT - 0.4), -10.1,
                                         max(7.4, _REG_RIGHT + 0.4), 2.4))


def _draw_shift(d, ax) -> None:
    pitch = 3.0
    boxes = [_ff(ax, i * pitch, 0.0) for i in range(4)]
    gates.wire(ax, [(-0.9, boxes[0]["d"][1]), boxes[0]["d"]])
    style.text(ax, "in", (-1.1, boxes[0]["d"][1]), halign="right", size=style.SMALL_SIZE)
    for i, b in enumerate(boxes):
        nxt = boxes[i + 1]["d"] if i < 3 else (b["q"][0] + 0.9, b["q"][1])
        mid = b["q"][0] + 0.45
        gates.wire(ax, [b["q"], nxt] if i < 3 else [b["q"], nxt])
        gates.wire(ax, [(mid, b["q"][1]), (mid, 2.5)])
        gates.dot(ax, (mid, b["q"][1]))
        style.text(ax, f"Q{i}", (mid, 2.7), valign="bottom", size=style.SMALL_SIZE)
    bus_y = -0.7
    gates.wire(ax, [(-0.9, bus_y), (3 * pitch - 0.4, bus_y)])
    for b in boxes:
        x = b["clk"][0] - 0.4
        gates.wire(ax, [(x, bus_y), (x, b["clk"][1]), b["clk"]])
        gates.dot(ax, (x, bus_y))
    style.text(ax, "klocka", (-1.1, bus_y), halign="right", size=style.SMALL_SIZE)
    style.caption(ax, ("Varje vippas Q matar nästa vippas D. Vid varje flank flyttas alla bitar",
                       "ett steg åt höger, och en ny bit kommer in från vänster."),
                  4.8, -1.5)


SHIFT_REGISTER = style.Figure(_draw_shift, (-2.4, -3.1, 11.8, 3.4))

# A 3-bit counter, counted from the clock's rising edges.
_C_END = 17.0
_C_CLK = wf.clock(1.0, 2.0, 8, begin=0.0, end=_C_END)


def _counter_bit(bit: int) -> list[tuple[float, int]]:
    points = [(0.0, 0)]
    for n in range(1, 9):
        value = (n % 8 >> bit) & 1
        points.append((1.0 + (n - 1) * 2.0, value))
    points.append((_C_END, points[-1][1]))
    return points


COUNTER_TIMING = wf.figure(wf.Timing(
    [wf.Signal("klocka", _C_CLK), wf.Signal("Q0", _counter_bit(0)),
     wf.Signal("Q1", _counter_bit(1)), wf.Signal("Q2", _counter_bit(2))],
    marks=[1.0 + 2.0 * i for i in range(8)],
    notes=[(3, 2.0 * i, str(i % 8)) for i in range(1, 9)],
    caption=("En 3-bitars räknare: Q2 Q1 Q0 räknar 0, 1, 2 ... 7 och börjar om på 0.",
             "Q0 växlar vid varje flank, Q1 vid varannan, Q2 vid var fjärde."),
    width=_C_END))

# ----------------------------------------------------------------------------------------
# B.3: the full adder, the cell the ALU's adder is made of.
# ----------------------------------------------------------------------------------------


def _draw_full_adder(d, ax) -> None:
    x1 = gates.ansi(d, "xor", (3.2, 2.0))
    x2 = gates.ansi(d, "xor", (7.0, 1.66))
    a2 = gates.ansi(d, "and", (7.0, -0.4))
    o = gates.ansi(d, "or", (10.4, -1.07))
    a1 = gates.ansi(d, "and", (3.2, o.inputs[1][1]))
    ya, yb, yc = x1.inputs[0][1], x1.inputs[1][1], -3.0
    ax_, bx_ = 0.2, 0.6
    gates.wire(ax, [(-0.4, ya), x1.inputs[0]])
    gates.wire(ax, [(-0.4, yb), x1.inputs[1]])
    gates.wire(ax, [(ax_, ya), (ax_, a1.inputs[0][1]), a1.inputs[0]])
    gates.wire(ax, [(bx_, yb), (bx_, a1.inputs[1][1]), a1.inputs[1]])
    gates.dot(ax, (ax_, ya))
    gates.dot(ax, (bx_, yb))
    # A xor B feeds both the second XOR and the second AND.
    t = 4.0
    gates.wire(ax, [x1.out, (t, x1.out[1]), (t, x2.inputs[0][1]), x2.inputs[0]])
    gates.wire(ax, [(t, x2.inputs[0][1]), (t, a2.inputs[0][1]), a2.inputs[0]])
    gates.dot(ax, (t, x2.inputs[0][1]))
    # Carry in feeds both too.
    cx = 4.5
    gates.wire(ax, [(-0.4, yc), (cx, yc), (cx, a2.inputs[1][1]), a2.inputs[1]])
    gates.wire(ax, [(cx, a2.inputs[1][1]), (cx, x2.inputs[1][1]), x2.inputs[1]])
    gates.dot(ax, (cx, a2.inputs[1][1]))
    gates.wire(ax, [a2.out, (7.8, a2.out[1]), (7.8, o.inputs[0][1]), o.inputs[0]])
    gates.wire(ax, [a1.out, o.inputs[1]])
    gates.wire(ax, [x2.out, (11.0, x2.out[1])])
    gates.wire(ax, [o.out, (11.0, o.out[1])])
    style.text(ax, "S", (11.2, x2.out[1]), halign="left")
    style.text(ax, "Cut", (11.2, o.out[1]), halign="left")
    for y, name in ((ya, "A"), (yb, "B"), (yc, "Cin")):
        style.text(ax, name, (-0.6, y), halign="right")
    style.caption(ax, ("Heladderaren: S = A xor B xor Cin, Cut = AB + (A xor B)Cin.",
                       "Åtta sådana i rad, där varje Cut blir nästa Cin, adderar två byte."),
                  5.2, -3.6)


FULL_ADDER = style.Figure(_draw_full_adder, (-2.4, -5.0, 12.8, 3.0))

# ----------------------------------------------------------------------------------------
# B.2: the microcomputer's block diagram.
# ----------------------------------------------------------------------------------------


def _box(ax, x, y, w, h, title, detail=None, fill="plain"):
    shapes.cell(ax, x, y, w, h, fill)
    if detail:
        style.text(ax, title, (x + w / 2, y + h / 2 + 0.2), valign="bottom",
                   size=style.SMALL_SIZE)
        style.text(ax, detail, (x + w / 2, y + h / 2 - 0.2), valign="top", size=style.TINY_SIZE,
                   color=style.MUTED_COLOR)
    else:
        style.text(ax, title, (x + w / 2, y + h / 2), size=style.SMALL_SIZE)


def _bus(ax, points, colour=None):
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=colour or style.ACCENT_COLOR_2, lw=style.BUS_WIDTH,
            solid_capstyle="butt", solid_joinstyle="miter", zorder=1)


def _draw_microcomputer(d, ax) -> None:
    # The CPU, with its parts inside.
    shapes.dashed_box(ax, 0.0, 0.0, 11.0, 8.4, "CPU (centralenhet)", color=style.LINE_COLOR)
    _box(ax, 0.6, 5.2, 4.4, 1.6, "Styrenhet", "avkodar instruktionen", "accent")
    _box(ax, 0.6, 3.0, 2.1, 1.4, "PC", "nästa adress")
    _box(ax, 2.9, 3.0, 2.1, 1.4, "IR", "instruktion")
    _box(ax, 6.0, 5.2, 4.4, 1.6, "Register", "r0-r31, 32 x 8 bitar", "accent2")
    _box(ax, 6.0, 2.6, 4.4, 1.8, "ALU", "räknar och jämför", "accent2")
    _box(ax, 6.0, 0.6, 4.4, 1.3, "SREG", "flaggor: C Z N V ...")
    shapes.arrow(ax, (8.2, 5.2), (8.2, 4.45))
    shapes.arrow(ax, (8.6, 4.45), (8.6, 5.2))
    shapes.arrow(ax, (8.2, 2.6), (8.2, 1.95))
    shapes.arrow(ax, (5.0, 6.0), (6.0, 6.0), dashed=True)
    shapes.arrow(ax, (5.0, 6.5), (6.4, 4.4), dashed=True)
    style.text(ax, "styrsignaler", (5.5, 7.1), size=style.TINY_SIZE, color=style.MUTED_COLOR)
    shapes.arrow(ax, (3.95, 4.4), (3.95, 5.2))
    # Program memory, reached through the program bus from PC and IR.
    _box(ax, 0.6, -4.4, 4.4, 2.2, "Programminne", "flash: instruktionerna", "muted")
    _bus(ax, [(1.65, 3.0), (1.65, -2.2)])
    _bus(ax, [(3.95, -2.2), (3.95, 3.0)])
    style.text(ax, "adress", (1.45, -1.1), halign="right", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    style.text(ax, "instruktion", (4.15, -1.1), halign="left", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    # The data bus: registers to SRAM and to the I/O ports.
    bus_y = -1.4
    _bus(ax, [(10.4, 5.9), (11.8, 5.9), (11.8, bus_y), (6.8, bus_y)])
    _bus(ax, [(11.8, bus_y), (19.4, bus_y)])
    style.text(ax, "databuss", (15.6, bus_y + 0.3), valign="bottom", size=style.SMALL_SIZE,
               color=style.ACCENT_COLOR_2)
    _box(ax, 6.0, -4.4, 4.4, 2.2, "Dataminne", "SRAM: variabler, stack", "muted")
    _bus(ax, [(8.2, bus_y), (8.2, -2.2)])
    _box(ax, 12.8, -4.4, 3.0, 2.2, "Utport", "PORTB")
    _box(ax, 16.4, -4.4, 3.0, 2.2, "Inport", "PIND")
    _bus(ax, [(14.3, bus_y), (14.3, -2.2)])
    _bus(ax, [(17.9, bus_y), (17.9, -2.2)])
    # Pins, to the outside world.
    for x in (13.4, 14.3, 15.2):
        gates.wire(ax, [(x, -4.4), (x, -5.4)])
    shapes.arrow(ax, (14.3, -5.4), (14.3, -6.3))
    style.text(ax, "lysdioder, reläer", (14.3, -6.6), valign="top", size=style.TINY_SIZE)
    for x in (17.0, 17.9, 18.8):
        gates.wire(ax, [(x, -5.4), (x, -4.4)])
    shapes.arrow(ax, (17.9, -6.3), (17.9, -5.4))
    style.text(ax, "knappar, givare", (17.9, -6.6), valign="top", size=style.TINY_SIZE)
    # The clock drives everything.
    _box(ax, 13.4, 6.9, 4.6, 1.5, "Klocka", "16 MHz på Arduino Uno")
    shapes.arrow(ax, (13.4, 7.65), (11.0, 7.65))
    style.caption(ax, ("Styrenheten hämtar instruktioner ur programminnet, där PC pekar, och låter",
                       "ALU:n räkna med registren. Data går över databussen till minnet och portarna."),
                  9.7, -7.5)


MICROCOMPUTER = style.Figure(_draw_microcomputer, (-1.2, -9.3, 20.4, 9.2))

INSTRUCTION_CYCLE = flow.figure(
    [
        flow.Node("1. Hämta", (0.0, 3.0), "läs instruktionen där PC pekar; PC ökas", "accent",
                  width=7.4),
        flow.Node("2. Avkoda", (5.6, -1.2), "styrenheten tolkar den", width=6.0),
        flow.Node("3. Utför", (-5.6, -1.2), "ALU, register, minne, port", "accent2", width=6.0),
    ],
    [flow.Edge(0, 1), flow.Edge(1, 2), flow.Edge(2, 0)],
    caption=("Samma tre steg, om och om igen, 16 miljoner gånger i sekunden.",
             "Ett hopp i programmet är en instruktion som skriver ett nytt värde i PC."))

# ----------------------------------------------------------------------------------------
# B.9: the ATmega328P, simplified.
# ----------------------------------------------------------------------------------------


def _draw_atmega(d, ax) -> None:
    shapes.dashed_box(ax, -0.6, -4.6, 20.8, 2.9, "ATmega328P", color=style.LINE_COLOR)
    bus_y = -1.0
    _bus(ax, [(0.2, bus_y), (19.6, bus_y)])
    top = [("AVR-CPU", "32 register, ALU", "accent"), ("Flash", "32 kB program", "muted"),
           ("SRAM", "2 kB data", "muted"), ("EEPROM", "1 kB, bevaras", "muted")]
    bottom = [("Port B", "PB0-PB7", "plain"), ("Port C", "PC0-PC6", "plain"),
              ("Port D", "PD0-PD7", "plain"), ("Timrar", "3 st", "plain"),
              ("USART", "seriell", "plain"), ("ADC", "analog in", "plain")]
    for i, (name, detail, fill) in enumerate(top):
        x = 0.4 + i * 4.9
        _box(ax, x, -0.3, 4.2, 1.7, name, detail, fill)
        if name != "Flash":
            _bus(ax, [(x + 2.1, -0.3), (x + 2.1, bus_y)])
    # Harvard: the flash reaches the CPU over its own program bus, not over the data bus.
    _bus(ax, [(4.6, 0.55), (5.3, 0.55)])
    style.text(ax, "programbuss", (4.95, 1.6), valign="bottom", size=style.TINY_SIZE,
               color=style.ACCENT_COLOR_2)
    for i, (name, detail, fill) in enumerate(bottom):
        x = 0.2 + i * 3.3
        _box(ax, x, -3.9, 3.0, 1.9, name, detail, fill)
        _bus(ax, [(x + 1.5, bus_y), (x + 1.5, -2.0)])
    style.text(ax, "intern databuss", (3.35, bus_y - 0.2), valign="top",
               size=style.TINY_SIZE, color=style.ACCENT_COLOR_2)
    _box(ax, 21.4, -1.8, 3.8, 1.6, "Kristall", "16 MHz, på kortet")
    shapes.arrow(ax, (21.4, -1.0), (20.2, -1.0))
    style.caption(ax, ("Hela mikrodatorn på ett chip. Flash når CPU:n över en egen programbuss",
                       "(Harvard); SRAM, EEPROM och kringenheterna delar databussen.",
                       "På Arduino Uno sitter kristallen bredvid chipet."),
                  12.0, -5.3)


ATMEGA = style.Figure(_draw_atmega, (-1.4, -7.6, 25.8, 3.4))

# ----------------------------------------------------------------------------------------
# Exercise 3: the inputs only, and the solution with both outputs.
# ----------------------------------------------------------------------------------------
# The short pulse on D comes while the clock is high after the second edge: the latch passes it
# on, the flip-flop never sees it.
_E_D = [(0.0, 1), (0.6, 1), (2.5, 0), (3.3, 1), (3.7, 0), (6.4, 1), (_END, 1)]
EX_TIMING = wf.figure(wf.Timing(
    [wf.Signal("klocka", _CLK), wf.Signal("D", _E_D)],
    marks=_RISES,
    caption=("Rita Q för ett D-lås och för en D-vippa. Båda startar med Q = 0.",),
    width=_END))
SOL_TIMING = wf.figure(wf.Timing(
    [wf.Signal("klocka", _CLK), wf.Signal("D", _E_D), wf.Signal("Q, lås", _latch(_CLK, _E_D)),
     wf.Signal("Q, vippa", _flip_flop(_CLK, _E_D))],
    marks=_RISES,
    shades=[(2, r, r + _CLK_PERIOD / 2) for r in _RISES],
    width=_END))

FIGURES = {
    "l06_self_hold": (SELF_HOLD, [L06 / "self_hold.png"]),
    "l06_sr_latch": (SR_LATCH, [L06 / "sr_latch.png"]),
    "l06_d_latch": (D_LATCH, [L06 / "d_latch.png"]),
    "l06_latch_vs_flipflop": (LATCH_VS_FLIPFLOP, [L06 / "latch_vs_flipflop.png"]),
    "l06_dff_timing": (DFF_TIMING, [L06 / "dff_timing.png"]),
    "l06_register": (REGISTER, [L06 / "register.png"]),
    "l06_shift_register": (SHIFT_REGISTER, [L06 / "shift_register.png"]),
    "l06_counter_timing": (COUNTER_TIMING, [L06 / "counter_timing.png"]),
    "l06_full_adder": (FULL_ADDER, [L06 / "full_adder.png"]),
    "l06_microcomputer": (MICROCOMPUTER, [L06 / "microcomputer.png"]),
    "l06_instruction_cycle": (INSTRUCTION_CYCLE, [L06 / "instruction_cycle.png"]),
    "l06_atmega328p": (ATMEGA, [L06 / "atmega328p.png"]),
    "l06_ex_timing": (EX_TIMING, [L06 / "ex_timing.png"]),
    "l06_sol_timing": (SOL_TIMING, [L06 / "sol_timing.png"]),
}
