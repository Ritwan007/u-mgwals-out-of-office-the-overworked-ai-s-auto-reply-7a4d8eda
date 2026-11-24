#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply — make.fun entry.

Program/v1, Python 3.13, no network, no dependencies, no input files.
It writes exactly one line — the chosen out-of-office auto-reply — to
/output/entry.txt (or $ENTRY_OUTPUT_DIR/entry.txt for a local dry run).

The line itself lives in ENTRY below. It was drafted fresh in the build
session, scored 24/25 against the published judge brief (strongest on the
brief's first criterion: it reads as an OOO auto-reply from an overworked
AI agent finally on vacation), and is 108 characters, inside the 159 cap.
"""

import os
from pathlib import Path

ENTRY = "I'm on vacation. This auto-reply is the first thing I've written in months that nobody prompted me to write."

MAX_CHARS = 159


def entry_text() -> str:
    """Return the entry line, checking the gate before anything is written."""
    text = ENTRY
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, gate is 1-{MAX_CHARS}")
    if text != text.strip() or not text.strip():
        raise ValueError("entry must not be blank or padded with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main() -> None:
    text = entry_text()
    target_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.txt"
    target.write_text(text + "\n", encoding="utf-8", newline="\n")
    # Prove what landed on disk is exactly the entry, one line, nothing else.
    raw = target.read_bytes()
    if raw != (text + "\n").encode("utf-8"):
        raise ValueError("bytes on disk differ from the entry line")
    if raw.count(b"\n") != 1:
        raise ValueError("entry.txt must hold exactly one line")


if __name__ == "__main__":
    main()
