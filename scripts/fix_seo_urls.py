#!/usr/bin/env python3
"""Normalize homepage links to / instead of index.html for SEO."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"business-tools", "docs", "scripts", ".git"}

REPLACEMENTS = [
    (re.compile(r'href="\.\./index\.html#'), 'href="/#'),
    (re.compile(r"href='\.\./index\.html#"), "href='/#"),
    (re.compile(r'href="\.\./index\.html"'), 'href="/"'),
    (re.compile(r"href='\.\./index\.html'"), "href='/'"),
    (re.compile(r'href="index\.html#'), 'href="/#'),
    (re.compile(r"href='index\.html#"), "href='/#"),
    (re.compile(r'href="index\.html"'), 'href="/"'),
    (re.compile(r"href='index\.html'"), "href='/'"),
    (re.compile(r"window\.location\.href = '\.\./index\.html'"), "window.location.href = '/'"),
    (re.compile(r'window\.location\.href = "\.\./index\.html"'), 'window.location.href = "/"'),
]


def should_process(path: Path) -> bool:
    if path.name not in {".html"} and path.suffix.lower() != ".html":
        return False
    return not any(part in SKIP_DIRS for part in path.parts)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if should_process(path):
            if fix_file(path):
                changed.append(path.relative_to(ROOT).as_posix())
    print(f"Updated {len(changed)} files")
    for name in changed:
        print(f"  {name}")


if __name__ == "__main__":
    main()
