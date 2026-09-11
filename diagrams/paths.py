"""Where figures are written: one images/ directory per lecture appendix, lab and info page."""

from __future__ import annotations

from pathlib import Path

# Repository root.
ROOT = Path(__file__).resolve().parent.parent


def lecture(number: str) -> Path:
    """The image directory of one lecture's appendices, e.g. `lecture("L04")`."""
    return ROOT / "lectures" / number / "appendix" / "images"


def lab(number: str) -> Path:
    """The image directory of one lab guide, e.g. `lab("lab1")`."""
    return ROOT / "labs" / number / "images"


def info() -> Path:
    """The image directory of the course information pages."""
    return ROOT / "info" / "images"


def exam() -> Path:
    """The image directory of the exam papers."""
    return ROOT / "exam" / "images"
