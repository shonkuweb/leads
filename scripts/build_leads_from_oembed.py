#!/usr/bin/env python3
"""Build india_jewellery_instagram_leads.txt from Instagram oEmbed JSONL dumps."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "india_jewellery_instagram_leads.txt"

OEMBED_SOURCES = [
    Path("/tmp/oembed.jsonl"),
    Path("/tmp/oembed2.jsonl"),
    Path("/tmp/oembed3.jsonl"),
]

# Dedicated ecommerce domains / large luxury portals — excluded from qualified pool.
WEBSITE_OR_ENTERPRISE = {
    "jalaram_artificial",
    "jewellery_by_rohika",
    "rasasilverjewels",
    "mirarijewels",
    "reetbyshruti",
    "renuoberoiluxuryjewellery",
    "harishee_creation",
    "beadsyde",
    "panoply_by_pearl",
    "caratcrush",
    "sutrafinejewellery",
    "sukkhi_jewellery",
    "misho_designs",
    "nikhaarjewelsindia",
    "amaltaasjewellery",
}

INACTIVE_OR_EMPTY = {"aurum_oasis_jewellery"}

CITY_HINTS: dict[str, tuple[str, str]] = {
    "allurajewelrybangalore": ("Bangalore", "Karnataka"),
    "handmade_jewelry_bangalore": ("Bangalore", "Karnataka"),
    "handmade_jewellery_india": ("India", "—"),
    "kabira_jewels_handmade": ("Bangalore", "Karnataka"),
    "prakashjewellers1989": ("Bangalore", "Karnataka"),
    "praveenjewellers_bangalore": ("Bangalore", "Karnataka"),
    "jewelsofkarnataka": ("Bangalore", "Karnataka"),
    "kingz_silver.pune": ("Pune", "Maharashtra"),
    "kapoorbangles": ("Delhi", "Delhi"),
    "nagpalimitationjewellery": ("Ludhiana", "Punjab"),
    "shreeshyamjewellersrewari": ("Rewari", "Haryana"),
    "mayuralankar": ("Mumbai", "Maharashtra"),
    "abhushanjewellersofficial": ("Pune", "Maharashtra"),
    "jewellersradhakrishna_": ("Hyderabad", "Telangana"),
    "srimahalaxmijewellers.45": ("Hyderabad", "Telangana"),
    "southindian__templejewellery": ("Chennai", "Tamil Nadu"),
    "southindianjewellery": ("Chennai", "Tamil Nadu"),
    "templejewelleryhub_bypriya": ("Chennai", "Tamil Nadu"),
    "meenakari.co": ("Jaipur", "Rajasthan"),
    "oxidised_collection_latest": ("Kolkata", "West Bengal"),
    "a.l.o.n.k.a.r.in": ("Kolkata", "West Bengal"),
    "oxidisedjewelleryshop": ("India", "—"),
    "oxidised_jewellery_store": ("India", "—"),
    "fashionjewelleryindia": ("Mumbai", "Maharashtra"),
    "artificialjewelleryindia": ("India", "—"),
    "artificialjewelleryshop": ("India", "—"),
    "imitationjewellerywholesale": ("India", "—"),
    "imitation_jewellery_wholesale": ("India", "—"),
    "silverjewelleryindia": ("India", "—"),
    "silverjewelsindia": ("India", "—"),
    "chhatralajewels": ("Jodhpur", "Rajasthan"),
}

WHATSAPP_HINTS: dict[str, str] = {
    "southindian__templejewellery": "+91 7904076978 / +91 8610765751",
    "jewelsofkarnataka": "+91 9740234813",
    "kapoorbangles": "+91 9310820050",
    "kingz_silver.pune": "+91 9004341600",
    "trend_jewelryys": "+91 7597344552",
}

BUSINESS_TYPE_DEFAULT = "Fashion / imitation / silver jewellery (verify niche before outreach)"

MANUAL_SCORE_BUMP: dict[str, int] = {
    "southindian__templejewellery": 2,
    "jewelsofkarnataka": 2,
    "kapoorbangles": 2,
    "kingz_silver.pune": 2,
    "thoselittleblingss": 2,
    "wear_nd_shine_jewelry": 1,
}


def parse_display_name(title: str) -> str:
    if "profile on Instagram" in title:
        m = re.match(r"^(.*)'s \(@", title)
        if m:
            return m.group(1).strip()
    return title.split("(")[0].strip() or "Unknown"


def load_oembed_rows(paths: list[Path]) -> dict[str, dict]:
    by_handle: dict[str, dict] = {}
    for p in paths:
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            h = rec["handle"]
            oe = rec.get("oembed") or {}
            if "error" in oe:
                continue
            by_handle[h] = oe
    return by_handle


def score_lead(handle: str, title: str, wa: str) -> int:
    s = 5
    t = title.lower()
    if wa and wa != "Not found in public oEmbed; check Instagram bio":
        s += 2
    if any(
        k in t
        for k in (
            "silver",
            "925",
            "oxid",
            "imitation",
            "temple",
            "jewel",
            "jewellery",
            "jewelry",
            "handmade",
        )
    ):
        s += 1
    s += MANUAL_SCORE_BUMP.get(handle, 0)
    return max(1, min(10, s))


def main() -> None:
    rows = load_oembed_rows(OEMBED_SOURCES)
    qualified = [h for h in rows if h not in WEBSITE_OR_ENTERPRISE and h not in INACTIVE_OR_EMPTY]
    if len(qualified) < 100:
        raise SystemExit(f"Need 100 qualified handles after filters; got {len(qualified)}")

    scored = []
    for h in qualified:
        title = rows[h].get("title") or ""
        wa = WHATSAPP_HINTS.get(h, "Not found in public oEmbed; check Instagram bio")
        scored.append((score_lead(h, title, wa), h))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = [h for _, h in scored[:100]]

    blocks: list[str] = []
    for i, handle in enumerate(top, start=1):
        oe = rows[handle]
        title = oe.get("title") or ""
        display = parse_display_name(title)
        city, state = CITY_HINTS.get(handle, ("India (city not inferred)", "—"))
        wa = WHATSAPP_HINTS.get(handle, "Not found in public oEmbed; check Instagram bio")
        website = "No"
        website_url = "—"
        ordering = (
            "Instagram DM + WhatsApp (numbers above from public posts/listings; re-verify)"
            if wa.startswith("+")
            else "Primarily Instagram DM; confirm WhatsApp in bio or captions"
        )
        score = score_lead(handle, title, wa)
        bio_text = title[:500]
        keys = [
            k
            for k in (
                "oxidised",
                "temple",
                "silver",
                "925",
                "imitation",
                "handmade",
                "fabric",
                "meenakari",
                "resin",
                "bridal",
                "wholesale",
                "artificial",
                "terracotta",
                "bead",
                "wire",
                "afghan",
                "kuchi",
                "american diamond",
                "one gram",
                "navratri",
            )
            if k in title.lower()
        ]
        keywords = ", ".join(sorted(set(keys))) or "jewellery, India, Instagram"
        reason = (
            "India-linked jewellery Instagram account verified via public oEmbed; "
            "not flagged as a known large ecommerce portal in our automated exclusion list."
        )
        services = (
            "Lightweight website or catalog, WhatsApp automation, CRM, Instagram shop, ads, content production"
        )
        notes = (
            "Compiled May 2026 from Instagram oEmbed public metadata plus selective open-web hints. "
            "Follower counts, exact bios, and last-post dates must be confirmed in the Instagram app."
        )

        block = f"""==================================================
LEAD #{i}
==================================================
Business Name:
{display}
Instagram Handle:
@{handle}
Instagram URL:
https://www.instagram.com/{handle}/
Followers Count:
Not available via public oEmbed API (verify inside Instagram)
City:
{city}
State:
{state}
Business Type:
{BUSINESS_TYPE_DEFAULT}
WhatsApp Number:
{wa}
Email:
Not scraped (check bio / contact button)
Ordering Method:
{ordering}
Website Present:
{website}
Website URL:
{website_url}
Recent Activity Date:
Verify live on Instagram (not exposed in oEmbed)
Average Engagement:
Not scraped (use analytics tools if needed)
Bio Text:
{bio_text}
Keywords:
{keywords}
Reason Qualified:
{reason}
Potential Services Needed:
{services}
Google Maps Link:
Not linked from public oEmbed (search business name + city)
Lead Quality Score:
{score}
Notes:
{notes}
"""
        blocks.append(block.strip() + "\n")

    OUT.write_text("\n".join(blocks).strip() + "\n", encoding="utf-8")
    print(f"Wrote {len(top)} leads to {OUT}")


if __name__ == "__main__":
    main()
