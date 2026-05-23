#!/usr/bin/env python3
"""Merge curated extras, dedupe, rewrite generate_jewellery_leads.py, export TXT."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "scripts" / "generate_jewellery_leads.py"
EXTRA = ROOT / "scripts" / "leads_extra.json"
OUT_TXT = ROOT / "india_jewellery_instagram_leads.txt"

REMOVE_HANDLES = frozenset({"amoraartsandjewels", "harshianbujewellery", "goyaz"})

GENERATOR_TAIL = r'''

def render_txt(leads: list[dict[str, str]]) -> str:
    blocks: list[str] = []
    for i, lead in enumerate(leads, start=1):
        h = lead["handle"]
        handle_clean = h.strip().lstrip("@")
        url = f"https://www.instagram.com/{handle_clean}/"
        lines = [
            "",
            "=" * 50,
            f"LEAD #{i}",
            "=" * 50,
            f"Business Name: {lead['business']}",
            f"Instagram Handle: @{handle_clean}",
            f"Instagram URL: {url}",
            f"Followers Count: {lead['followers']}",
            f"City: {lead['city']}",
            f"State: {lead['state']}",
            f"Business Type: {lead['type']}",
            f"WhatsApp Number: {lead['whatsapp']}",
            f"Email: {lead['email']}",
            f"Ordering Method: {lead['ordering']}",
            f"Website Present: {lead['website_yn']}",
            f"Website URL: {lead['website_url']}",
            f"Recent Activity Date: {lead['activity']}",
            f"Average Engagement: {lead['engagement']}",
            f"Bio Text: {lead['bio']}",
            f"Keywords: {lead['keywords']}",
            f"Reason Qualified: {lead['qualified']}",
            f"Potential Services Needed: {lead['services']}",
            f"Google Maps Link: {lead['maps']}",
            f"Lead Quality Score: {lead['score']}",
            f"Notes: {lead['notes']}",
        ]
        blocks.append("\n".join(lines))
    return "\n".join(blocks).lstrip("\n") + "\n"


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "india_jewellery_instagram_leads.txt"
    out.write_text(render_txt(LEADS), encoding="utf-8")
    print(f"Wrote {out} ({len(LEADS)} leads)")


if __name__ == "__main__":
    main()
'''

HEADER = '''#!/usr/bin/env python3
"""Generate india_jewellery_instagram_leads.txt from curated public-source snapshots."""
from __future__ import annotations

from pathlib import Path

# Each entry: unique Instagram handle; phone numbers normalized where known; no duplicate phones.
'''


def norm_phone(p: str) -> str:
    if not p or p.lower().startswith("verify"):
        return ""
    digits = re.sub(r"\D", "", p)
    if len(digits) >= 10:
        return digits[-10:]
    return digits


def load_leads_from_generator() -> list[dict[str, str]]:
    src = GEN.read_text(encoding="utf-8")
    mod = ast.parse(src)
    for node in mod.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "LEADS":
            seg = ast.get_source_segment(src, node.value)
            assert seg is not None
            return eval(seg, {"__builtins__": {}}, {})
    raise RuntimeError("LEADS not found")


def render_python_file(leads: list[dict[str, str]]) -> str:
    parts = [HEADER, "LEADS: list[dict[str, str]] = [\n"]
    for d in leads:
        parts.append("    {\n")
        for k, v in d.items():
            ks = json.dumps(k, ensure_ascii=False)
            vs = json.dumps(v, ensure_ascii=False)
            parts.append(f"        {ks}: {vs},\n")
        parts.append("    },\n")
    parts.append("]")
    parts.append(GENERATOR_TAIL)
    return "".join(parts)


def dedupe_merge(
    base: list[dict[str, str]], extra: list[dict[str, str]]
) -> list[dict[str, str]]:
    seen_handles: set[str] = set()
    seen_phones: set[str] = set()
    seen_biz: set[str] = set()
    out: list[dict[str, str]] = []

    def add_row(row: dict[str, str]) -> None:
        h = row["handle"].strip().lstrip("@").lower()
        if h in seen_handles:
            return
        p = norm_phone(row.get("whatsapp", ""))
        if p and p in seen_phones:
            return
        b = row["business"].strip().lower()
        if b in seen_biz:
            return
        seen_handles.add(h)
        if p:
            seen_phones.add(p)
        seen_biz.add(b)
        out.append(row)

    for row in base:
        if row["handle"].strip().lstrip("@").lower() in REMOVE_HANDLES:
            continue
        add_row(row)
    for row in extra:
        add_row(row)
    return out


def run_rebuild() -> None:
    base = load_leads_from_generator()
    extra = json.loads(EXTRA.read_text(encoding="utf-8"))
    merged = dedupe_merge(base, extra)
    if len(merged) != 100:
        raise SystemExit(f"Expected 100 leads after merge, got {len(merged)}")
    GEN.write_text(render_python_file(merged), encoding="utf-8")
    ns: dict = {}
    exec(compile(GEN.read_text(encoding="utf-8"), str(GEN), "exec"), ns)
    txt = ns["render_txt"](ns["LEADS"])
    OUT_TXT.write_text(txt, encoding="utf-8")
    print(f"Updated {GEN.name} and wrote {OUT_TXT} ({len(merged)} leads)")


if __name__ == "__main__":
    run_rebuild()
