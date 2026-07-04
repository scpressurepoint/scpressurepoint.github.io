#!/usr/bin/env python3
"""Update nav links and estimate anchors across public HTML pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Public-facing HTML (exclude business-tools, docs)
SKIP = {"business-tools", "docs"}

NEW_NAV_ROOT = """    <ul class="nav-links">
      <li><a href="pages/gallery.html">Gallery</a></li>
      <li><a href="pages/services.html">Services</a></li>
      <li><a href="pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="pages/about.html">About</a></li>
      <li><a href="pages/reviews.html">Reviews</a></li>
      <li><a href="pages/contact.html">Contact</a></li>
    </ul>"""

NEW_DRAWER_ROOT = """    <ul>
      <li><a href="pages/gallery.html">Gallery</a></li>
      <li><a href="pages/services.html">Services</a></li>
      <li><a href="pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="pages/about.html">About</a></li>
      <li><a href="pages/reviews.html">Reviews</a></li>
      <li><a href="pages/faq.html">FAQ</a></li>
      <li><a href="pages/contact.html">Contact</a></li>
      <li><a href="pages/estimate.html#form">Get a Free Estimate</a></li>
    </ul>"""

NEW_NAV_PAGES = """    <ul class="nav-links">
      <li><a href="gallery.html">Gallery</a></li>
      <li><a href="services.html">Services</a></li>
      <li><a href="../pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="reviews.html">Reviews</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>"""

NEW_DRAWER_PAGES = """    <ul>
      <li><a href="gallery.html">Gallery</a></li>
      <li><a href="services.html">Services</a></li>
      <li><a href="../pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="reviews.html">Reviews</a></li>
      <li><a href="faq.html">FAQ</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="estimate.html#form">Get a Free Estimate</a></li>
    </ul>"""

NAV_LINKS_PATTERN = re.compile(
    r"<ul class=\"nav-links\">.*?</ul>",
    re.DOTALL,
)

DRAWER_PATTERN = re.compile(
    r"<div class=\"nav-drawer\" id=\"nav-drawer\">\s*<ul>.*?</ul>",
    re.DOTALL,
)


def should_process(path: Path) -> bool:
    parts = path.parts
    return path.suffix == ".html" and not any(p in SKIP for p in parts)


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    rel = path.relative_to(ROOT)
    if rel.parts[0] == "pages":
        text = NAV_LINKS_PATTERN.sub(NEW_NAV_PAGES, text, count=1)
        text = DRAWER_PATTERN.sub(
            '<div class="nav-drawer" id="nav-drawer">\n' + NEW_DRAWER_PAGES,
            text,
            count=1,
        )
        text = text.replace('href="estimate.html"', 'href="estimate.html#form"')
    elif rel.parts[0] == "services":
        pass  # generated with correct nav
    else:
        text = NAV_LINKS_PATTERN.sub(NEW_NAV_ROOT, text, count=1)
        text = DRAWER_PATTERN.sub(
            '<div class="nav-drawer" id="nav-drawer">\n' + NEW_DRAWER_ROOT,
            text,
            count=1,
        )
        text = text.replace('href="pages/estimate.html"', 'href="pages/estimate.html#form"')

    # Footer quick links on index-like pages
    footer_replacements = [
        ('href="#gallery"', 'href="pages/gallery.html"'),
        ('href="#services"', 'href="pages/services.html"'),
        ('href="#about"', 'href="pages/about.html"'),
        ('href="#reviews"', 'href="pages/reviews.html"'),
        ('href="/#gallery"', 'href="pages/gallery.html"'),
        ('href="/#services"', 'href="pages/services.html"'),
        ('href="/#about"', 'href="pages/about.html"'),
        ('href="/#reviews"', 'href="pages/reviews.html"'),
        ('href="/#faq"', 'href="pages/faq.html"'),
        ('href="/#contact"', 'href="pages/contact.html"'),
    ]
    for old, new in footer_replacements:
        if rel.parts[0] not in ("pages", "services"):
            text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    updated = []
    for path in ROOT.rglob("*.html"):
        if should_process(path):
            if update_file(path):
                updated.append(path.relative_to(ROOT))
    for p in sorted(updated):
        print(f"Updated {p}")
    print(f"Done — {len(updated)} files updated")


if __name__ == "__main__":
    main()
