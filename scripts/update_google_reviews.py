#!/usr/bin/env python3
"""Update assets/data/google-reviews.json (no Google API required).

Usage:
  python scripts/update_google_reviews.py 5.0 12
  python scripts/update_google_reviews.py          # interactive prompts

After updating, commit and push so the public site picks up the new stats.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data" / "google-reviews.json"
DEFAULT_REVIEW_URL = "https://share.google/tQ0cC4PlI2R972dyA"
DEFAULT_NAME = "SC Pressure Point"


def load_existing() -> dict:
    if OUT.exists():
        try:
            return json.loads(OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def parse_args() -> tuple[float, int]:
    if len(sys.argv) >= 3:
        return float(sys.argv[1]), int(sys.argv[2])

    existing = load_existing()
    default_rating = existing.get("rating", 5.0)
    default_count = existing.get("reviewCount", 5)

    print("Update Google Business Profile stats for the public website.")
    print(f"Open your profile: {DEFAULT_REVIEW_URL}\n")

    rating_raw = input(f"Star rating [{default_rating}]: ").strip() or str(default_rating)
    count_raw = input(f"Review count [{default_count}]: ").strip() or str(default_count)
    return float(rating_raw), int(count_raw)


def main() -> None:
    existing = load_existing()
    rating, count = parse_args()

    if not (1 <= rating <= 5):
        print("Rating must be between 1.0 and 5.0.", file=sys.stderr)
        sys.exit(1)
    if count < 0:
        print("Review count cannot be negative.", file=sys.stderr)
        sys.exit(1)

    record = {
        "rating": round(rating, 1),
        "reviewCount": count,
        "reviewUrl": existing.get("reviewUrl") or DEFAULT_REVIEW_URL,
        "placeId": existing.get("placeId", ""),
        "placeName": existing.get("placeName") or DEFAULT_NAME,
        "updatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "manual",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("\nWrote", OUT.relative_to(ROOT))
    print(json.dumps(record, indent=2))
    print("\nNext: git add assets/data/google-reviews.json && git commit && git push")


if __name__ == "__main__":
    main()
