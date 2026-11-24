#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

Writes one satirical sentence (1-320 chars, UTF-8, not only whitespace)
to $MAKEFUN_OUTPUT_DIR/entry.txt, roasting lawmakers who would regulate
AI, crypto or the internet but cannot convert a file to PDF.
"""

import os
import sys

MAX_CHARS = 320

ROAST = (
    "The senator drafting the AI Safety Act printed his own bill, "
    "scanned it back in, and emailed the scan to his staff asking them "
    "to turn it back into a PDF \u2014 then cast the deciding vote to "
    "regulate the machines that wrote it."
)


def resolve_output_dir():
    """Return the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Check the entry text against the competition gate.

    Returns a list of problems (empty means valid).
    """
    problems = []
    if not isinstance(text, str):
        problems.append("text is not a string")
        return problems
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("text is not valid UTF-8: %s" % exc)
    if not text.strip():
        problems.append("text is only whitespace")
    if len(text) < 1:
        problems.append("text is empty (needs 1-320 characters)")
    if len(text) > MAX_CHARS:
        problems.append(
            "text is %d characters, over the 320-character limit"
            % len(text)
        )
    if text.count(".") + text.count("!") + text.count("?") < 1:
        problems.append("text has no sentence-ending punctuation")
    return problems


def main():
    problems = validate(ROAST)
    if problems:
        for problem in problems:
            print("ERROR: %s" % problem, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ROAST + "\n")
    print("wrote %s (%d characters)" % (path, len(ROAST)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
