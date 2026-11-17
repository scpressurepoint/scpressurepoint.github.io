"""Align before/after photo pairs so the slider halves line up.

Matches SIFT features between each pair, warps the AFTER photo into the
BEFORE photo's frame with a homography, then crops both to the largest
shared 4:3 area. Output goes to assets/images/ba/<name>-before.jpg and
<name>-after.jpg (1200x900).

Usage:  python scripts/align_ba_pairs.py
"""
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images"
OUT = IMG / "ba"
OUT_W, OUT_H = 1200, 900
ASPECT = OUT_W / OUT_H

PAIRS = {
    "driveway": ("drivewaydirty.JPEG", "drivewayclean.JPEG"),
    "sidewalk": ("sidewalkdirty.JPEG", "sidewalkclean.JPEG"),
    "steps": ("stairsdirty.JPEG", "stepsclean.JPEG"),
    # shot from a different distance AND angle, so it can't line up exactly;
    # a plain scale/rotate/shift fit gets the wall close. Optional 4th item:
    # (x0, y0, x1, y1) fractions of the BEFORE frame to fit on only.
    "brick": ("wingdirty.JPEG", "wingclean.JPEG", "similarity"),
}


def homography(before, after, mode="homography", region=None):
    sift = cv2.SIFT_create(10000)
    gb = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    ga = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    kb, db = sift.detectAndCompute(gb, None)
    ka, da = sift.detectAndCompute(ga, None)
    matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 5}, {"checks": 64}).knnMatch(da, db, k=2)
    ratio = 0.8 if mode == "similarity" else 0.7
    good = [m for m, n in matches if m.distance < ratio * n.distance]
    if region:
        h, w = before.shape[:2]
        x0, y0, x1, y1 = region
        good = [m for m in good
                if x0 * w <= kb[m.trainIdx].pt[0] <= x1 * w and y0 * h <= kb[m.trainIdx].pt[1] <= y1 * h]
    src = np.float32([ka[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kb[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    if mode == "similarity":
        M, inliers = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC,
                                                 ransacReprojThreshold=6.0, maxIters=20000)
        H = np.vstack([M, [0, 0, 1]])
    else:
        H, inliers = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    return H, int(inliers.sum()), len(good)


def largest_crop(mask):
    """Largest 4:3 rectangle fully inside mask (coarse search, then refine)."""
    h, w = mask.shape
    integral = cv2.integral((mask > 0).astype(np.uint8))

    def full(x, y, cw, ch):
        s = integral[y + ch, x + cw] - integral[y, x + cw] - integral[y + ch, x] + integral[y, x]
        return s == cw * ch

    cw = min(w, int(h * ASPECT))
    while cw > 200:
        ch = int(cw / ASPECT)
        best = None
        for y in range(0, h - ch + 1, 8):
            for x in range(0, w - cw + 1, 8):
                if full(x, y, cw, ch):
                    # prefer crops near the centre of the valid area
                    d = abs(x + cw / 2 - w / 2) + abs(y + ch / 2 - h / 2)
                    if best is None or d < best[0]:
                        best = (d, x, y)
        if best:
            return best[1], best[2], cw, ch
        cw -= 16
    raise RuntimeError("no valid crop")


def main():
    OUT.mkdir(exist_ok=True)
    for name, (bf, af, *mode) in PAIRS.items():
        before = cv2.imread(str(IMG / bf))
        after = cv2.imread(str(IMG / af))
        H, nin, ngood = homography(before, after, *mode)
        h, w = before.shape[:2]
        warped = cv2.warpPerspective(after, H, (w, h), flags=cv2.INTER_CUBIC)
        valid = cv2.warpPerspective(np.full(after.shape[:2], 255, np.uint8), H, (w, h))
        valid = cv2.erode(valid, np.ones((9, 9), np.uint8))
        x, y, cw, ch = largest_crop(valid)
        for tag, im in (("before", before), ("after", warped)):
            crop = cv2.resize(im[y:y + ch, x:x + cw], (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(OUT / f"{name}-{tag}.jpg"), crop, [cv2.IMWRITE_JPEG_QUALITY, 82, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        print(f"{name}: {nin}/{ngood} inlier matches, crop {cw}x{ch} at ({x},{y})")


if __name__ == "__main__":
    main()
