#!/usr/bin/env python3
"""Hourly cron entry: discovery tick + build exports + git-ready outputs."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def main() -> int:
    sys.path.insert(0, str(SCRIPTS))

    from discover_batch import run_discovery_tick

    discovery = run_discovery_tick()
    print("Discovery:", json.dumps(discovery))

    from build_india_school_leads import build

    stats = build(check_websites=True)
    print("Build:", json.dumps(stats))

    total = stats.get("total", 0)
    if total < 1000:
        print(f"NOTE: {total} leads in master DB (goal: 1000+). Add seed_batches or automated discovery.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
