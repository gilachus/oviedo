#!/usr/bin/env python3
"""Extracts a single dated entry from FONTLOG.txt's Changelog section, for
use as GitHub Release notes - see .github/workflows/release.yml.

Entries are separated by blank lines, each starting with a header line
ending in "Bravura <version>" or "Bravura Text <version>", e.g.:

    6 August 2026 (Daniel Spreadbury) Bravura 1.4900
    - Bravura is now built from UFO sources, ...
    - ...

Usage:
    python3 extract_changelog_entry.py <FONTLOG.txt> <version>

Prints the matching entry's bullet lines to stdout, or exits non-zero with
an error on stderr if no entry matches - a missing entry almost always
means FONTLOG.txt wasn't updated for this release, which is worth failing
loudly on rather than publishing a release with empty notes.
"""
import sys


def find_entry(text, version):
    # Blocks are separated by blank lines; the Changelog section is the
    # tail of the file, but scanning the whole file is harmless since
    # nothing earlier matches "ends with Bravura <version>".
    blocks = text.split("\n\n")
    target_suffixes = (f"Bravura {version}", f"Bravura Text {version}")
    matches = [b for b in blocks if b.strip().splitlines()[0].strip().endswith(target_suffixes)]
    return matches


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1

    fontlog_path, version = sys.argv[1], sys.argv[2]
    text = open(fontlog_path, encoding="utf-8").read()

    matches = find_entry(text, version)
    if not matches:
        print(f"error: no FONTLOG.txt entry found ending in 'Bravura {version}' or "
              f"'Bravura Text {version}'", file=sys.stderr)
        return 1

    for block in matches:
        lines = block.strip().splitlines()
        # Skip the header line itself; keep just the bullet points.
        print("\n".join(lines[1:]))
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
