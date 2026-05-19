"""Replace em/en dashes in public HTML with commas, colons, or hyphens."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOBS = ["*.html", "pages/*.html"]

# (old, new) — order matters; specific before generic
REPLACEMENTS = [
    ("Author — Parker", "Author: Parker"),
    ("— Parker Branham, Owner", "Parker Branham, Owner"),
    ("Driveway — drag", "Driveway: drag"),
    ("Before & After — Siding", "Before & After: Siding"),
    ("Before &amp; After — Siding", "Before &amp; After: Siding"),
    ("Gallery — SC", "Gallery | SC"),
    ("FAQs — Columbia", "FAQs: Columbia"),
    ("Forest Acres — concrete", "Forest Acres: concrete"),
    ("Lexington — driveway", "Lexington: driveway"),
    ("Lake Murray) — back", "Lake Murray): back"),
    ("Math you can check — same", "Math you can check: same"),
    ("owner oversight — ", "owner oversight. "),
    ("on every job — ", "on every job. "),
    ("inconsistent — Parker", "inconsistent. Parker"),
    ("on-site standards — fast", "on-site standards: fast"),
    ("Text a photo — we", "Text a photo. We"),
    ("to maintain — especially", "to maintain, especially"),
    ("flatwork — two-car", "flatwork: two-car"),
    ("the surface — that", "the surface. That"),
    ("for the surface —\n", "for the surface.\n"),
    ("for the surface — ", "for the surface. "),
    ("aged stucco — those", "aged stucco. Those"),
    ("preferred date — we", "preferred date. We"),
    ("sq ft</strong> — often", "sq ft</strong>: often"),
    ("custom quote</strong> — custom", "custom quote</strong>: custom"),
    ("communication — you", "communication: you"),
    ("siding — you", "siding: you"),
    ("Yes — with", "Yes. With"),
    ("$120 — mobilization", "$120. Mobilization"),
    ("Parker approves every quote — student", "Parker approves every quote: student"),
    ("and more — safe", "and more: safe"),
    ("footage</strong> — so", "footage</strong>, so"),
    ("photos — size", "photos: size"),
    ("approach — we", "approach: we"),
]

def fix_en_dash_ranges(text: str) -> str:
    """$125–$275 and 500–700 → hyphens."""
    import re
    text = re.sub(r"(\$[\d,]+)–(\$?[\d,]+)", r"\1-\2", text)
    text = re.sub(r"(\d+)–(\d+)", r"\1-\2", text)
    text = re.sub(r" – ", " - ", text)
    text = re.sub(r"–", "-", text)
    return text


def fix_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    text = raw
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = fix_en_dash_ranges(text)
    if text != raw:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for pattern in GLOBS:
        for path in ROOT.glob(pattern):
            if "business-tools" in str(path):
                continue
            if fix_file(path):
                changed.append(path.name)
    print("Updated:", ", ".join(changed) if changed else "(none)")


if __name__ == "__main__":
    main()
