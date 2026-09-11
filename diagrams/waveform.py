"""Digital timing diagrams: several signals drawn against one shared time axis.

The natural picture for anything defined by *when* it happens rather than by what it computes:
a latch against a flip-flop, a counter's bits, a blinking LED and the delay loop behind it.

A signal is a list of (x, level) points: each point sets the level held from its own x until
the next point's x, so the last point only supplies where the trace ends. `clock()` builds that
list for a square wave. Geometry only; everything visual comes from `style`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import shapes
import style

TRACE_HEIGHT = 0.85
ROW_PITCH = 1.7        # Centre-to-centre spacing between traces.
LABEL_GAP = 0.40       # Between a signal's name and the start of its trace.
MARK_DASH = (0, (3, 3))
MARGIN = 0.45
CAPTION_DROP = 0.75


@dataclass(frozen=True)
class Signal:
    """One trace: its name, its (x, level) points, and optionally a dashed style."""

    name: str
    points: Sequence[tuple[float, int]]
    dashed: bool = False


@dataclass(frozen=True)
class Timing:
    """A complete diagram: the signals top to bottom, and what to mark on them."""

    signals: Sequence[Signal]
    marks: Sequence[float] = ()                      # x of vertical dashed lines (clock edges).
    shades: Sequence[tuple[int, float, float]] = ()  # (row, x from, x to) shaded intervals.
    notes: Sequence[tuple[int, float, str]] = ()     # (row, x, text) below a trace.
    caption: Sequence[str] = ()
    width: float = 12.0                              # Where the traces end on the right.


def clock(start: float, period: float, count: int, begin: float = 0.0,
          end: float | None = None) -> list[tuple[float, int]]:
    """A clock that is low at `begin`, rises at `start` and every `period` after it."""
    points: list[tuple[float, int]] = [(begin, 0)]
    for i in range(count):
        rise = start + i * period
        points += [(rise, 1), (rise + period / 2, 0)]
    points.append((end if end is not None else start + count * period, 0))
    return points


def _row(index: int) -> tuple[float, float]:
    """(low, high) y of trace `index`, counted downwards from the top."""
    high = -index * ROW_PITCH
    return high - TRACE_HEIGHT, high


def _trace(ax, points: Sequence[tuple[float, int]], low: float, high: float,
           dashed: bool) -> None:
    xs: list[float] = []
    ys: list[float] = []
    for (x_a, level), (x_b, next_level) in zip(points, points[1:]):
        y = high if level else low
        xs += [x_a, x_b, x_b]
        ys += [y, y, high if next_level else low]
    ax.plot(xs, ys, color=style.LINE_COLOR, lw=style.WIRE_WIDTH,
            linestyle=(0, (4, 3)) if dashed else "-", solid_joinstyle="miter", clip_on=False)


def _draw(timing: Timing, drawing, ax) -> None:
    rows = len(timing.signals)
    top, bottom = 0.3, _row(rows - 1)[0] - 0.3
    for x in timing.marks:
        ax.plot([x, x], [bottom, top], color=style.ACCENT_COLOR, lw=style.ACCENT_WIDTH,
                linestyle=MARK_DASH, zorder=0)
    for row, x_a, x_b in timing.shades:
        low, high = _row(row)
        shapes.shade(ax, x_a, x_b, low, high, 0.18)
    for index, signal in enumerate(timing.signals):
        low, high = _row(index)
        style.text(ax, signal.name, (-LABEL_GAP, (low + high) / 2), halign="right")
        _trace(ax, signal.points, low, high, signal.dashed)
    for row, x, text in timing.notes:
        low, _ = _row(row)
        # On a white ground, so a dashed edge marker running behind the note cannot strike
        # through it; the marker is interrupted instead, which reads correctly.
        ax.text(x, low - 0.18, text, fontsize=style.TINY_SIZE, family=style.FONT,
                color=style.ACCENT_COLOR, ha="center", va="top", zorder=5,
                bbox=dict(facecolor=style.BACKGROUND, edgecolor="none", pad=1.5))
    if timing.caption:
        drop = 0.55 if timing.notes else 0.0
        style.caption(ax, timing.caption, timing.width / 2, bottom - drop - 0.35)


def figure(timing: Timing) -> style.Figure:
    """A ready-to-render timing diagram, with the canvas measured around its labels."""
    rows = len(timing.signals)
    names = max(style.text_width(signal.name) for signal in timing.signals)
    left, right = -LABEL_GAP - names, timing.width
    bottom = _row(rows - 1)[0] - 0.3
    if timing.notes:
        bottom -= 0.55
    if timing.caption:
        bottom -= 0.35 + style.caption_height(timing.caption)
        span_left, span_right = style.caption_bounds(timing.caption, timing.width / 2)
        left, right = min(left, span_left), max(right, span_right)
    return style.Figure(lambda d, ax: _draw(timing, d, ax),
                        (left - MARGIN, bottom - MARGIN, right + MARGIN, 0.3 + MARGIN))
