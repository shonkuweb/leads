#!/usr/bin/env python3
"""Hourly discovery cycle: rotate search queries, merge leads, export, persist state."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_india_school_leads import CURATED_LEADS, load_master, merge_leads, save_master, write_exports

CONFIG_PATH = ROOT / "config" / "search_queries.json"
STATE_PATH = ROOT / "data" / "discovery_state.json"


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"query_index": 0, "runs": 0, "last_queries": []}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def next_queries(batch_size: int = 3) -> list[str]:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    queries = cfg.get("google_queries", [])
    if not queries:
        return []
    state = load_state()
    idx = state.get("query_index", 0) % len(queries)
    selected = []
    for i in range(batch_size):
        selected.append(queries[(idx + i) % len(queries)])
    state["query_index"] = (idx + batch_size) % len(queries)
    state["runs"] = state.get("runs", 0) + 1
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["last_queries"] = selected
    save_state(state)
    return selected


def main() -> None:
    queries = next_queries()
    print("Discovery cycle — next search batch:")
    for q in queries:
        print(f"  - {q}")

    existing = load_master()
    merged, added = merge_leads(existing, CURATED_LEADS)
    meta = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "added_this_run": added,
        "total": len(merged),
        "queries_rotated": queries,
    }
    save_master(merged, meta)
    write_exports(merged)
    print(f"Cycle complete: {len(merged)} leads in master (+{added} new).")


if __name__ == "__main__":
    main()
