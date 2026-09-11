"""Exam figures: the network each paper's analysis question hands the candidate.

The practice exam's is a contact network and is published with it. The real exam's is a gate
network, written to exam/images/exam_network.png, and must stay out of the repository for the
same reason exam/exam.md does.
"""

from __future__ import annotations

import contacts
import gates
import paths
import style

# ----------------------------------------------------------------------------------------
# Practice exam, question 4: (S1 + S2)(S1 + S3'), which simplifies to S1 + S2S3'.
# ----------------------------------------------------------------------------------------
_TOP, _BOTTOM = 0.0, -9.6
_XA, _XB = 2.4, 5.6
_JOIN_1 = _TOP - 0.35 - contacts.CONTACT_LEN - 0.35
_JOIN_2 = _JOIN_1 - 0.35 - contacts.CONTACT_LEN - 0.35


def _draw_practice(drawing, ax) -> None:
    contacts.rail(ax, 0.8, 7.2, _TOP, "+24 V")
    contacts.rail(ax, 0.8, 7.2, _BOTTOM, "0 V")
    # First pair: S1 in parallel with S2.
    contacts.column(ax, _XA, _TOP, _JOIN_1, [("no", "S1")])
    contacts.column(ax, _XB, _TOP, _JOIN_1, [("no", "S2")])
    contacts.wire(ax, [(_XA, _JOIN_1), (_XB, _JOIN_1)])
    # Second pair: S1 (a second contact block on the same button) in parallel with S3, NC.
    contacts.column(ax, _XA, _JOIN_1, _JOIN_2, [("no", "S1")])
    contacts.column(ax, _XB, _JOIN_1, _JOIN_2, [("nc", "S3")])
    contacts.wire(ax, [(_XA, _JOIN_2), (_XB, _JOIN_2)])
    contacts.column(ax, _XA, _JOIN_2, _BOTTOM, [("gap", 0.3), ("lamp", "H1")])
    for point in ((_XA, _TOP), (_XB, _TOP), (_XA, _JOIN_1), (_XB, _JOIN_1), (_XA, _JOIN_2),
                  (_XB, _JOIN_2), (_XA, _BOTTOM)):
        contacts.dot(ax, point)


PRACTICE_CONTACTS = style.Figure(_draw_practice, (-1.6, _BOTTOM - 0.6, 8.2, _TOP + 0.6))

# ----------------------------------------------------------------------------------------
# Exam, question 4: X = A'B + AC, a two-to-one multiplexer with A as the selector.
# ----------------------------------------------------------------------------------------


def _draw_exam(drawing, ax) -> None:
    upper = gates.ansi(drawing, "and", (6.5, 1.8))
    lower = gates.ansi(drawing, "and", (6.5, -1.0))
    out = gates.ansi(drawing, "or", (10.2, 0.4))
    # The inverter sits above the AND gate's input, clear of the B wire, and steps down to it.
    a_y = upper.inputs[0][1] + 0.8
    inv = gates.ansi(drawing, "not", (2.5, a_y))
    # A goes to the inverter, and past it down to the lower AND gate.
    gates.wire(ax, [(-0.4, a_y), inv.inputs[0]])
    gates.wire(ax, [inv.out, (3.4, a_y), (3.4, upper.inputs[0][1]), upper.inputs[0]])
    gates.wire(ax, [(0.8, a_y), (0.8, lower.inputs[0][1]), lower.inputs[0]])
    gates.dot(ax, (0.8, a_y))
    style.text(ax, "A", (-0.6, a_y), halign="right")
    for pin, name in ((upper.inputs[1], "B"), (lower.inputs[1], "C")):
        gates.wire(ax, [(-0.4, pin[1]), pin])
        style.text(ax, name, (-0.6, pin[1]), halign="right")
    join = out.inputs[0][0] - 0.5
    gates.wire(ax, [upper.out, (join, upper.out[1]), (join, out.inputs[0][1]), out.inputs[0]])
    gates.wire(ax, [lower.out, (join, lower.out[1]), (join, out.inputs[1][1]), out.inputs[1]])
    gates.wire(ax, [out.out, (out.out[0] + 0.5, out.out[1])])
    style.text(ax, "X", (out.out[0] + 0.7, out.out[1]), halign="left")


EXAM_NETWORK = style.Figure(_draw_exam, (-1.4, -2.2, 11.6, 3.9))

FIGURES = {
    "exam_practice_contacts": (PRACTICE_CONTACTS, [paths.exam() / "practice_contacts.png"]),
    "exam_network": (EXAM_NETWORK, [paths.exam() / "exam_network.png"]),
}
