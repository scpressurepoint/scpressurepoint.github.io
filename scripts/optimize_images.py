#!/usr/bin/env python3
"""Resize and compress all site images in assets/images/."""

from __future__ import annotations

import io
import os
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1] / "assets" / "images"

# (max_width, max_height, jpeg_quality, force_jpeg)
RULES: dict[str, tuple[int, int, int, bool]] = {
    "photos/": (1920, 1280, 82, True),
    "ActionShot.JPG": (1920, 1280, 82, True),
    "Trailer.JPG": (1920, 1280, 82, True),
    "parker.jpg": (800, 1000, 85, True),
    "comingsoon.jpg": (800, 800, 82, True),
    "BeforeandAfterSiding.jpg": (1400, 900, 85, True),
    "Before1.jpg": (1000, 1500, 85, True),
    "After1.jpg": (1000, 1500, 85, True),
    "Logo.png": (512, 512, 90, False),
    "LogoWBG.png": (512, 512, 90, False),
    "og-image.jpg": (1200, 630, 85, True),
    "rightleft.png": (351, 135, 90, False),
    "default_jpeg": (1200, 1600, 80, True),
}


def rule_for(rel: str) -> tuple[int, int, int, bool]:
    if rel.startswith("photos" + os.sep) or rel.startswith("photos/"):
        return RULES["photos/"]
    name = Path(rel).name
    if name in RULES:
        return RULES[name]
    if name.lower().endswith((".jpg", ".jpeg")):
        return RULES["default_jpeg"]
    if name.lower().endswith(".png"):
        return (1400, 1600, 85, False)
    return RULES["default_jpeg"]


def fit_within(size: tuple[int, int], max_w: int, max_h: int) -> tuple[int, int]:
    w, h = size
    scale = min(max_w / w, max_h / h, 1.0)
    if scale >= 1.0:
        return w, h
    return max(1, int(w * scale)), max(1, int(h * scale))


def enhance_rgb(img: Image.Image) -> Image.Image:
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.12)
    return img


def save_jpeg(img: Image.Image, path: Path, quality: int) -> None:
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(
        path,
        "JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling=2,
    )


def save_png(img: Image.Image, path: Path) -> None:
    img.save(path, "PNG", optimize=True)


def optimize_file(path: Path) -> dict:
    rel = path.relative_to(ROOT).as_posix()
    max_w, max_h, quality, force_jpeg = rule_for(rel.replace("\\", "/"))
    before = path.stat().st_size

    with Image.open(path) as src:
        src = ImageOps.exif_transpose(src)
        new_size = fit_within(src.size, max_w, max_h)
        if new_size != src.size:
            src = src.resize(new_size, Image.Resampling.LANCZOS)

        ext = path.suffix.lower()
        is_photo = ext in {".jpg", ".jpeg"} or force_jpeg

        if is_photo and src.mode in {"RGB", "L"}:
            out = enhance_rgb(src.convert("RGB"))
        elif is_photo:
            out = enhance_rgb(src.convert("RGB"))
        else:
            out = src

        if force_jpeg and ext == ".png":
            new_path = path.with_suffix(".jpg")
            save_jpeg(out.convert("RGB"), new_path, quality)
            if new_path != path:
                path.unlink(missing_ok=True)
                path = new_path
        elif is_photo:
            save_jpeg(out, path, quality)
        else:
            save_png(out, path)

    after = path.stat().st_size
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "before_kb": round(before / 1024, 1),
        "after_kb": round(after / 1024, 1),
        "saved_pct": round((1 - after / before) * 100, 1) if before else 0,
    }


def make_apple_touch_icon() -> None:
    logo = ROOT / "Logo.png"
    out = ROOT / "apple-touch-icon.png"
    with Image.open(logo) as img:
        img = img.convert("RGBA")
        img.thumbnail((180, 180), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (180, 180), (255, 255, 255, 255))
        x = (180 - img.width) // 2
        y = (180 - img.height) // 2
        canvas.paste(img, (x, y), img)
        canvas.save(out, "PNG", optimize=True)


def make_og_image() -> None:
    """Build a proper 1200x630 OG image from hero photo + brand overlay."""
    hero = ROOT / "photos" / "hero-driveway-surface-cleaner.jpg"
    logo = ROOT / "Logo.png"
    out = ROOT / "og-image.jpg"

    with Image.open(hero) as bg:
        bg = ImageOps.exif_transpose(bg).convert("RGB")
        # Cover crop to 1200x630
        target_w, target_h = 1200, 630
        scale = max(target_w / bg.width, target_h / bg.height)
        resized = bg.resize(
            (int(bg.width * scale), int(bg.height * scale)),
            Image.Resampling.LANCZOS,
        )
        left = (resized.width - target_w) // 2
        top = (resized.height - target_h) // 2
        canvas = resized.crop((left, top, left + target_w, top + target_h))

        # Dark gradient overlay for text legibility
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        for x in range(target_w):
            alpha = int(210 * (1 - x / target_w) ** 0.55)
            for y in range(target_h):
                overlay.putpixel((x, y), (15, 61, 114, min(255, alpha)))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

        # Logo
        if logo.exists():
            with Image.open(logo) as mark:
                mark = mark.convert("RGBA")
                mark.thumbnail((120, 120), Image.Resampling.LANCZOS)
                canvas.paste(mark, (56, 56), mark)

        save_jpeg(canvas, out, 85)


def main() -> None:
    results: list[dict] = []
    skip = {"apple-touch-icon.png"}

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if path.name in skip:
            continue
        try:
            results.append(optimize_file(path))
        except Exception as exc:
            print(f"FAIL {path.name}: {exc}")

    make_apple_touch_icon()
    make_og_image()

    total_before = sum(r["before_kb"] for r in results)
    total_after = sum(r["after_kb"] for r in results)
    print(f"Optimized {len(results)} files")
    print(f"Total: {total_before:.0f} KB -> {total_after:.0f} KB")
    for r in sorted(results, key=lambda x: x["before_kb"], reverse=True)[:15]:
        print(
            f"  {r['file']}: {r['before_kb']} KB -> {r['after_kb']} KB ({r['saved_pct']}% saved)"
        )


if __name__ == "__main__":
    main()
