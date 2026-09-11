"""Flowcharts (flödesplaner), with the symbols from ISO 5807 the course uses.

* `terminal`: start and stop, a rounded box.
* `process`: something the program does, a rectangle.
* `decision`: a question with a yes and a no exit, a diamond.
* `io`: reading an input or writing an output, a parallelogram.
* `call`: a subroutine call, a rectangle with a double line at each end.

Nodes are placed by hand at explicit centres, as in the assembly course's flow diagrams: a
flowchart is read in a fixed order and where a box sits carries meaning. Edges leave and enter
through the midpoint of a named side and may pass through explicit waypoints, so a loop back to
the top is drawn the way it would be drawn by hand, down, across and up, never diagonally.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

import style

NODE_W = 4.2
NODE_H = 1.1
DECISION_W = 4.6
DECISION_H = 1.7
LINE_STEP = 0.40      # Between two lines of text inside a node.
LABEL_GAP = 0.18      # Between an edge and its label.
MARGIN = 0.45
CAPTION_DROP = 0.6


@dataclass(frozen=True)
class Node:
    """One symbol: its kind, its text (one string per line), and its centre."""

    kind: str
    text: Sequence[str]
    pos: tuple[float, float]
    width: float | None = None
    height: float | None = None
    fill: str = "plain"

    @property
    def size(self) -> tuple[float, float]:
        if self.kind == "decision":
            return self.width or DECISION_W, self.height or DECISION_H
        return self.width or NODE_W, self.height or max(NODE_H, 0.55 + LINE_STEP * len(self.text))

    def side(self, name: str) -> tuple[float, float]:
        """The midpoint of one side: top, bottom, left or right."""
        x, y = self.pos
        w, h = self.size
        return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
                "left": (x - w / 2, y), "right": (x + w / 2, y)}[name]

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        x, y = self.pos
        w, h = self.size
        return x - w / 2, y - h / 2, x + w / 2, y + h / 2


@dataclass(frozen=True)
class Edge:
    """One arrow from node `src` to node `dst`, by index, leaving and entering by named sides."""

    src: int
    dst: int
    src_side: str = "bottom"
    dst_side: str = "top"
    via: Sequence[tuple[float, float]] = ()
    label: str = ""        # "Ja" or "Nej" on a decision's exits; written near the start.


def _node(ax, node: Node) -> None:
    x, y = node.pos
    w, h = node.size
    face = style.FILLS[node.fill]
    kw = dict(facecolor=face, edgecolor=style.LINE_COLOR, lw=style.BOX_WIDTH, zorder=3)
    if node.kind == "terminal":
        # The full declared width, ends rounded inside it, so an edge entering from the side
        # meets the box where `side()` says the side is.
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle=f"round,pad=0,rounding_size={h / 2}", **kw))
    elif node.kind == "process":
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, **kw))
    elif node.kind == "call":
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, **kw))
        for edge in (x - w / 2 + 0.22, x + w / 2 - 0.22):
            ax.plot([edge, edge], [y - h / 2, y + h / 2], color=style.LINE_COLOR,
                    lw=style.CELL_WIDTH, zorder=4)
    elif node.kind == "io":
        slant = 0.35
        ax.add_patch(Polygon([(x - w / 2 + slant, y + h / 2), (x + w / 2 + slant, y + h / 2),
                              (x + w / 2 - slant, y - h / 2), (x - w / 2 - slant, y - h / 2)],
                             closed=True, **kw))
    elif node.kind == "decision":
        ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                             closed=True, **kw))
    else:
        raise ValueError(f"unknown flowchart symbol {node.kind!r}")

    first = y + (len(node.text) - 1) * LINE_STEP / 2
    for i, line in enumerate(node.text):
        style.text(ax, line, (x, first - i * LINE_STEP), size=style.SMALL_SIZE)


def _edge(ax, nodes: Sequence[Node], edge: Edge) -> None:
    start = nodes[edge.src].side(edge.src_side)
    end = nodes[edge.dst].side(edge.dst_side)
    points = [start, *edge.via, end]
    # Every leg but the last as plain wire; the last leg carries the arrowhead.
    if len(points) > 2:
        ax.plot([p[0] for p in points[:-1]], [p[1] for p in points[:-1]],
                color=style.LINE_COLOR, lw=style.WIRE_WIDTH, solid_joinstyle="miter", zorder=2)
    ax.add_patch(FancyArrowPatch(points[-2], end, arrowstyle="-|>", mutation_scale=14,
                                 color=style.LINE_COLOR, lw=style.WIRE_WIDTH, shrinkA=0,
                                 shrinkB=0, zorder=2))
    if edge.label:
        # Beside the first leg, just outside the node it leaves.
        (x0, y0), (x1, y1) = points[0], points[1]
        if abs(x1 - x0) > abs(y1 - y0):      # Horizontal first leg: label above it.
            direction = 1 if x1 > x0 else -1
            pos = (x0 + direction * 0.25, y0 + LABEL_GAP)
            style.text(ax, edge.label, pos, halign="left" if direction > 0 else "right",
                       valign="bottom", size=style.SMALL_SIZE, color=style.ACCENT_COLOR)
        else:                                 # Vertical first leg: label to its right.
            direction = 1 if y1 > y0 else -1
            pos = (x0 + LABEL_GAP, y0 + direction * 0.25)
            style.text(ax, edge.label, pos, halign="left",
                       valign="bottom" if direction > 0 else "top", size=style.SMALL_SIZE,
                       color=style.ACCENT_COLOR)


def figure(nodes: Sequence[Node], edges: Sequence[Edge],
           caption: Sequence[str] = ()) -> style.Figure:
    """A ready-to-render flowchart, sized to its symbols, waypoints and caption."""
    xs = [v for node in nodes for v in (node.bounds[0], node.bounds[2])]
    ys = [v for node in nodes for v in (node.bounds[1], node.bounds[3])]
    for edge in edges:
        for x, y in edge.via:
            xs.append(x)
            ys.append(y)
    left, right, low, high = min(xs) - 0.5, max(xs) + 0.5, min(ys), max(ys)
    # Text lines inside a node can be wider than the node; include them.
    for node in nodes:
        for line in node.text:
            half = style.text_width(line, style.SMALL_SIZE) / 2
            left, right = min(left, node.pos[0] - half), max(right, node.pos[0] + half)
    bottom = low
    if caption:
        bottom = low - CAPTION_DROP - style.caption_height(caption)
        span_left, span_right = style.caption_bounds(caption, (left + right) / 2)
        left, right = min(left, span_left), max(right, span_right)

    def draw(d, ax) -> None:
        for edge in edges:
            _edge(ax, nodes, edge)
        for node in nodes:
            _node(ax, node)
        if caption:
            style.caption(ax, caption, (min(xs) + max(xs)) / 2, low - CAPTION_DROP)

    return style.Figure(draw, (left - MARGIN, bottom - MARGIN, right + MARGIN, high + MARGIN))
