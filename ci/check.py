#!/usr/bin/env python3
"""Check the course's own conventions, the ones no other tool knows about.

    ci/check.py

Every rule below is one that a reader relies on without being told, so breaking it produces a
course that is harder to use rather than an error anywhere. Each failure is printed as
file:line and a sentence, and the script exits 1 if there was any.

| Rule            | What it wants                                                            |
|-----------------|--------------------------------------------------------------------------|
| Layout          | Every lectures/LNN/ holds README.md and appendix/.                       |
| Title           | A lecture README starts `# LNN - Titel`, with a hyphen, not a dash.      |
| Sections        | The eight `##` sections of a lecture README, in order. The last lecture  |
|                 | closes with `## Efter kursen` in place of `## Nästa föreläsning`.         |
| Closing rule    | A lecture README's last line is `---`.                                   |
| Appendix letters| Theory appendices first; the second-to-last is the exercises and the     |
|                 | last the solutions. Until the solutions are published (force-added), the |
|                 | exercises are last, and that shape is accepted too.                      |
| Appendix titles | An appendix starts `# Appendix X - Titel`, X matching its file letter.   |
| Section rules   | Every `##` is preceded by `---`, except one directly under the title.     |
| Figures         | Every published PNG is embedded by published Markdown, and every image   |
|                 | has at least 25 characters of alt text. Git-ignored files (solutions,    |
|                 | the teacher's exam, sol_*.png) count as unpublished.                     |
| Line width      | Prose lines in Markdown are at most 100 characters, not counting link    |
|                 | targets. Tables, code blocks, headings and URL lines are exempt.         |
| Whitespace      | No trailing whitespace in Markdown, assembly or Python; no tabs in       |
|                 | assembly.                                                                |
"""

from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# build/ is what `make -C book` writes: copies of the programs and the rendered figures, never
# committed, and not course material a reader opens.
SKIP = {".git", ".venv", "temp", "__pycache__", "build"}

SECTIONS = [
    "Agenda",
    "Föreläsningsupplägg",
    "Före föreläsningen",
    "Efter föreläsningen",
    "Det här ska du kunna efteråt",
    "Frågor att testa dig själv med",
    "Referens",
    "Nästa föreläsning",
]
LAST_SECTION = "Efter kursen"
MAX_WIDTH = 100
MIN_ALT = 25

problems: list[str] = []


def ignore_patterns() -> list[str]:
    """The plain ignore patterns in .gitignore: no negations, and not the catch-all `*`."""
    patterns = []
    for line in (ROOT / ".gitignore").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "!")) and line != "*":
            patterns.append(line)
    return patterns


IGNORED = ignore_patterns()


def unpublished(path: Path) -> bool:
    """Whether git ignores this file: a solution, a teacher-only paper, or a figure of either.

    Such a file is on disk here but absent from a fresh clone until it is force-added, so a
    check that relies on it passes locally and fails in CI. The figure check below therefore
    treats it as if it were not there.
    """
    relative = path.relative_to(ROOT).as_posix()
    for pattern in IGNORED:
        if pattern.endswith("/"):
            if relative.startswith(pattern) or f"/{pattern}" in f"/{relative}":
                return True
        elif "/" in pattern:
            if fnmatch.fnmatch(relative, pattern):
                return True
        elif fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def report(path: Path, line: int | None, message: str) -> None:
    location = str(path.relative_to(ROOT)) + (f":{line}" if line else "")
    problems.append(f"{location}: {message}")


def files(pattern: str) -> list[Path]:
    return sorted(p for p in ROOT.rglob(pattern)
                  if not SKIP.intersection(p.relative_to(ROOT).parts))


def prose_lines(text: str):
    """(line number, line, inside a code block) for every line of a Markdown file."""
    fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fence = not fence
            yield number, line, True
            continue
        yield number, line, fence


def check_lecture(directory: Path, last: bool) -> None:
    readme = directory / "README.md"
    appendix = directory / "appendix"
    if not readme.is_file():
        report(directory, None, "missing README.md")
        return
    if not appendix.is_dir():
        report(directory, None, "missing appendix/")

    lines = readme.read_text().splitlines()
    name = directory.name
    if not lines or not re.fullmatch(rf"# {name} - \S.*", lines[0]):
        report(readme, 1, f"first line must be '# {name} - Titel' (with a hyphen)")
    if not lines or lines[-1].strip() != "---":
        report(readme, len(lines), "last line must be '---'")

    headings = [(i + 1, line[3:].strip()) for i, line in enumerate(lines)
                if line.startswith("## ")]
    expected = SECTIONS[:-1] + [LAST_SECTION if last else SECTIONS[-1]]
    found = [title for _, title in headings]
    if found != expected:
        report(readme, None, f"sections must be {expected}, found {found}")

    if appendix.is_dir():
        docs = sorted(p for p in appendix.glob("*.md"))
        letters = [p.name[0] for p in docs]
        if letters != [chr(ord("a") + i) for i in range(len(letters))]:
            report(appendix, None, f"appendix letters must run a, b, c ... without gaps: "
                   f"{[p.name for p in docs]}")
        kinds = [p.stem.split("_", 1)[1] if "_" in p.stem else "" for p in docs]
        if kinds and kinds[-1] == "solutions":
            if len(kinds) < 2 or kinds[-2] != "exercises":
                report(appendix, None, "the appendix before the solutions must be the exercises")
        elif kinds and kinds[-1] != "exercises":
            report(appendix, None, "the last appendix must be the exercises or the solutions")
        for doc in docs:
            first = doc.read_text().splitlines()[:1]
            letter = doc.name[0].upper()
            if not first or not re.fullmatch(rf"# Appendix {letter} - \S.*", first[0]):
                report(doc, 1, f"first line must be '# Appendix {letter} - Titel'")


def check_markdown(path: Path) -> None:
    text = path.read_text()
    previous = ""  # The previous non-blank line outside a code block.
    for number, line, in_code in prose_lines(text):
        if line != line.rstrip():
            report(path, number, "trailing whitespace")
        if in_code:
            continue
        # A section starts after a horizontal rule, unless it sits directly under the title.
        if line.startswith("## ") and previous.strip() != "---" and not previous.startswith("# "):
            report(path, number, "a '##' section must be preceded by a '---' line")
        exempt = (line.lstrip().startswith("|") or line.startswith("#") or "http" in line
                  or line.lstrip().startswith("!["))
        # A relative link target cannot be broken across lines, so it does not count towards the
        # width: a line is too long only if it would still be too long without its targets.
        width = len(re.sub(r"\]\([^)]*\)", "]()", line))
        if width > MAX_WIDTH and not exempt:
            report(path, number, f"line is {width} characters without link targets, the "
                   f"limit is {MAX_WIDTH}")
        for alt in re.findall(r"!\[([^\]]*)\]\(", line):
            if len(alt) < MIN_ALT:
                report(path, number, f"image alt text is {len(alt)} characters, needs "
                       f"at least {MIN_ALT}: '{alt}'")
        if line.strip():
            previous = line


def check_figures() -> None:
    # Only published Markdown counts as a reader, and only published figures need one: see
    # `unpublished` for why a solutions appendix cannot be the only thing embedding a figure.
    embedded: set[Path] = set()
    for md in files("*.md"):
        if unpublished(md):
            continue
        for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md.read_text()):
            embedded.add((md.parent / target.split("#")[0]).resolve())
    for png in files("*.png"):
        if not unpublished(png) and png.resolve() not in embedded:
            report(png, None, "PNG is not embedded by any published Markdown file "
                   "(a figure used only in solutions must be named sol_*.png)")


def check_code() -> None:
    for pattern in ("*.asm", "*.py"):
        for path in files(pattern):
            for number, line in enumerate(path.read_text().splitlines(), start=1):
                if line != line.rstrip():
                    report(path, number, "trailing whitespace")
                if pattern == "*.asm" and "\t" in line:
                    report(path, number, "tab character; indent assembly with spaces")


def main() -> int:
    lectures = sorted(p for p in (ROOT / "lectures").glob("L[0-9][0-9]") if p.is_dir())
    for index, directory in enumerate(lectures):
        check_lecture(directory, last=index == len(lectures) - 1)
    for md in files("*.md"):
        check_markdown(md)
    check_figures()
    check_code()

    if problems:
        for problem in problems:
            print(problem)
        print(f"\nerror: {len(problems)} convention problem(s).", file=sys.stderr)
        return 1
    print(f"Convention check: {len(lectures)} lecture(s), {len(files('*.md'))} Markdown "
          f"file(s), {len(files('*.png'))} figure(s); no problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
