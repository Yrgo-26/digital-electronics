"""L11 figures: wiring the traffic light, its timing, the worked example's flowchart, a relay
driver for a 24 V lamp, and what a bouncing button looks like to the program.

The wiring and the timing are also written into the Lab 3 final task, which uses the same
pins and the same sequence.
"""

from __future__ import annotations

import schemdraw.elements as elm

import contacts
import flowchart as fc
import paths
import shapes
import style
import waveform as wf

# ----------------------------------------------------------------------------------------
# The traffic light, wired: three LEDs with series resistors, and a button to ground.
# ----------------------------------------------------------------------------------------
_CHIP_X = 0.0             # The board's right edge, where the pins leave it.
_CHIP_W = 4.2
_ROWS = ((3.6, "8", "PB0", "röd", "#c00000"),
         (1.8, "9", "PB1", "gul", "#b8860b"),
         (0.0, "10", "PB2", "grön", "#2e7d32"))
_BUTTON_Y = -2.0
_GND_Y = -3.6
_R_X = 1.0
_LED_X = 4.6
_BUS_X = 8.9
_WIRING_CAPTION = (
    "Varje lysdiod har ett eget motstånd på 220-330 Ω och går till jord (GND). Knappen",
    "kopplar stift 2 till jord; den interna pull-upen håller stiftet högt när knappen är",
    "släppt. Stift 0 och 1 används av USB-kabeln och lämnas lediga.")


def _draw_wiring(drawing, ax) -> None:
    for y, pin, port, colour_name, ink in _ROWS:
        drawing.add(elm.Line().at((_CHIP_X, y)).to((_R_X, y)))
        drawing.add(elm.Resistor().at((_R_X, y)).right().label("220 Ω", loc="top",
                                                                 fontsize=11))
        drawing.add(elm.Line().at((_R_X + 3.0, y)).to((_LED_X, y)))
        drawing.add(elm.LED().at((_LED_X, y)).right().color(ink))
        drawing.add(elm.Line().at((_LED_X + 3.0, y)).to((_BUS_X, y)))
        style.text(ax, f"{pin} ({port})", (_CHIP_X - 0.2, y), halign="right",
                   size=style.SMALL_SIZE)
        style.text(ax, colour_name, (_LED_X + 1.5, y - 0.55), valign="top",
                   size=style.SMALL_SIZE, color=ink)
    drawing.add(elm.Line().at((_CHIP_X, _BUTTON_Y)).to((_R_X + 1.5, _BUTTON_Y)))
    drawing.add(elm.Button().at((_R_X + 1.5, _BUTTON_Y)).right().label("knapp", loc="top",
                                                                        fontsize=11))
    drawing.add(elm.Line().at((_R_X + 4.5, _BUTTON_Y)).to((_BUS_X, _BUTTON_Y)))
    style.text(ax, "2 (PD2)", (_CHIP_X - 0.2, _BUTTON_Y), halign="right",
               size=style.SMALL_SIZE)
    # The ground bus: every path ends on it, and it runs back to the board's GND pin.
    drawing.add(elm.Line().at((_BUS_X, _ROWS[0][0])).to((_BUS_X, _GND_Y)))
    drawing.add(elm.Line().at((_BUS_X, _GND_Y)).to((_CHIP_X, _GND_Y)))
    for y in (_ROWS[1][0], _ROWS[2][0], _BUTTON_Y, _GND_Y):
        drawing.add(elm.Dot().at((_BUS_X, y)))
    style.text(ax, "GND", (_CHIP_X - 0.2, _GND_Y), halign="right", size=style.SMALL_SIZE)
    shapes.dashed_box(ax, _CHIP_X - _CHIP_W, _GND_Y - 0.9, _CHIP_X, _ROWS[0][0] + 1.4,
                      "Arduino Uno")
    style.caption(ax, _WIRING_CAPTION, (_CHIP_X - _CHIP_W + _BUS_X) / 2, _GND_Y - 1.5)


_W_LEFT, _W_RIGHT = style.caption_bounds(_WIRING_CAPTION, (_CHIP_X - _CHIP_W + _BUS_X) / 2)
TRAFFIC_WIRING = style.Figure(
    _draw_wiring,
    (min(_CHIP_X - _CHIP_W, _W_LEFT) - 0.5,
     _GND_Y - 1.5 - style.caption_height(_WIRING_CAPTION) - 0.5,
     max(_BUS_X + 0.5, _W_RIGHT) + 0.5, _ROWS[0][0] + 1.9))

# ----------------------------------------------------------------------------------------
# The traffic light's sequence, as a timing diagram over ten seconds.
# ----------------------------------------------------------------------------------------
_S = 1.25                 # Canvas units per second.


def _on(*intervals: tuple[float, float], end: float = 10.0) -> list[tuple[float, int]]:
    """A light that is on during each (from, to) interval in seconds, off otherwise.

    An interval reaching `end` leaves the light on to the edge of the figure, rather than
    drawing a fall at the edge that never happens.
    """
    points: list[tuple[float, int]] = [] if intervals and intervals[0][0] == 0 else [(0.0, 0)]
    for start, stop in intervals:
        points.append((start * _S, 1))
        if stop < end:
            points.append((stop * _S, 0))
    points.append((end * _S, points[-1][1]))
    return points


TRAFFIC_TIMING = wf.figure(wf.Timing(
    [wf.Signal("röd (PB0)", _on((0, 4), (8, 10))),
     wf.Signal("gul (PB1)", _on((3, 4), (7, 8))),
     wf.Signal("grön (PB2)", _on((4, 7)))],
    marks=[3 * _S, 4 * _S, 7 * _S, 8 * _S],
    notes=[(2, 0.0, "0 s"), (2, 3 * _S, "3 s"), (2, 4 * _S, "4 s"), (2, 7 * _S, "7 s"),
           (2, 8 * _S, "8 s")],
    caption=("Röd 3 s, röd och gul 1 s, grön 3 s, gul 1 s. Efter 8 s börjar",
             "cykeln om från början."),
    width=10 * _S))

# ----------------------------------------------------------------------------------------
# B.3: the road-work light's flowchart.
# ----------------------------------------------------------------------------------------
ROADWORK_FLOWCHART = fc.figure(
    [
        fc.Node("terminal", ["Start"], (0.0, 0.0)),
        fc.Node("process", ["Initiera stackpekaren", "PB0 och PB2 utgångar"], (0.0, -2.2)),
        fc.Node("io", ["Tänd röd, släck grön"], (0.0, -4.6)),
        fc.Node("call", ["Vänta 4 s (delay_s)"], (0.0, -6.7)),
        fc.Node("io", ["Tänd grön, släck röd"], (0.0, -8.8)),
        fc.Node("call", ["Vänta 4 s (delay_s)"], (0.0, -10.9)),
    ],
    [fc.Edge(0, 1), fc.Edge(1, 2), fc.Edge(2, 3), fc.Edge(3, 4), fc.Edge(4, 5),
     fc.Edge(5, 2, "bottom", "right", via=[(0.0, -12.1), (3.6, -12.1), (3.6, -4.6)])],
    caption=("Vägarbetsljuset: två tillstånd som avlöser varandra för",
             "alltid. Loopen tillbaka har inget villkor."))

# ----------------------------------------------------------------------------------------
# A.3: a relay driven from a pin, switching a 24 V lamp.
# ----------------------------------------------------------------------------------------
_RELAY_CAPTION = (
    "Stiftet orkar inte driva reläspolen själv. Transistorn gör det: en etta på PB0 slår",
    "på den, spolen drar, och reläkontakten K1 sluter 24 V-kretsen till lampan H1. Dioden",
    "tar hand om spänningstoppen när spolen släpps; utan den förstörs transistorn.")


def _draw_relay(drawing, ax) -> None:
    # The driver: pin, base resistor, transistor, coil to +5 V with a diode across it.
    bjt = drawing.add(elm.BjtNpn(circle=True).anchor("base").at((3.2, 0.0)))
    drawing.add(elm.Resistor().at((0.0, 0.0)).to((3.2, 0.0)).label("1 kΩ", loc="top",
                                                                    fontsize=11))
    style.text(ax, "PB0", (-0.25, 0.0), halign="right", size=style.SMALL_SIZE)
    collector = bjt.absanchors["collector"]
    emitter = bjt.absanchors["emitter"]
    x_coil = collector[0]
    drawing.add(elm.Ground().at(emitter))
    coil_bottom = collector[1] + 0.6
    coil_top = coil_bottom + contacts.COIL_LEN
    coil_mid = (coil_top + coil_bottom) / 2
    drawing.add(elm.Line().at(collector).to((x_coil, coil_bottom)))
    contacts.coil(ax, x_coil, coil_top, "")
    style.text(ax, "K1", (x_coil + 0.75, coil_mid + 0.55), halign="left",
               size=style.SMALL_SIZE)
    # The diode on the left of the coil, cathode up: it conducts only when the coil is
    # switched off and tries to keep its current flowing.
    diode_x = x_coil - 1.6
    drawing.add(elm.Line().at((x_coil, coil_bottom)).to((diode_x, coil_bottom)))
    drawing.add(elm.Diode().at((diode_x, coil_bottom)).to((diode_x, coil_top)))
    drawing.add(elm.Line().at((diode_x, coil_top)).to((x_coil, coil_top)))
    drawing.add(elm.Line().at((x_coil, coil_top)).to((x_coil, coil_top + 0.6)))
    drawing.add(elm.Vdd().at((x_coil, coil_top + 0.6)).label("+5 V"))
    for point in ((x_coil, coil_bottom), (x_coil, coil_top)):
        drawing.add(elm.Dot().at(point))

    # The 24 V side: the relay's contact in series with the lamp, between the two rails. The
    # rails are placed so that the contact's blade sits level with the coil, and the dashed
    # mechanical link between the two runs straight across.
    x = x_coil + 5.0
    rail_top = coil_mid + 0.35 + contacts.CONTACT_LEN / 2
    rail_bottom = rail_top - 0.35 - contacts.CONTACT_LEN - 0.35 - 0.4 - contacts.LAMP_LEN - 0.9
    contacts.rail(ax, x - 1.2, x + 1.2, rail_top, "+24 V")
    contacts.rail(ax, x - 1.2, x + 1.2, rail_bottom, "0 V")
    contacts.column(ax, x, rail_top, rail_bottom, [("relay_no", ""), ("gap", 0.4),
                                                    ("lamp", "H1")])
    style.text(ax, "K1", (x + 0.3, coil_mid + 0.1), halign="left", size=style.SMALL_SIZE)
    contacts.link(ax, (x_coil + contacts.COIL_W / 2, coil_mid), (x - 0.35, coil_mid))
    style.caption(ax, _RELAY_CAPTION, 4.6, _RELAY_CAPTION_TOP)


_RELAY_CAPTION_TOP = -3.2
_R_LEFT, _R_RIGHT = style.caption_bounds(_RELAY_CAPTION, 4.6)
RELAY_DRIVER = style.Figure(
    _draw_relay,
    (min(-1.6, _R_LEFT) - 0.4, _RELAY_CAPTION_TOP - style.caption_height(_RELAY_CAPTION) - 0.5,
     max(10.6, _R_RIGHT) + 0.5, 5.9))

# ----------------------------------------------------------------------------------------
# A.4: a bouncing button, and the program's two settle delays.
# ----------------------------------------------------------------------------------------
BOUNCE = wf.figure(wf.Timing(
    [wf.Signal("PD2", [(0.0, 1), (1.5, 0), (1.75, 1), (2.0, 0), (6.5, 1), (6.75, 0),
                       (7.0, 1), (11.0, 1)]),
     wf.Signal("räknaren", [(0.0, 0), (1.5, 1), (11.0, 1)])],
    shades=[(0, 1.5, 3.9), (0, 6.5, 8.9)],
    notes=[(0, 2.7, "väntar 20 ms"), (0, 7.7, "väntar 20 ms"), (1, 1.5, "+1")],
    caption=("En knapp studsar några millisekunder när den sluts och när den öppnas.",
             "Programmet räknar vid första nollan och tittar sedan inte på knappen på",
             "20 ms. Utan väntan hade det här trycket räknats tre gånger."),
    width=11.0))

FIGURES = {
    "l11_traffic_wiring": (TRAFFIC_WIRING, [paths.lecture("L11") / "traffic_wiring.png",
                                            paths.lab("lab3") / "traffic_wiring.png"]),
    "l11_traffic_timing": (TRAFFIC_TIMING, [paths.lecture("L11") / "traffic_timing.png",
                                            paths.lab("lab3") / "traffic_timing.png"]),
    "l11_roadwork_flowchart": (ROADWORK_FLOWCHART,
                               [paths.lecture("L11") / "roadwork_flowchart.png"]),
    "l11_relay_driver": (RELAY_DRIVER, [paths.lecture("L11") / "relay_driver.png"]),
    "l11_bounce": (BOUNCE, [paths.lecture("L11") / "bounce.png"]),
}
