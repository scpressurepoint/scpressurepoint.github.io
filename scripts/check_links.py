#!/usr/bin/env python3
"""Verify internal href/src targets resolve to real files across public HTML pages."""

import re
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"business-tools", "docs", ".git", "node_modules"}
ATTR_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'id="([^"]+)"')

pages = [p for p in ROOT.rglob("*.html") if not any(d in p.parts for d in SKIP_DIRS)]
ids_cache = {}

def ids_of(path: Path):
    if path not in ids_cache:
        try:
            ids_cache[path] = set(ID_RE.findall(path.read_text(encoding="utf-8")))
        except Exception:
            ids_cache[path] = set()
    return ids_cache[path]

errors = []
for page in pages:
    text = page.read_text(encoding="utf-8")
    for url in ATTR_RE.findall(text):
        if url.startswith(("http://", "https://", "mailto:", "tel:", "sms:", "data:", "javascript:")):
            continue
        parsed = urlparse(url)
        path_part, frag = unquote(parsed.path), parsed.fragment
        if not path_part:
            # pure fragment (#foo) - check id exists on same page, "#" placeholders are JS-filled
            if frag and frag not in ids_of(page):
                errors.append(f"{page.relative_to(ROOT)}: broken anchor #{frag}")
            continue
        if path_part.startswith("/"):
            target = ROOT / path_part.lstrip("/")
            if path_part == "/":
                target = ROOT / "index.html"
        else:
            target = (page.parent / path_part).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: missing target {url}")
        elif frag and target.suffix == ".html" and frag not in ids_of(target):
            errors.append(f"{page.relative_to(ROOT)}: {url} -> no id '{frag}' in target")

if errors:
    print(f"{len(errors)} problems:")
    for e in errors:
        print(" ", e)
else:
    print(f"All internal links OK across {len(pages)} pages")
