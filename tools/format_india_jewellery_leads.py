#!/usr/bin/env python3
"""Read tools/leads.compact.jsonl and write ../india_jewellery_instagram_leads.txt."""
from __future__ import annotations

import json
from pathlib import Path

# Short keys: h n c s t w e o y u f a g b k r p m q x — see emit_leads_jsonl.py

FIELDS = [
    "Business Name",
    "Instagram Handle",
    "Instagram URL",
    "Followers Count",
    "City",
    "State",
    "Business Type",
    "WhatsApp Number",
    "Email",
    "Ordering Method",
    "Website Present",
    "Website URL",
    "Recent Activity Date",
    "Average Engagement",
    "Bio Text",
    "Keywords",
    "Reason Qualified",
    "Potential Services Needed",
    "Google Maps Link",
    "Lead Quality Score",
    "Notes",
]


def _row_to_record(row: dict[str, str]) -> dict[str, str]:
    h = (row.get("h") or "").strip()
    url = f"https://www.instagram.com/{h}/" if h else ""
    rec = {
        "Business Name": row.get("n", ""),
        "Instagram Handle": h,
        "Instagram URL": url,
        "Followers Count": row.get("f", ""),
        "City": row.get("c", ""),
        "State": row.get("s", ""),
        "Business Type": row.get("t", ""),
        "WhatsApp Number": row.get("w", ""),
        "Email": row.get("e", ""),
        "Ordering Method": row.get("o", ""),
        "Website Present": row.get("y", ""),
        "Website URL": row.get("u", ""),
        "Recent Activity Date": row.get("a", ""),
        "Average Engagement": row.get("g", ""),
        "Bio Text": row.get("b", ""),
        "Keywords": row.get("k", ""),
        "Reason Qualified": row.get("r", ""),
        "Potential Services Needed": row.get("p", ""),
        "Google Maps Link": row.get("m", ""),
        "Lead Quality Score": row.get("q", ""),
        "Notes": row.get("x", ""),
    }
    return rec


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    jsonl_path = root / "tools" / "leads.compact.jsonl"
    out_path = root / "india_jewellery_instagram_leads.txt"
    rows: list[dict[str, str]] = []
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    lines_out: list[str] = []
    for i, row in enumerate(rows, start=1):
        rec = _row_to_record(row)
        lines_out.append("=" * 50)
        lines_out.append(f"LEAD #{i}")
        lines_out.append("=" * 50)
        for key in FIELDS:
            lines_out.append(f"{key}: {str(rec.get(key, '')).strip()}")
        lines_out.append("")
    out_path.write_text("\n".join(lines_out).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({len(rows)} leads)")


if __name__ == "__main__":
    main()
