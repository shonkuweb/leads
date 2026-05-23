#!/usr/bin/env python3
"""
Post-process india_jewellery_instagram_leads.txt:
- Replace generic OSINT boilerplate Notes with verification-first language.
- Inject public, web-index evidence where available (handle-keyed).
Run from repo root: python3 scripts/patch_india_jewellery_leads.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / "india_jewellery_instagram_leads.txt"

EVIDENCE: dict[str, dict[str, str]] = {
    "jodhpuri__jewellery": {
        "WhatsApp Number": "+91 7568283224",
        "Ordering Method": "WhatsApp (number in public reel caption; Jodhpuri / payal-house style listing).",
        "Notes": "Indexed Instagram reel on jodhpuri__jewellery referenced WhatsApp 7568283224 for orders. Verify current bio and highlights.",
    },
    "sujatha_gold_covering_works": {
        "WhatsApp Number": "+91 7382222208 (caption also listed 7997757703, 8886428899; bulk line 7036132171)",
        "Ordering Method": "WhatsApp booking with COD option per indexed reel caption; screenshot-to-order style.",
        "Notes": "Public indexed reel on sujatha_gold_covering_works listed multiple WhatsApp lines for bookings and bulk. Confirm which number is primary today.",
    },
    "aakankshajewellery": {
        "WhatsApp Number": "+91 9324512333",
        "Ordering Method": "WhatsApp for details (Maharashtrian / bridal jewellery style posts).",
        "Notes": "Indexed Instagram post snippet referenced WhatsApp 9324512333 for Aakanksha Jewellery. Verify live bio and ordering flow.",
    },
    "rajshreejewellershyderabad": {
        "WhatsApp Number": "+91 9000070515 / +91 9705333099",
        "Ordering Method": "Phone / shop contact (Hyderabad Manikonda); verify WhatsApp availability on profile.",
        "Notes": "Indexed post snippet for Rajshree Jewellers Hyderabad listed shop phone contacts. Showroom-forward; confirm Instagram-first selling vs owned ecommerce.",
    },
    "bcos_its_silver": {
        "Ordering Method": "DM / message for enquiries (typical for Hyderabad silver guttapusalu sellers); confirm WhatsApp in bio.",
        "Notes": "Indexed legacy post on bcos_its_silver for Hyderabad-area pure silver / guttapusalu style pieces. Verify current contact channels on profile.",
    },
    "rohitbhaijewellers": {
        "WhatsApp Number": "+91 9953916916 / +91 9953916903",
        "Ordering Method": "WhatsApp + showroom visit (Chandni Chowk, Delhi).",
        "Notes": "Large established Delhi gold retailer with showroom presence — weaker fit for IG-only SMB digital upsell; verify needs vs enterprise stack.",
        "Lead Quality Score": "4",
    },
    "indiagemsandbeads": {
        "Website Present": "Yes",
        "Website URL": "https://ebay.us/R99JJH (eBay listing linked from indexed post — not owned D2C site)",
        "Notes": "Indexed post linked out to eBay; may still want owned landing + WhatsApp CRM. Confirm India ops and primary channel.",
    },
}

GENERIC_NOTE = (
    "Handle surfaced via public web index / Instagram discovery heuristics (India jewellery segment). "
    "Before outreach: open the live profile, confirm posting recency (30 days), capture bio WhatsApp/wa.me, "
    "check for Shopify/Woo/Meesho-only vs owned site, and dedupe against nearby clone pages."
)


def field(block: str, name: str) -> str:
    m = re.search(
        rf"^{re.escape(name)}:\s*\n(.+?)(?=\n[^\n]+:\s*\n|\Z)",
        block,
        re.M | re.S,
    )
    return (m.group(1).strip() if m else "")


def replace_field(block: str, name: str, value: str) -> str:
    pat = rf"^({re.escape(name)}:\s*\n)(.+?)(?=\n[^\n]+:\s*\n|\Z)"
    return re.sub(pat, rf"\g<1>{value}\n", block, count=1, flags=re.M | re.S)


def patch_block(block: str) -> str:
    handle = field(block, "Instagram Handle").strip().lower()
    if "OSINT seed from public discovery" in block or "OSINT seed" in field(block, "Notes"):
        block = replace_field(block, "Notes", GENERIC_NOTE)
    ev = EVIDENCE.get(handle)
    if ev:
        for fk, v in ev.items():
            block = replace_field(block, fk, v)
    return block


def main() -> None:
    text = TXT.read_text(encoding="utf-8")
    parts = re.split(r"(={10,}\s*LEAD #\d+\s*={10,})", text)
    out: list[str] = [parts[0]]
    for i in range(1, len(parts), 2):
        sep = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        out.append(sep)
        out.append(patch_block(body))
    TXT.write_text("".join(out), encoding="utf-8")
    print("Patched", TXT)


if __name__ == "__main__":
    main()
