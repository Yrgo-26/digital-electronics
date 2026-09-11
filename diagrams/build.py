#!/usr/bin/env python3
"""Regenerate the course figures.

    .venv/bin/python diagrams/build.py                     # every figure, into the course tree
    .venv/bin/python diagrams/build.py kmap_3var           # one figure
    .venv/bin/python diagrams/build.py --list              # what can be built
    .venv/bin/python diagrams/build.py --outdir /tmp/x     # preview, without touching the repo

Adding a figure: write a builder in a figure module (one per lecture or lab, named after it:
`l04.py`, `lab2.py`), and list it in that module's `FIGURES` dict together with every path
that should receive it. Modules are discovered, not registered: any module in this directory
that defines `FIGURES` is picked up, so two people adding figures to two lectures never edit
the same file.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import style  # noqa: E402

# Modules that hold drawing machinery rather than figures, skipped by discovery.
LIBRARY = {"build", "style", "shapes", "paths", "bitfield", "regfile", "memory", "flow",
           "gates", "contacts", "kmap", "waveform", "flowchart", "dip"}


def discover() -> dict[str, tuple[style.Figure, list[Path]]]:
    """Every figure defined by every figure module, keyed by figure name.

    A module that fails to import is reported and skipped rather than ending the run, so a
    half-written figure module for one lecture never stops the figures of another from being
    drawn. Asking for one of its figures by name still fails, with the reason printed above.
    """
    figures: dict[str, tuple[style.Figure, list[Path]]] = {}
    for path in sorted(HERE.glob("*.py")):
        if path.stem in LIBRARY:
            continue
        try:
            module = importlib.import_module(path.stem)
        except Exception as error:  # noqa: BLE001 - any failure in a figure module is its own
            print(f"warning: skipping {path.name}: {type(error).__name__}: {error}",
                  file=sys.stderr)
            continue
        for name, entry in getattr(module, "FIGURES", {}).items():
            if name in figures:
                raise SystemExit(f"figure name '{name}' is defined twice (second in {path.name})")
            figures[name] = entry
    return figures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="figures to build (default: all)")
    parser.add_argument("--list", action="store_true", help="list the figures and exit")
    parser.add_argument("--outdir", type=Path,
                        help="write <name>.png into this directory instead of the course tree")
    args = parser.parse_args()

    figures = discover()
    if args.list:
        for name, (_, paths) in figures.items():
            print(f"{name:32} -> {', '.join(str(p.relative_to(HERE.parent)) for p in paths)}")
        return

    unknown = [name for name in args.names if name not in figures]
    if unknown:
        raise SystemExit(f"unknown figure(s): {', '.join(unknown)}; try --list")

    for name in args.names or figures:
        figure, paths = figures[name]
        targets = [args.outdir / f"{name}.png"] if args.outdir else paths
        style.render(figure, targets)
        print(f"{name}: {', '.join(str(t) for t in targets)}")


if __name__ == "__main__":
    main()
