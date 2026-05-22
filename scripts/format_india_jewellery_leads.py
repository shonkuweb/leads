#!/usr/bin/env python3
"""Generate india_jewellery_instagram_leads.txt from leads.csv (repo root)."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leads.csv"
OUT_PATH = ROOT / "india_jewellery_instagram_leads.txt"


def main() -> None:
    rows: list[dict[str, str]] = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if len(rows) != 100:
        raise SystemExit(f"Expected 100 leads, found {len(rows)}")

    handles = [r["instagram_handle"].strip().lower() for r in rows]
    if len(set(handles)) != 100:
        raise SystemExit("Duplicate Instagram handles detected")

    phones = [r.get("whatsapp_number", "").strip() for r in rows if r.get("whatsapp_number", "").strip()]
    if len(phones) != len(set(phones)):
        raise SystemExit("Duplicate WhatsApp numbers detected")

    lines: list[str] = []
    for i, r in enumerate(rows, start=1):
        lines.append("=" * 50)
        lines.append(f"LEAD #{i}")
        lines.append("=" * 50)
        for key in [
            "business_name",
            "instagram_handle",
            "instagram_url",
            "followers_count",
            "city",
            "state",
            "business_type",
            "whatsapp_number",
            "email",
            "ordering_method",
            "website_present",
            "website_url",
            "recent_activity_date",
            "average_engagement",
            "bio_text",
            "keywords",
            "reason_qualified",
            "potential_services_needed",
            "google_maps_link",
            "lead_quality_score",
            "notes",
        ]:
            label = (
                "Instagram Handle:"
                if key == "instagram_handle"
                else "".join([w.capitalize() if w.islower() else w for w in key.split("_")])
                .replace("Instagramurl", "Instagram URL")
                .replace("Whatsapp", "WhatsApp")
                .replace("Bio", "Bio")
            )
            # Fix a few labels to match requested format exactly
            pretty = {
                "business_name": "Business Name",
                "instagram_handle": "Instagram Handle",
                "instagram_url": "Instagram URL",
                "followers_count": "Followers Count",
                "city": "City",
                "state": "State",
                "business_type": "Business Type",
                "whatsapp_number": "WhatsApp Number",
                "email": "Email",
                "ordering_method": "Ordering Method",
                "website_present": "Website Present",
                "website_url": "Website URL",
                "recent_activity_date": "Recent Activity Date",
                "average_engagement": "Average Engagement",
                "bio_text": "Bio Text",
                "keywords": "Keywords",
                "reason_qualified": "Reason Qualified",
                "potential_services_needed": "Potential Services Needed",
                "google_maps_link": "Google Maps Link",
                "lead_quality_score": "Lead Quality Score",
                "notes": "Notes",
            }[key]
            val = r.get(key, "").replace("\\n", "\n")
            lines.append(f"{pretty}:")
            lines.append(val)
            lines.append("")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(rows)} leads)")


if __name__ == "__main__":
    main()
