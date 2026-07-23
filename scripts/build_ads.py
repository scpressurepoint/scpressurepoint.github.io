#!/usr/bin/env python3
"""Build upload-ready Meta ad creatives for SC Pressure Point from real job photos.
Outputs PNGs to ../../SC_Pressure_Point_Ads/ as 1080x1080 (feed) and 1080x1350 (portrait/Reels).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")
OUT = os.path.abspath(os.path.join(ROOT, "..", "..", "SC_Pressure_Point_Ads"))
os.makedirs(OUT, exist_ok=True)

# Brand palette
BLUE      = (26, 94, 168)      # #1A5EA8 primary
BLUE_DK   = (15, 61, 114)      # #0F3D72
BLUE_LT   = (184, 217, 245)    # #B8D9F5
GOLD      = (246, 194, 0)      # #F6C200
WHITE     = (255, 255, 255)
DARK      = (31, 41, 55)       # #1f2937
GREY      = (100, 116, 139)    # #64748b

FONT_B = os.path.join("C:/Windows/Fonts", "arialbd.ttf")
FONT_R = os.path.join("C:/Windows/Fonts", "arial.ttf")

def font(sz, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, sz)

def fit(img, w, h):
    """Cover-resize img to (w,h), center crop."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def logo_chip(size=64):
    """White rounded chip with the blue logo centered, for dark bars."""
    p = os.path.join(IMG, "Logo.png")
    logo = Image.open(p).convert("RGBA")
    s = size
    logo = logo.resize((int(s * logo.width / logo.height), s), Image.LANCZOS)
    chip = Image.new("RGBA", (logo.width + 24, s + 24), (255, 255, 255, 255))
    c = ImageDraw.Draw(chip)
    rad = (logo.width + 24) // 2
    c.rounded_rectangle([(0, 0), chip.size], radius=rad, fill=(255, 255, 255, 255))
    chip.paste(logo, ((chip.width - logo.width) // 2, (chip.height - logo.height) // 2), logo)
    return chip

def brand_bar(draw, W, y0, h, phone="(803) 272-8118"):
    """Dark-blue bottom bar with logo chip + wordmark + stars + phone."""
    draw.rectangle([(0, y0), (W, y0 + h)], fill=BLUE_DK)
    chip = logo_chip(int(h * 0.62))
    draw.bitmap((18, y0 + (h - chip.height) // 2), chip, fill=None)
    tx = 18 + chip.width + 14
    f1 = font(int(h * 0.30))
    draw.text((tx, y0 + h * 0.16), "SC PRESSURE POINT", font=f1, fill=WHITE)
    f2 = font(int(h * 0.24))
    draw.text((tx, y0 + h * 0.55), "5.0 on Google  \u00b7  " + phone, font=f2, fill=GOLD)
    # right side url
    fr = font(int(h * 0.24))
    draw.text((W - 18, y0 + h * 0.40), "scpressurepoint.com", font=fr, fill=WHITE, anchor="ra")

def top_banner(draw, W, y0, h, text, bg=BLUE, fg=WHITE, sub=None):
    draw.rectangle([(0, y0), (W, y0 + h)], fill=bg)
    if sub:
        # reserve bottom ~30% of banner for sub line on a darker band
        f = font(int(h * 0.26))
        lines = wrap(draw, text, f, W - 60)
        lh = int(h * 0.32)
        yy = y0 + (int(h * 0.66) - len(lines) * lh) // 2 + 2
        for ln in lines:
            draw.text(((W - draw.textlength(ln, font=f)) // 2, yy), ln, font=f, fill=fg)
            yy += lh
        fs = font(int(h * 0.26))
        draw.rectangle([(0, y0 + int(h * 0.66)), (W, y0 + h)], fill=BLUE_DK)
        draw.text(((W - draw.textlength(sub, font=fs)) // 2, y0 + int(h * 0.70)), sub, font=fs, fill=WHITE)
    else:
        f = font(int(h * 0.34))
        lines = wrap(draw, text, f, W - 60)
        lh = int(h * 0.40)
        yy = y0 + (h - len(lines) * lh) // 2 + 4
        for ln in lines:
            draw.text(((W - draw.textlength(ln, font=f)) // 2, yy), ln, font=f, fill=fg)
            yy += lh

def label(draw, x, y, text, bg):
    f = font(34)
    tw = draw.textlength(text, font=f) + 28
    px, py, pad = 18, 18, 14
    draw.rectangle([(x + px, y + py), (x + px + tw, y + py + 56)], fill=bg)
    draw.text((x + px + pad, y + py + 10), text, font=f, fill=WHITE)

def build_before_after(name, before_p, after_p, hook, sub, sizes):
    before = Image.open(os.path.join(IMG, before_p)).convert("RGB")
    after = Image.open(os.path.join(IMG, after_p)).convert("RGB")
    for (W, H) in sizes:
        banner_h = int(H * 0.11)
        bar_h = int(H * 0.11)
        mid_top = banner_h
        mid_bot = H - bar_h
        mid_h = mid_bot - mid_top
        half = W // 2
        b = fit(before, half, mid_h)
        a = fit(after, W - half, mid_h)
        canvas = Image.new("RGB", (W, H), WHITE)
        canvas.paste(b, (0, mid_top))
        canvas.paste(a, (half, mid_top))
        d = ImageDraw.Draw(canvas)
        # divider
        d.rectangle([(half - 4, mid_top), (half + 4, mid_bot)], fill=WHITE)
        # labels
        label(d, 20, mid_top + 18, "BEFORE", GREY)
        label(d, half + 20, mid_top + 18, "AFTER", BLUE)
        top_banner(d, W, 0, banner_h, hook, sub=sub)
        brand_bar(d, W, mid_bot, bar_h)
        canvas.save(os.path.join(OUT, f"{name}_{W}x{H}.png"))
        print("saved", f"{name}_{W}x{H}.png")

def build_single(name, photo_p, hook, sub, sizes, bg=BLUE, fg=WHITE):
    photo = Image.open(os.path.join(IMG, photo_p)).convert("RGB")
    for (W, H) in sizes:
        banner_h = int(H * 0.15)
        bar_h = int(H * 0.11)
        photo_h = H - banner_h - bar_h
        ph = fit(photo, W, photo_h)
        canvas = Image.new("RGB", (W, H), WHITE)
        canvas.paste(ph, (0, banner_h))
        d = ImageDraw.Draw(canvas)
        # dark gradient-ish bottom band over photo for legibility is skipped; rely on banner/bar
        top_banner(d, W, 0, banner_h, hook, bg=bg, fg=fg, sub=sub)
        brand_bar(d, W, H - bar_h, bar_h)
        canvas.save(os.path.join(OUT, f"{name}_{W}x{H}.png"))
        print("saved", f"{name}_{W}x{H}.png")

def build_parker(sizes):
    parker = Image.open(os.path.join(IMG, "parker.png")).convert("RGBA")
    # crop to head/shoulders, drop formal lapel/boutonniere: keep top ~75%
    pw, ph = parker.size
    parker = parker.crop((0, 0, pw, int(ph * 0.92)))
    for (W, H) in sizes:
        banner_h = int(H * 0.13)
        bar_h = int(H * 0.11)
        canvas = Image.new("RGB", (W, H), BLUE_DK)
        d = ImageDraw.Draw(canvas)
        # place parker on right, cover-fit to right ~55%
        right_w = int(W * 0.55)
        pk = fit(parker, right_w, H - banner_h)
        canvas.paste(pk, (W - right_w, banner_h))
        # left text panel
        margin = 40
        f = font(int(H * 0.060))
        txt = "When you text us, you text PARKER \u2014 the owner. Not a franchise call center."
        lines = wrap(d, txt, f, W - right_w - margin * 2)
        yy = banner_h + 40
        lh = int(H * 0.075)
        for ln in lines:
            d.text((margin, yy), ln, font=f, fill=WHITE)
            yy += lh
        f2 = font(int(H * 0.030))
        d.text((margin, yy + 10), "Every Columbia job carries his name & his standard.", font=f2, fill=BLUE_LT)
        top_banner(d, W, 0, banner_h, "TEXT THE OWNER, NOT A CALL CENTER", bg=GOLD, fg=DARK)
        brand_bar(d, W, H - bar_h, bar_h)
        canvas.save(os.path.join(OUT, f"parker_owner_{W}x{H}.png"))
        print("saved", f"parker_owner_{W}x{H}.png")

SIZES = [(1080, 1080), (1080, 1350)]

# --- Before/After ads ---
build_before_after("ba_driveway", "drivewaydirty.JPEG", "drivewayclean.JPEG",
                   "GONE GREEN FROM HUMIDITY?", "Columbia, SC \u00b7 driveways from $125",
                   SIZES)
build_before_after("ba_sidewalk", "sidewalkdirty.JPEG", "sidewalkclean.JPEG",
                   "SAFE. CLEAN. SHARP.", "Sidewalks & walkways",
                   SIZES)
build_before_after("ba_brickwing", "wingdirty.JPEG", "wingclean.JPEG",
                   "BRICK & MORTAR, DONE RIGHT", "Gentle cleaning, no damage",
                   SIZES)
build_before_after("ba_steps", "stairsdirty.JPEG", "stepsclean.JPEG",
                   "FIRST IMPRESSIONS START HERE", "Steps & entryways",
                   SIZES)
# Siding is already a perfect split -> single hero-style
build_single("ba_siding_split", "BeforeandAfterSiding.jpg",
             "MOLD ON YOUR SIDING?", "We soft wash it safe \u2014 no damage",
             SIZES, bg=BLUE, fg=WHITE)

# --- Action / single ads ---
build_single("act_surfacecleaner", "photos/hero-driveway-surface-cleaner.jpg",
             "WE DON'T JUST CLEAN. WE TRANSFORM.", "100% satisfaction guaranteed",
             SIZES)
build_single("act_softwash", "photos/soft-wash-exterior.jpg",
             "COLUMBIA'S HUMIDITY MEETS ITS MATCH", "Soft wash \u00b7 safe for siding",
             SIZES)
build_single("act_walkway", "photos/walkway-pressure-washing.jpg",
             "YOUR HOME. LOOKING NEW AGAIN.", "Honest per-sq-ft pricing",
             SIZES)

# --- Owner face ad ---
# HELD: needs a real on-site/casual Parker photo (current assets are formal/prom shots
# which clash with the "on the job / text the owner" message). Re-enable after swap.
# build_parker(SIZES)

print("\nALL DONE ->", OUT)
