#!/usr/bin/env python3
"""
Rotate discovery search queries for hourly automation.

This module records which query buckets were processed and loads the next
seed batch file when new curated data is added under data/seed_batches/.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "discovery_state.json"

SEARCH_QUERIES = [
    '"admissions open" "school" "instagram.com" India',
    '"new private school" India CBSE 2024',
    '"play school" WhatsApp admissions India',
    '"English medium school" Facebook admissions',
    'site:justdial.com private school CBSE',
    'site:sulekha.com play school admissions',
    '"school" gmail.com admissions India',
    '"CBSE school" "admissions open" 2025',
    '"montessori school" Bihar admissions',
    '"private school" Ranchi WhatsApp',
    '"proposed CBSE school" Gujarat admissions',
    '"preschool" "admissions open" Maharashtra',
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"last_run": None, "batch_index": 0, "queries_completed": [], "total_discovered": 0}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def next_query(state: dict) -> str:
    completed = set(state.get("queries_completed", []))
    for q in SEARCH_QUERIES:
        if q not in completed:
            return q
    state["queries_completed"] = []
    return SEARCH_QUERIES[0]


def run_discovery_tick() -> dict:
    """Advance discovery cursor; actual web scraping is done via curated seed batches."""
    state = load_state()
    query = next_query(state)
    state["queries_completed"] = list(state.get("queries_completed", [])) + [query]
    state["batch_index"] = int(state.get("batch_index", 0)) + 1
    state["last_run"] = _now_iso()
    state["last_query"] = query
    save_state(state)
    return {"query": query, "batch_index": state["batch_index"], "hint": "Add curated results to data/seed_batches/batch_NNN.json"}


if __name__ == "__main__":
    print(json.dumps(run_discovery_tick(), indent=2))
