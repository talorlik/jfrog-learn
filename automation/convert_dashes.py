#!/usr/bin/env python3
"""
convert_dashes.py - One-shot utility to enforce the project's hard rule:
NO em-dashes and NO en-dashes anywhere in source content. Replace them with
plain hyphens (minus). This covers literal characters and HTML entity forms.

Spacing rule:
  " - "  (already spaced)  -> keep the spaces, swap the dash char
  "a-b"  (unspaced range)  -> plain hyphen, no spaces added

Scope: all text source files in the repo, excluding .git and generated /
gitignored artifact directories (_diagrams, _docx). Run from the repo root.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# File extensions we treat as editable text source.
EXTS = {".html", ".css", ".js", ".py", ".md", ".yml", ".yaml",
        ".json", ".txt"}

# Directories never to touch. `.claude` holds Claude Code tooling and skills,
# not site content - it is never part of the page_data -> pages -> docx pipeline
# that the dash rule protects, and its skill files legitimately document the
# forbidden dash forms (like this script and AGENTS.md do). Converting them
# would corrupt the documentation, so the whole tree is exempt.
EXCLUDE_DIRS = {".git", ".claude", "_diagrams", "_docx", "__pycache__", "node_modules"}

# Don't rewrite this script itself (it intentionally documents the characters).
SELF = Path(__file__).resolve()

# Files that legitimately contain the forbidden dash forms and must NOT be
# rewritten. AGENTS.md / DECISIONS.md document the rule itself; sync_to_drive.py
# uses the U+2014 / U+2013 escapes as CODE - it matches existing Google
# Doc names that were created with those dashes so it can update them in place
# and preserve their Drive file IDs (NotebookLM source links depend on this).
# Flattening those escapes would silently break ID preservation. Matched by file
# name, repo-wide.
EXCLUDE_FILES = {"AGENTS.md", "DECISIONS.md", "sync_to_drive.py"}

EM = "\u2014"   # —
EN = "\u2013"   # –


def convert_text(s: str) -> str:
    # HTML entity forms first.
    s = s.replace("&mdash;", "-").replace("&ndash;", "-")
    s = s.replace("&#8212;", "-").replace("&#8211;", "-")
    s = s.replace("&#x2014;", "-").replace("&#x2013;", "-")
    s = s.replace("&#X2014;", "-").replace("&#X2013;", "-")
    # Python/JSON unicode-escape forms (e.g. page_data.py stores "\u2014").
    # These appear in source as the literal 6-char sequence, not the char.
    s = s.replace("\\u2014", "-").replace("\\u2013", "-")
    s = s.replace("\\U00002014", "-").replace("\\U00002013", "-")
    # Literal dash characters -> plain hyphen (preserves any surrounding spaces).
    s = s.replace(EM, "-").replace(EN, "-")
    return s


def should_skip(p: Path) -> bool:
    if p.resolve() == SELF:
        return True
    if p.name in EXCLUDE_FILES:
        return True
    parts = set(p.parts)
    if parts & EXCLUDE_DIRS:
        return True
    return p.suffix.lower() not in EXTS


def main() -> int:
    changed = []
    for p in REPO.rglob("*"):
        if not p.is_file() or should_skip(p):
            continue
        try:
            original = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        converted = convert_text(original)
        if converted != original:
            p.write_text(converted, encoding="utf-8")
            changed.append(str(p.relative_to(REPO)))

    if changed:
        print(f"Converted {len(changed)} file(s):")
        for c in sorted(changed):
            print(f"  {c}")
    else:
        print("No dashes found to convert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
