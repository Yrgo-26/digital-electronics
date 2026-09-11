#!/usr/bin/env python3
"""Assemble every assembly program in the course, and simulate the ones that say how.

    ci/simtest.py              Assemble everything; simulate every file with @expect lines.
    ci/simtest.py --build      Assemble only.
    ci/simtest.py lab_06       Only files whose path contains "lab_06".

A program is assembled with avra, which takes the same AVRASM2 syntax as Microchip Studio, so a
file that passes here opens and assembles unchanged in Studio.

A program is simulated when its source carries test directives in comments, usually at the
bottom of the file:

    ; @sim --cycles 5000 --pin D2=0
    ; @expect r16 = 0x2A
    ; @expect PORTB = 0b00001111
    ; @expect C = 1
    ; @expect between = 600

Every `@sim` line starts a new case, run from reset with the simcheck options it gives, and
the `@expect` lines after it belong to that case. `@expect` lines before any `@sim` line
belong to one default case. Names understood on the left of `=`:

* `r0` to `r31`, `SREG`, the flags `C Z N V S H T I`, `SP`, `pc`, `cycles`
* `reached` (1 if `--until` got there) and `between` (cycles between two labels)
* any I/O register name from m328Pdef.inc, such as `PORTB`, `DDRD` or `PIND`
* a data space address in brackets, such as `[0x0100]`

Values may be written in decimal, hexadecimal (0x) or binary (0b). Every line printed says what
was checked, so a file that was only assembled never reads like one that was simulated.
"""

from __future__ import annotations

import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIMCHECK = ROOT / "ci" / "simcheck" / "simcheck"
AVRA_INCLUDE = Path("/usr/share/avra")
DEVICE_FILE = AVRA_INCLUDE / "m328Pdef.inc"

# Directories never searched for sources. build/ is what `make -C book` writes, which includes a
# copy of every example program with its test block cut off; the originals are tested instead.
SKIP = {".git", ".venv", "temp", "__pycache__", "build"}


@dataclass
class Case:
    """One simulation run: its simcheck options and what the machine must look like after."""

    options: list[str] = field(default_factory=list)
    expects: list[tuple[int, str, str]] = field(default_factory=list)  # (line, name, value)


def io_registers() -> dict[str, int]:
    """Map every register name in the device file to its data space address.

    m328Pdef.inc gives I/O registers by their I/O address (PORTB = 0x05) and the registers above
    the I/O window by their data space address (TCCR1B = 0x81, marked MEMORY MAPPED). The first
    kind sits 0x20 higher in the data space, which is the address simcheck prints.
    """
    names: dict[str, int] = {}
    pattern = re.compile(r"^\s*\.equ\s+(\w+)\s*=\s*(0x[0-9a-fA-F]+)\s*(;.*)?$")
    for line in DEVICE_FILE.read_text(errors="replace").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        value = int(match.group(2), 16)
        comment = match.group(3) or ""
        if "MEMORY MAPPED" in comment:
            names[match.group(1).upper()] = value
        elif value < 0x40:
            names[match.group(1).upper()] = value + 0x20
    return names


def number(text: str) -> int:
    """Parse a decimal, 0x hexadecimal or 0b binary value, allowing _ as a digit separator."""
    return int(text.replace("_", ""), 0)


def parse(source: Path) -> list[Case]:
    """Read the test directives out of a source file."""
    cases: list[Case] = []
    current: Case | None = None
    for index, line in enumerate(source.read_text(errors="replace").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("; @sim"):
            current = Case(options=shlex.split(stripped[len("; @sim"):]))
            cases.append(current)
        elif stripped.startswith("; @expect"):
            body = stripped[len("; @expect"):]
            if "=" not in body:
                raise SystemExit(f"{source}:{index}: @expect needs 'name = value'")
            name, value = (part.strip() for part in body.split("=", 1))
            # Only the first word is the value; anything after it is a comment for the reader.
            value = value.split()[0] if value else value
            if current is None:
                current = Case()
                cases.append(current)
            current.expects.append((index, name, value))
    return cases


def assemble(source: Path, workdir: Path) -> tuple[bool, str, Path]:
    """Assemble one file with avra into `workdir`. Returns (ok, output, hex path)."""
    stem = source.stem
    hex_path = workdir / f"{stem}.hex"
    # Every output file is named explicitly, into the scratch directory. avra otherwise writes
    # its object file and EEPROM image beside the source, which litters the lecture tree.
    command = ["avra", "-I", str(AVRA_INCLUDE), "-I", str(source.parent),
               "-l", str(workdir / f"{stem}.lst"), "-m", str(workdir / f"{stem}.map"),
               "-e", str(workdir / f"{stem}.eep.hex"), "-d", str(workdir / f"{stem}.obj"),
               "-o", str(hex_path), str(source)]
    result = subprocess.run(command, cwd=workdir, capture_output=True, text=True)
    output = result.stdout + result.stderr
    # The device file's PRAGMA lines are avra's, not ours, and are noise in every build.
    lines = [line for line in output.splitlines() if "PRAGMA" not in line]
    ok = result.returncode == 0 and "Assembly complete with no errors" in output
    return ok, "\n".join(lines), hex_path


def simulate(hex_path: Path, case: Case) -> dict[str, str]:
    """Run simcheck on an assembled program and return what it printed, as a dict."""
    result = subprocess.run([str(SIMCHECK), str(hex_path), *case.options],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "simcheck failed")
    state: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if "=" in line and not line.startswith("watch "):
            key, value = line.split("=", 1)
            state[key] = value
    return state


def lookup(state: dict[str, str], name: str, registers: dict[str, int]) -> int | None:
    """The value the machine holds for one @expect name, or None if the name is unknown."""
    key = name.strip()
    bracket = re.fullmatch(r"\[(\w+)\]", key)
    if bracket:
        address = number(bracket.group(1))
        return number(state.get(f"d[0x{address:02X}]", state.get(f"d[0x{address:04X}]", "0")))
    if key in state:
        return number(state[key])
    if key.upper() in registers:
        address = registers[key.upper()]
        return number(state.get(f"d[0x{address:02X}]", "0"))
    return None


def main() -> int:
    build_only = "--build" in sys.argv[1:]
    filters = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    sources = sorted(
        path for path in ROOT.rglob("*.asm")
        if not SKIP.intersection(path.relative_to(ROOT).parts)
        and all(f in str(path.relative_to(ROOT)) for f in filters))
    if not sources:
        print("error: no assembly sources found" + (f" matching {filters}" if filters else ""),
              file=sys.stderr)
        return 1

    if not build_only and not SIMCHECK.exists():
        print(f"error: {SIMCHECK.relative_to(ROOT)} is not built; run `make -C ci/simcheck`",
              file=sys.stderr)
        return 1

    registers = io_registers()
    assembled = simulated = failed = 0

    for source in sources:
        relative = source.relative_to(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            ok, output, hex_path = assemble(source, Path(scratch))
            if not ok:
                print(f"FAIL {relative}: did not assemble")
                print("\n".join("     " + line for line in output.splitlines()[-15:]))
                failed += 1
                continue
            assembled += 1

            cases = [] if build_only else parse(source)
            if not cases:
                print(f"==> {relative} (assembled)")
                continue

            problems: list[str] = []
            for number_, case in enumerate(cases, start=1):
                try:
                    state = simulate(hex_path, case)
                except RuntimeError as error:
                    problems.append(f"case {number_}: {error}")
                    continue
                for line, name, value in case.expects:
                    actual = lookup(state, name, registers)
                    if actual is None:
                        problems.append(f"line {line}: unknown name '{name}'")
                    elif actual != number(value):
                        problems.append(f"line {line}: {name} = {actual} (0x{actual:02X}), "
                                        f"expected {value}")

            checks = sum(len(case.expects) for case in cases)
            if problems:
                print(f"FAIL {relative}")
                for problem in problems:
                    print(f"     {problem}")
                failed += 1
            else:
                print(f"==> {relative} (assembled, {len(cases)} case(s), {checks} check(s) "
                      "passed)")
                simulated += 1

    print()
    print(f"Assembled {assembled} of {len(sources)} program(s); simulated and checked "
          f"{simulated}.")
    if failed:
        print(f"error: {failed} program(s) failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
