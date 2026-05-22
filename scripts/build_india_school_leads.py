#!/usr/bin/env python3
"""
Build and maintain India private-school lead database (weak digital presence focus).

Outputs:
  - output/india_school_leads.json
  - output/india_school_leads.csv
  - output/india_school_leads.txt
  - output/priority_outreach_list.txt
  - output/high_conversion_prospects.csv
  - output/schools_without_websites.csv
  - output/schools_weak_branding.csv
"""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_websites import classify_website, compute_lead_score, is_generic_email

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
MASTER_PATH = DATA / "master_school_leads.json"
SEED_DIR = DATA / "seed_batches"

CSV_FIELDS = [
    "school_name",
    "year_established",
    "city",
    "state",
    "address",
    "phone",
    "whatsapp",
    "email",
    "principal_name",
    "director_name",
    "website",
    "website_status",
    "instagram",
    "facebook",
    "linkedin",
    "google_maps",
    "lead_score",
    "notes",
]

FULL_JSON_FIELDS = [
    "school_name",
    "year_established",
    "board",
    "school_type",
    "address",
    "area",
    "city",
    "district",
    "state",
    "pincode",
    "google_maps",
    "latitude",
    "longitude",
    "website",
    "website_status",
    "domain_notes",
    "instagram",
    "facebook",
    "linkedin",
    "youtube",
    "whatsapp",
    "telegram",
    "phone",
    "alternate_phone",
    "landline",
    "email",
    "admission_contact",
    "principal_name",
    "director_name",
    "chairman_name",
    "trustee_name",
    "founder_name",
    "correspondent_name",
    "lead_score",
    "active_admission_campaign",
    "recent_admissions_post_date",
    "engagement_level",
    "no_ssl",
    "broken_website",
    "no_domain_email",
    "source",
    "discovered_at",
    "last_verified_at",
    "notes",
]


def _digits_last10(value: str | None) -> str | None:
    if not value or str(value).lower() == "unknown":
        return None
    digits = re.sub(r"\D", "", str(value))
    return digits[-10:] if len(digits) >= 10 else None


def _norm_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower())


def _norm_key(lead: dict) -> str:
    phone = _digits_last10(lead.get("phone") or lead.get("whatsapp"))
    if phone:
        return f"phone:{phone}"
    ig = (lead.get("instagram") or "").lower()
    m = re.search(r"instagram\.com/([^/]+)", ig)
    if m:
        return f"ig:{m.group(1)}"
    return f"name:{_norm_name(lead.get('school_name', ''))}|{lead.get('city', '').lower()}"


def load_json(path: Path) -> dict | list:
    if not path.exists():
        return {} if path.name.endswith(".json") and "master" in path.name else []
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_seed_batches() -> list[dict]:
    leads: list[dict] = []
    if not SEED_DIR.exists():
        return leads
    for batch_file in sorted(SEED_DIR.glob("batch_*.json")):
        batch = load_json(batch_file)
        if isinstance(batch, list):
            leads.extend(batch)
    return leads


def merge_leads(existing: list[dict], incoming: list[dict]) -> tuple[list[dict], int]:
    by_key: dict[str, dict] = {_norm_key(x): x for x in existing}
    added = 0
    for lead in incoming:
        key = _norm_key(lead)
        if key in by_key:
            old = by_key[key]
            for field, val in lead.items():
                if val and str(val).lower() != "unknown":
                    if not old.get(field) or str(old.get(field)).lower() == "unknown":
                        old[field] = val
            old["last_verified_at"] = _now_iso()
        else:
            lead.setdefault("discovered_at", _now_iso())
            lead.setdefault("last_verified_at", _now_iso())
            by_key[key] = lead
            added += 1
    return list(by_key.values()), added


def enrich_lead(lead: dict, check_http: bool = True) -> dict:
    out = {k: lead.get(k, "") for k in FULL_JSON_FIELDS}
    for k, v in lead.items():
        if v is not None and v != "":
            out[k] = v

    website = out.get("website") or ""
    if check_http:
        status, notes = classify_website(website if website else None)
    else:
        status, notes = ("none", "Not checked") if not website else ("unknown", "Skipped HTTP check")

    out["website_status"] = status
    out["domain_notes"] = notes
    out["broken_website"] = status in {"broken", "parked", "facebook_only"}
    out["no_domain_email"] = is_generic_email(out.get("email"))
    out["lead_score"] = compute_lead_score(out, status)

    if not out.get("admission_contact"):
        out["admission_contact"] = out.get("phone") or out.get("whatsapp") or "Unknown"

    out["last_verified_at"] = _now_iso()
    return out


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_txt(leads: list[dict], path: Path) -> None:
    lines = [
        "INDIA PRIVATE SCHOOL LEADS — WEAK / NO WEBSITE DIGITAL PRESENCE",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "Source: public web search, Instagram/Facebook/JustDial/Sulekha snippets.",
        "Verify every field before outreach.",
        f"Total unique leads: {len(leads)}",
        "",
    ]
    for i, lead in enumerate(sorted(leads, key=lambda x: -int(x.get("lead_score", 0))), start=1):
        lines.append("=" * 60)
        lines.append(f"LEAD #{i} | Score: {lead.get('lead_score')}/10")
        lines.append("=" * 60)
        for field in FULL_JSON_FIELDS:
            val = lead.get(field, "")
            if val and str(val).lower() not in {"", "unknown"}:
                lines.append(f"{field}: {val}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(leads: list[dict], path: Path, fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for lead in sorted(leads, key=lambda x: -int(x.get("lead_score", 0))):
            writer.writerow({k: lead.get(k, "") for k in fields})


def write_priority_lists(leads: list[dict]) -> None:
    high = [l for l in leads if int(l.get("lead_score", 0)) >= 8]
    no_web = [l for l in leads if l.get("website_status") in {"none", "broken", "parked", "facebook_only"}]
    weak = [
        l
        for l in leads
        if l.get("no_domain_email") or l.get("broken_website") or l.get("website_status") == "none"
    ]

    priority_path = OUTPUT / "priority_outreach_list.txt"
    lines = [
        "PRIORITY OUTREACH LIST (lead_score >= 8)",
        f"Count: {len(high)}",
        "",
    ]
    for lead in sorted(high, key=lambda x: -int(x.get("lead_score", 0))):
        lines.append(
            f"- [{lead.get('lead_score')}] {lead.get('school_name')} | {lead.get('city')}, {lead.get('state')} "
            f"| {lead.get('phone') or lead.get('whatsapp') or 'no phone'} | {lead.get('email') or 'no email'}"
        )
    priority_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    write_csv(high, OUTPUT / "high_conversion_prospects.csv", CSV_FIELDS)
    write_csv(no_web, OUTPUT / "schools_without_websites.csv", CSV_FIELDS)
    write_csv(weak, OUTPUT / "schools_weak_branding.csv", CSV_FIELDS)


def build(check_websites: bool = True) -> dict:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    master = load_json(MASTER_PATH)
    if not isinstance(master, dict):
        master = {"version": 1, "leads": []}

    existing = master.get("leads", [])
    seeds = load_seed_batches()
    merged, added = merge_leads(existing, seeds)

    enriched = [enrich_lead(l, check_http=check_websites) for l in merged]
    master["leads"] = enriched
    master["updated_at"] = _now_iso()
    master["total"] = len(enriched)
    save_json(MASTER_PATH, master)

    save_json(OUTPUT / "india_school_leads.json", {"updated_at": master["updated_at"], "total": len(enriched), "leads": enriched})
    write_csv(enriched, OUTPUT / "india_school_leads.csv", CSV_FIELDS)
    write_txt(enriched, OUTPUT / "india_school_leads.txt")
    write_priority_lists(enriched)

    return {"total": len(enriched), "added_this_run": added}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Build India school lead database")
    parser.add_argument("--skip-http", action="store_true", help="Skip live website checks (faster)")
    args = parser.parse_args()
    stats = build(check_websites=not args.skip_http)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
