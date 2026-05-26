#!/usr/bin/env python3
"""Validate and lightly normalize india_jewellery_instagram_leads.txt.

The canonical lead database lives at the repository root. This script checks
that there are exactly 100 unique Instagram handles and no duplicate
normalized Indian mobile numbers (last 10 digits), then rewrites the file
with a refreshed export header date when run with --write.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = ROOT / "india_jewellery_instagram_leads.txt"


def norm_phone(raw: str) -> str | None:
    if not raw or raw.strip().lower() in {"unknown", "n/a", "none", ""}:
        return None
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) < 10:
        return None
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) >= 12 and digits.startswith("91"):
        digits = digits[-10:]
    if len(digits) > 10:
        digits = digits[-10:]
    if not digits.startswith(("6", "7", "8", "9")):
        return None
    return digits


def parse_handles_and_phones(text: str) -> tuple[list[str], dict[str, list[int]]]:
    handles: list[str] = []
    phone_to_leads: dict[str, list[int]] = {}
    blocks = re.split(r"={50}\s*\nLEAD #(\d+)\s*\n={50}", text)
    # blocks: [preamble, num1, body1, num2, body2, ...]
    for i in range(1, len(blocks), 2):
        lead_no = int(blocks[i])
        body = blocks[i + 1]
        hm = re.search(
            r"^Instagram Handle:\s*\n@([A-Za-z0-9._]+)\s*$",
            body,
            re.MULTILINE,
        )
        if not hm:
            raise ValueError(f"Missing Instagram handle in LEAD #{lead_no}")
        h = hm.group(1).strip().lower()
        handles.append(h)
        pm = re.search(r"^WhatsApp Number:\s*\n(.+)\s*$", body, re.MULTILINE)
        if pm:
            pn = norm_phone(pm.group(1).strip())
            if pn:
                phone_to_leads.setdefault(pn, []).append(lead_no)
    return handles, phone_to_leads


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="Rewrite header lines 1-5 with updated generated date (2026-05-26 UTC).",
    )
    args = parser.parse_args()

    if not LEADS_PATH.is_file():
        print(f"Missing {LEADS_PATH}", file=sys.stderr)
        return 2

    text = LEADS_PATH.read_text(encoding="utf-8")
    handles, phone_map = parse_handles_and_phones(text)

    dup_handles = sorted({h for h in handles if handles.count(h) > 1})
    dup_phones = {p: leads for p, leads in phone_map.items() if len(leads) > 1}

    print(f"Leads parsed: {len(handles)}")
    print(f"Unique handles: {len(set(handles))}")
    if dup_handles:
        print("DUPLICATE HANDLES:", ", ".join(dup_handles), file=sys.stderr)
    if dup_phones:
        print("DUPLICATE PHONE (last-10) across lead numbers:", dup_phones, file=sys.stderr)

    if len(handles) != 100 or len(set(handles)) != 100 or dup_handles or dup_phones:
        return 1

    if args.write:
        lines = text.splitlines()
        if len(lines) >= 5:
            lines[1] = "Generated: 2026-05-26 (UTC) — validated by scripts/build_india_jewellery_leads.py"
            lines[2] = (
                "Source: Public web search snippets (Instagram posts/reels indexed by search engines); "
                "consolidated from prior curation pass."
            )
        LEADS_PATH.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        print(f"Updated header in {LEADS_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
