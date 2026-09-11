"""Karnaugh maps of two, three or four variables, with groups that may wrap around the edges.

A map is described by its variables and its cell values; groups are described by the rows and
columns they cover, in map order (0 is the top row, the left column). Everything else, the Gray
code labels, the cell contents, the outlines and the term each group reduces to, is derived.

Layout follows the course convention, set in L04:

* two variables: `A` down the rows, `B` across the columns.
* three variables: `AB` down the rows (Gray code 00, 01, 11, 10), `C` across.
* four variables: `AB` down the rows, `CD` across, both in Gray code.

A group that wraps around an edge is drawn as two (or four) open-ended outlines, each open on
the side that touches the edge it wraps across, which is how a group is drawn by hand.

Groups are told apart by colour *and* line style, so the distinction survives a greyscale
print. Geometry only, as always: everything visual comes from `style`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import style

GRAY1 = ("0", "1")
GRAY2 = ("00", "01", "11", "10")

# Cell size and the gaps around the grid, in canvas units.
CELL_W = 1.7
CELL_H = 1.35
VALUE_GAP = 0.45       # Gray-code labels, outside the grid.
AXIS_GAP = 1.45        # Variable names, outside the labels.
TERM_GAP = 0.40        # A group's term, right of the grid.
TERM_STEP = 0.48       # Between two terms whose groups start on the same row.
INSET = 0.16           # How far inside the cell border a group outline sits.
INSET_STEP = 0.09      # Extra inset for each further group, so overlapping outlines separate.
MINTERM_INSET = 0.30   # Inset used when minterm numbers occupy the cells' top-left corners.
MARGIN = 0.45
CAPTION_DROP = 0.65

# Inks and dash patterns for successive groups: colour and line style both change, so a
# reader who cannot tell the colours apart can still tell the groups apart.
GROUP_STYLES = (
    (style.ACCENT_COLOR, "-"),
    (style.ACCENT_COLOR_2, (0, (5, 3))),
    ("#2e7d32", (0, (1.5, 2))),
    ("#6a1b9a", (0, (6, 2, 1.5, 2))),
    (style.MUTED_COLOR, (0, (3, 3))),
)


@dataclass(frozen=True)
class Group:
    """One group: the rows and columns it covers, in map order, and the term it reduces to."""

    rows: Sequence[int]
    cols: Sequence[int]
    term: str = ""


@dataclass(frozen=True)
class Kmap:
    """A complete map: variable names, cell values by minterm number, and groups."""

    variables: str                       # "AB", "ABC" or "ABCD", MSB first.
    values: dict[int, str]               # minterm -> "1", "0" or "X"; missing cells are blank.
    groups: Sequence[Group] = ()
    caption: Sequence[str] = ()
    show_zeros: bool = False             # Write the 0s instead of leaving those cells blank.
    minterms: bool = False               # Write each cell's minterm number in its corner.
    title: str | None = None             # Output name above the map, e.g. "X".
    terms: bool = True                   # Write each group's term beside the grid.

    @property
    def row_vars(self) -> str:
        return self.variables[:1] if len(self.variables) == 2 else self.variables[:2]

    @property
    def col_vars(self) -> str:
        return self.variables[len(self.row_vars):]

    @property
    def row_codes(self) -> Sequence[str]:
        return GRAY1 if len(self.row_vars) == 1 else GRAY2

    @property
    def col_codes(self) -> Sequence[str]:
        return GRAY1 if len(self.col_vars) == 1 else GRAY2

    def minterm(self, row: int, col: int) -> int:
        """The minterm number of one cell: its row code and column code read as one binary."""
        return int(self.row_codes[row] + self.col_codes[col], 2)


def _segments(indices: Sequence[int], count: int) -> list[tuple[int, int, bool, bool]]:
    """Split a set of row (or column) indices into contiguous runs.

    Returns (first, last, open_low, open_high) per run. A run is open on its low side when the
    group wraps across that edge, i.e. the run starts at index 0 and the group also contains the
    last index, and likewise for its high side.
    """
    chosen = sorted(set(indices))
    runs: list[list[int]] = []
    for index in chosen:
        if runs and index == runs[-1][-1] + 1:
            runs[-1].append(index)
        else:
            runs.append([index])
    wraps = len(runs) > 1 and chosen[0] == 0 and chosen[-1] == count - 1
    result = []
    for run in runs:
        open_low = wraps and run[0] == 0
        open_high = wraps and run[-1] == count - 1
        result.append((run[0], run[-1], open_low, open_high))
    return result


def _draw(kmap: Kmap, drawing, ax) -> None:
    rows, cols = len(kmap.row_codes), len(kmap.col_codes)
    right, bottom = cols * CELL_W, -rows * CELL_H

    # The grid: one line per boundary.
    for i in range(rows + 1):
        ax.plot([0, right], [-i * CELL_H] * 2, color=style.LINE_COLOR, lw=style.BOX_WIDTH,
                solid_capstyle="projecting")
    for j in range(cols + 1):
        ax.plot([j * CELL_W] * 2, [0, bottom], color=style.LINE_COLOR, lw=style.BOX_WIDTH,
                solid_capstyle="projecting")

    # Gray-code values and the variable names they belong to.
    for j, code in enumerate(kmap.col_codes):
        style.text(ax, code, ((j + 0.5) * CELL_W, VALUE_GAP))
    for i, code in enumerate(kmap.row_codes):
        style.text(ax, code, (-VALUE_GAP, -(i + 0.5) * CELL_H), halign="right")
    style.title(ax, kmap.col_vars, (right / 2, AXIS_GAP))
    style.title(ax, kmap.row_vars, (-AXIS_GAP - 0.25 * len(kmap.row_vars), bottom / 2))
    if kmap.title:
        style.text(ax, kmap.title, (-AXIS_GAP - 0.3, AXIS_GAP), weight="bold",
                   size=style.TITLE_SIZE)

    # Cell contents, and optionally the minterm number in the corner.
    for i in range(rows):
        for j in range(cols):
            number = kmap.minterm(i, j)
            value = kmap.values.get(number, "0" if kmap.show_zeros else "")
            if value == "0" and not kmap.show_zeros:
                value = ""
            centre = ((j + 0.5) * CELL_W, -(i + 0.5) * CELL_H)
            if value:
                colour = style.MUTED_COLOR if value in ("0", "X") else style.LINE_COLOR
                style.text(ax, value, centre, color=colour)
            if kmap.minterms:
                style.text(ax, str(number), (j * CELL_W + 0.08, -i * CELL_H - 0.05),
                           halign="left", valign="top", size=style.TINY_SIZE,
                           color=style.MUTED_COLOR)

    # Groups, each as one outline per contiguous piece, open where it wraps.
    for index, group in enumerate(kmap.groups):
        colour, dash = GROUP_STYLES[index % len(GROUP_STYLES)]
        # Only a group that overlaps an earlier one is pulled further in, so the two outlines
        # never lie on top of each other; a group on its own keeps the base inset.
        cells = {(r, c) for r in group.rows for c in group.cols}
        overlaps = sum(1 for earlier in kmap.groups[:index]
                       if cells & {(r, c) for r in earlier.rows for c in earlier.cols})
        inset = (MINTERM_INSET if kmap.minterms else INSET) + INSET_STEP * overlaps
        for r0, r1, top_open, bottom_open in _segments(group.rows, rows):
            for c0, c1, left_open, right_open in _segments(group.cols, cols):
                x0, x1 = c0 * CELL_W + inset, (c1 + 1) * CELL_W - inset
                y0, y1 = -r0 * CELL_H - inset, -(r1 + 1) * CELL_H + inset
                # An open side reaches out to the grid edge it wraps across.
                if top_open:
                    y0 = 0.0 + 0.02
                if bottom_open:
                    y1 = bottom - 0.02
                if left_open:
                    x0 = 0.0 - 0.02
                if right_open:
                    x1 = right + 0.02
                sides = [((x0, y0), (x1, y0), top_open), ((x1, y0), (x1, y1), right_open),
                         ((x1, y1), (x0, y1), bottom_open), ((x0, y1), (x0, y0), left_open)]
                for start, end, is_open in sides:
                    if not is_open:
                        ax.plot([start[0], end[0]], [start[1], end[1]], color=colour,
                                lw=style.ACCENT_WIDTH + 0.4, linestyle=dash,
                                solid_capstyle="round", dash_capstyle="round", zorder=3)
        if kmap.terms and group.term:
            # Beside the group's first row; a second group starting on the same row gets the
            # next line down, so two terms never print on top of each other.
            first_row = min(group.rows)
            stacked = sum(1 for earlier in kmap.groups[:index]
                          if earlier.term and min(earlier.rows) == first_row)
            style.text(ax, group.term, (right + TERM_GAP, -(first_row + 0.5) * CELL_H
                                        - TERM_STEP * stacked),
                       halign="left", color=colour, size=style.FONT_SIZE)

    if kmap.caption:
        style.caption(ax, kmap.caption, right / 2, bottom - CAPTION_DROP)


def figure(kmap: Kmap) -> style.Figure:
    """A ready-to-render map, with the canvas measured around its labels and caption."""
    rows, cols = len(kmap.row_codes), len(kmap.col_codes)
    right, bottom = cols * CELL_W, -rows * CELL_H
    terms = [group.term for group in kmap.groups if group.term and kmap.terms]
    term_width = max((style.text_width(t) for t in terms), default=0.0)
    left = -AXIS_GAP - 0.25 * len(kmap.row_vars) - style.text_width(kmap.row_vars,
                                                                     style.TITLE_SIZE)
    if kmap.title:
        left = min(left, -AXIS_GAP - 0.3 - style.text_width(kmap.title, style.TITLE_SIZE))
    edge = right + (TERM_GAP + term_width if terms else 0.0)
    low = bottom
    if kmap.caption:
        low = bottom - CAPTION_DROP - style.caption_height(kmap.caption)
        span_left, span_right = style.caption_bounds(kmap.caption, right / 2)
        left, edge = min(left, span_left), max(edge, span_right)
    top = AXIS_GAP + style.text_height(style.TITLE_SIZE) / 2
    return style.Figure(lambda d, ax: _draw(kmap, d, ax),
                        (left - MARGIN, low - MARGIN, edge + MARGIN, top + MARGIN))


def from_ones(variables: str, ones: Sequence[int], dont_care: Sequence[int] = (),
              **kwargs) -> Kmap:
    """A map whose listed minterms are 1, listed don't-cares X, and everything else 0."""
    values = {m: "1" for m in ones} | {m: "X" for m in dont_care}
    return Kmap(variables, values, **kwargs)
